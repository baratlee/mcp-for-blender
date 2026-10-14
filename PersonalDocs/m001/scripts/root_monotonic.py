"""m001: bounded-speed root translation with world-pose compensation in Blender."""

import hashlib
import json
import math
from pathlib import Path

import bpy
import numpy as np


WORK = Path(r"G:\baratli_BARATLI-PC1_4572\Sampler\Saved\Blender\m001\20260913-172626")
MIN_SPEED = 0.01  # meters per second
POSITION_TOL = 1e-5  # meters; 0.01 mm
LINEAR_MATRIX_TOL = 1e-6


def curves(action):
    return [fc for layer in action.layers for strip in layer.strips
            for bag in strip.channelbags for fc in bag.fcurves]


def assign_action(root, action):
    root.animation_data.action = action
    root.animation_data.action_slot = action.slots[0]


def curve_hash(action):
    h = hashlib.sha256()
    for fc in curves(action):
        h.update(f"{fc.data_path}:{fc.array_index}".encode())
        data = np.empty(len(fc.keyframe_points) * 2, dtype=np.float32)
        fc.keyframe_points.foreach_get("co", data)
        h.update(data.tobytes())
        h.update("|".join(k.interpolation for k in fc.keyframe_points).encode())
    return h.hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def fit_progress(values, times, distance, speed_floor=MIN_SPEED):
    """L2 isotonic projection after subtracting the positive speed floor."""
    residual = values - speed_floor * times
    upper = distance - speed_floor * times[-1]
    assert upper > 0, "Speed floor exceeds available endpoint displacement"
    blocks = []
    for index in range(1, len(values) - 1):
        blocks.append([index, index, residual[index], 1])
        while len(blocks) > 1 and blocks[-2][2] / blocks[-2][3] > blocks[-1][2] / blocks[-1][3]:
            right, left = blocks.pop(), blocks.pop()
            blocks.append([left[0], right[1], left[2] + right[2], left[3] + right[3]])
    fitted = np.zeros(len(values), dtype=np.float64)
    fitted[-1] = upper
    for low, high, total, count in blocks:
        fitted[low:high + 1] = np.clip(total / count, 0.0, upper)
    return fitted + speed_floor * times


def make_action(root_name, mesh_name, output_name, max_lateral_projection_m=1e-5,
                account_for_storage_precision=False):
    WORK.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    root, mesh = bpy.data.objects[root_name], bpy.data.objects[mesh_name]
    original = root.animation_data.action
    assert bpy.data.actions.get(output_name) is None, "Output Action already exists"
    assert root.parent is None and not root.constraints
    assert not root.animation_data.drivers and not root.animation_data.nla_tracks
    assert not any(p.constraints for p in root.pose.bones)
    tops = [p for p in root.pose.bones if p.parent is None]
    assert {p.name for p in tops} == {"Bip001", "ik_root"}
    assert all(p.bone.use_local_location for p in tops)
    source_curves = {(fc.data_path, fc.array_index): fc for fc in curves(original)}
    fps = scene.render.fps / scene.render.fps_base
    first, last = map(int, original.frame_range)
    frames = np.arange(first, last + 1)
    times = (frames - first) / fps
    old_positions = np.array([[source_curves[("location", i)].evaluate(int(f)) for i in range(3)] for f in frames])
    displacement = old_positions[-1] - old_positions[0]
    distance = np.linalg.norm(displacement)
    direction = displacement / distance
    old_progress = (old_positions - old_positions[0]) @ direction
    lateral = old_positions - old_positions[0] - old_progress[:, None] * direction
    lateral_deviation = float(np.max(np.linalg.norm(lateral, axis=1)))
    assert lateral_deviation <= max_lateral_projection_m, "Trajectory exceeds the allowed projection onto its endpoint line"
    speed_margin = 0.0
    if account_for_storage_precision:
        # Bound key storage and half-frame evaluation rounding in meters and FBX centimeters.
        magnitudes = np.max(np.abs(old_positions), axis=0)
        world_ulp = np.spacing(magnitudes.astype(np.float32)).astype(np.float64)
        fbx_ulp = np.spacing((magnitudes * 100.0).astype(np.float32)).astype(np.float64) * 0.01
        speed_margin = float(2 * fps * np.linalg.norm(2 * world_ulp + fbx_ulp))
    new_progress = fit_progress(old_progress, times, distance, MIN_SPEED + speed_margin)
    new_positions = old_positions[0] + new_progress[:, None] * direction
    new_positions[0], new_positions[-1] = old_positions[0], old_positions[-1]
    saved_frame, saved_subframe = scene.frame_current, scene.frame_subframe
    scene.frame_set(first)
    root_linear = np.array(root.matrix_world, dtype=np.float64)[:3, :3]
    for path in ("rotation_euler", "scale"):
        for axis in range(3):
            fc = source_curves[(path, axis)]
            values = [fc.evaluate(int(f)) for f in frames]
            assert max(values) - min(values) < 1e-10, "Root linear transform is animated"
    valid_groups = {g.index for g in mesh.vertex_groups if g.name in {b.name for b in root.data.bones if b.use_deform}}
    assert all(any(g.group in valid_groups and g.weight > 0 for g in v.groups) for v in mesh.data.vertices)
    original_hash = curve_hash(original)
    original.use_fake_user = True
    modified = original.copy()
    modified.name = output_name
    modified.use_fake_user = True
    destination = {(fc.data_path, fc.array_index): fc for fc in curves(modified)}
    replacements = {("location", i): new_positions[:, i] for i in range(3)}
    delta_armature = (old_positions - new_positions) @ np.linalg.inv(root_linear).T
    for pose_bone in tops:
        path = pose_bone.path_from_id() + ".location"
        rest_linear = np.array(pose_bone.bone.matrix_local, dtype=np.float64)[:3, :3]
        delta_local = delta_armature @ np.linalg.inv(rest_linear).T
        for axis in range(3):
            source = source_curves[(path, axis)]
            original_local = np.array([source.evaluate(int(f)) for f in frames])
            replacements[(path, axis)] = original_local + delta_local[:, axis]
    for key, values in replacements.items():
        fc = destination[key]
        assert len(fc.keyframe_points) == len(frames)
        assert all(k.interpolation == "LINEAR" for k in fc.keyframe_points)
        for k, frame, value in zip(fc.keyframe_points, frames, values):
            assert abs(k.co.x - frame) < 1e-6
            k.co.y = float(value)
        fc.update()
    assert curve_hash(original) == original_hash, "Original Action was modified"
    assign_action(root, modified)
    scene.frame_set(saved_frame, subframe=saved_subframe)
    errors = np.linalg.norm(new_positions - old_positions, axis=1)
    report = {
        "root": root_name, "mesh": mesh_name, "original_action": original.name,
        "modified_action": modified.name, "original_curve_sha256": original_hash,
        "modified_curve_sha256": curve_hash(modified), "frame_range": [first, last],
        "fps": fps, "duration_s": times[-1], "min_speed_m_s": MIN_SPEED,
        "fitting_speed_floor_m_s": MIN_SPEED + speed_margin,
        "storage_precision_speed_margin_m_s": speed_margin,
        "direction": direction.tolist(), "endpoint_displacement_m": displacement.tolist(),
        "max_original_lateral_deviation_m": lateral_deviation,
        "max_allowed_lateral_projection_m": max_lateral_projection_m,
        "max_root_correction_m": float(errors.max()),
        "rms_root_correction_m": float(np.sqrt(np.mean(errors ** 2))),
        "planned_min_speed_m_s": float(np.diff(new_progress).min() * fps),
        "planned_max_speed_m_s": float(np.diff(new_progress).max() * fps),
        "compensated_bones": [p.name for p in tops],
        "edited_channels": [f"{path}[{axis}]" for path, axis in replacements],
        "position_tolerance_m": POSITION_TOL, "linear_matrix_tolerance": LINEAR_MATRIX_TOL,
        "samples": [{"frame": int(f), "time_s": float(t), "original_root_m": p.tolist(),
                     "modified_root_m": n.tolist()} for f, t, p, n in zip(frames, times, old_positions, new_positions)],
    }
    dump(WORK / f"{output_name}_edit.json", report)
    return {key: value for key, value in report.items() if key != "samples"}


def evaluate(root, mesh):
    graph = bpy.context.evaluated_depsgraph_get()
    arm = root.evaluated_get(graph)
    root_matrix = np.array(arm.matrix_world, dtype=np.float64)
    bone_matrices = np.array([root_matrix @ np.array(p.matrix, dtype=np.float64) for p in arm.pose.bones])
    evaluated_mesh = mesh.evaluated_get(graph)
    result_mesh = evaluated_mesh.to_mesh()
    try:
        positions = np.empty(len(result_mesh.vertices) * 3, dtype=np.float64)
        result_mesh.vertices.foreach_get("co", positions)
        positions = positions.reshape((-1, 3))
        world = np.array(evaluated_mesh.matrix_world, dtype=np.float64)
        positions = positions @ world[:3, :3].T + world[:3, 3]
    finally:
        evaluated_mesh.to_mesh_clear()
    assert np.isfinite(positions).all() and np.isfinite(bone_matrices).all()
    return root_matrix, bone_matrices, positions


def validate_chunk(output_name, begin, end):
    report = json.loads((WORK / f"{output_name}_edit.json").read_text(encoding="utf-8"))
    scene = bpy.context.scene
    root, mesh = bpy.data.objects[report["root"]], bpy.data.objects[report["mesh"]]
    original, modified = bpy.data.actions[report["original_action"]], bpy.data.actions[report["modified_action"]]
    times = np.arange(report["frame_range"][0], report["frame_range"][1] + 0.25, 0.5)
    old_frame, old_subframe = scene.frame_current, scene.frame_subframe
    rows = []
    try:
        for sample in times[begin:end]:
            frame, subframe = int(math.floor(sample)), float(sample % 1)
            assign_action(root, original)
            scene.frame_set(frame, subframe=subframe)
            old_root, old_bones, old_vertices = evaluate(root, mesh)
            assign_action(root, modified)
            scene.frame_set(frame, subframe=subframe)
            new_root, new_bones, new_vertices = evaluate(root, mesh)
            pos = np.linalg.norm(new_bones[:, :3, 3] - old_bones[:, :3, 3], axis=1)
            basis = np.abs(new_bones[:, :3, :3] - old_bones[:, :3, :3])
            vertices = np.linalg.norm(new_vertices - old_vertices, axis=1)
            rows.append({"frame": float(sample), "max_bone_position_error_m": float(pos.max()),
                         "max_bone_linear_matrix_error": float(basis.max()),
                         "max_vertex_error_m": float(vertices.max()),
                         "worst_bone": root.pose.bones[int(pos.argmax())].name,
                         "worst_vertex": int(vertices.argmax()),
                         "root_world_m": new_root[:3, 3].tolist()})
    finally:
        assign_action(root, modified)
        scene.frame_set(old_frame, subframe=old_subframe)
    dump(WORK / f"{output_name}_check_{begin:03d}_{end:03d}.json", rows)
    return {"sample_count": len(rows), "sample_range": [rows[0]["frame"], rows[-1]["frame"]],
            "max_bone_position_error_m": max(r["max_bone_position_error_m"] for r in rows),
            "max_bone_linear_matrix_error": max(r["max_bone_linear_matrix_error"] for r in rows),
            "max_vertex_error_m": max(r["max_vertex_error_m"] for r in rows),
            "original_action_unchanged": curve_hash(original) == report["original_curve_sha256"]}


def summarize_validation(output_name):
    report = json.loads((WORK / f"{output_name}_edit.json").read_text(encoding="utf-8"))
    rows = []
    for path in sorted(WORK.glob(f"{output_name}_check_*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8")))
    expected = list(np.arange(report["frame_range"][0], report["frame_range"][1] + 0.25, 0.5))
    assert [r["frame"] for r in rows] == expected, "Missing or duplicate samples"
    points = np.array([r["root_world_m"] for r in rows])
    progress = (points - points[0]) @ np.array(report["direction"])
    speeds = np.diff(progress) * report["fps"] * 2
    result = {"samples": len(rows), "bone_count": len(bpy.data.objects[report["root"]].data.bones),
              "vertex_count": len(bpy.data.objects[report["mesh"]].data.vertices),
              "max_bone_position_error_m": max(r["max_bone_position_error_m"] for r in rows),
              "max_bone_linear_matrix_error": max(r["max_bone_linear_matrix_error"] for r in rows),
              "max_vertex_error_m": max(r["max_vertex_error_m"] for r in rows),
              "actual_min_speed_m_s": float(speeds.min()), "actual_max_speed_m_s": float(speeds.max()),
              "nonpositive_intervals": int((speeds <= 0).sum()),
              "endpoint_error_m": float(np.linalg.norm(points[-1] - np.array(report["samples"][-1]["original_root_m"]))),
              "original_action_unchanged": curve_hash(bpy.data.actions[report["original_action"]]) == report["original_curve_sha256"]}
    result["passed"] = (result["max_bone_position_error_m"] <= POSITION_TOL and
                        result["max_bone_linear_matrix_error"] <= LINEAR_MATRIX_TOL and
                        result["max_vertex_error_m"] <= POSITION_TOL and
                        result["actual_min_speed_m_s"] >= MIN_SPEED - 1e-5 and
                        result["nonpositive_intervals"] == 0 and
                        result["endpoint_error_m"] <= 1e-7 and result["original_action_unchanged"])
    dump(WORK / f"{output_name}_validation.json", result)
    return result


def export_preserved_fbx(source_path, output_name):
    """Transfer nine translation channels while preserving the source FBX graph."""
    from io_scene_fbx import parse_fbx, encode_bin
    from mathutils import Euler

    source, version = parse_fbx.parse(str(source_path))
    objects = next(e for e in source.elems if e.id == b"Objects")
    connections = next(e for e in source.elems if e.id == b"Connections")
    by_id = {e.props[0]: e for e in objects.elems if e.props}
    models = {e.props[1].split(b"\0")[0].decode(): e for e in objects.elems if e.id == b"Model"}
    report = json.loads((WORK / f"{output_name}_edit.json").read_text(encoding="utf-8"))

    def model_curves(name, property_name):
        model_id = models[name].props[0]
        nodes = [c.props[1] for c in connections.elems
                 if len(c.props) > 3 and c.props[2] == model_id and c.props[3] == property_name]
        result = {}
        for node in nodes:
            for c in connections.elems:
                if len(c.props) > 3 and c.props[2] == node and c.props[1] in by_id:
                    elem = by_id[c.props[1]]
                    if elem.id == b"AnimationCurve":
                        result[c.props[3].split(b"|")[-1].decode()] = elem
        assert set(result) == {"X", "Y", "Z"}
        return [result[axis] for axis in "XYZ"]

    def part(curve, name):
        return next(e for e in curve.elems if e.id == name)

    def values(curve):
        return np.asarray(part(curve, b"KeyValueFloat").props[0], dtype=np.float64)

    root_curves = model_curves("Root_M", b"Lcl Translation")
    times = np.asarray(part(root_curves[0], b"KeyTime").props[0], dtype=np.int64)
    old = np.array([values(c) for c in root_curves]).T
    target = np.array([r["modified_root_m"] for r in report["samples"]]) * 100.0
    assert old.shape == target.shape
    baseline = np.array([r["original_root_m"] for r in report["samples"]])
    assert np.max(np.abs(old * 0.01 - baseline)) < 1e-6, "Unexpected FBX axis or unit mapping"
    target[0], target[-1] = old[0], old[-1]
    rotation = [values(c) for c in model_curves("Root_M", b"Lcl Rotation")]
    scaling = [values(c) for c in model_curves("Root_M", b"Lcl Scaling")]
    assert all(np.ptp(v) < 1e-10 for v in rotation + scaling)
    root_linear = np.array(Euler(tuple(math.radians(v[0]) for v in rotation), "XYZ").to_matrix(), dtype=np.float64)
    root_linear = root_linear @ np.diag([v[0] for v in scaling])
    compensation = (old - target) @ np.linalg.inv(root_linear).T
    overrides, edited_ids = {}, []

    def replace_translation(curve, new_values):
        assert np.array_equal(np.asarray(part(curve, b"KeyTime").props[0]), times)
        overrides[id(part(curve, b"KeyValueFloat"))] = [np.asarray(new_values, dtype=np.float32)]
        # Blender FBX exporter flag 24836 denotes linear interpolation.
        overrides[id(part(curve, b"KeyAttrFlags"))] = [np.array([24836], dtype=np.int32)]
        overrides[id(part(curve, b"KeyAttrDataFloat"))] = [np.zeros(4, dtype=np.float32)]
        overrides[id(part(curve, b"KeyAttrRefCount"))] = [np.array([len(times)], dtype=np.int32)]
        edited_ids.append(curve.props[0])

    for axis, curve in enumerate(root_curves):
        replace_translation(curve, target[:, axis])
    for name in ("Bip001", "ik_root"):
        assert any(c.props[:3] == [b"OO", models[name].props[0], models["Root_M"].props[0]]
                   or tuple(c.props[:3]) == (b"OO", models[name].props[0], models["Root_M"].props[0])
                   for c in connections.elems)
        for axis, curve in enumerate(model_curves(name, b"Lcl Translation")):
            replace_translation(curve, values(curve) + compensation[:, axis])

    metadata_updates = []
    def fix_span(elem):
        if elem.id in (b"LocalTime", b"ReferenceTime"):
            overrides[id(elem)] = [int(times[0]), int(times[-1])]
            metadata_updates.append(elem.id.decode())
        elif elem.id == b"P" and elem.props[0] in (b"LocalStop", b"TimeSpanStop"):
            props = list(elem.props)
            props[-1] = int(times[-1])
            overrides[id(elem)] = props
            metadata_updates.append(elem.props[0].decode())
        for child in elem.elems:
            fix_span(child)
    fix_span(source)
    methods = {"Y": "add_int16", "B": "add_bool", "C": "add_char", "Z": "add_int8",
               "I": "add_int32", "L": "add_int64", "F": "add_float32", "D": "add_float64",
               "S": "add_string", "R": "add_bytes", "f": "add_float32_array",
               "d": "add_float64_array", "i": "add_int32_array", "l": "add_int64_array",
               "b": "add_bool_array", "c": "add_byte_array"}

    def clone(elem):
        copy = encode_bin.FBXElem(elem.id)
        for type_code, value in zip(elem.props_type, overrides.get(id(elem), elem.props)):
            if chr(type_code) == "B":
                value = bool(value)
            getattr(copy, methods[chr(type_code)])(value)
        copy.elems = [clone(child) for child in elem.elems]
        return copy

    output = WORK / f"{output_name}.FBX"
    assert not output.exists(), "Refusing to overwrite output FBX"
    encode_bin.write(str(output), clone(source), version)
    readback, read_version = parse_fbx.parse(str(output))
    read_objects = next(e for e in readback.elems if e.id == b"Objects")
    read_ids = {e.props[0]: e for e in read_objects.elems if e.props}

    def digest(elem):
        h = hashlib.sha256(elem.id + bytes(elem.props_type))
        for value in elem.props:
            if hasattr(value, "tobytes"):
                h.update(value.tobytes())
            elif isinstance(value, bytes):
                h.update(value)
            else:
                h.update(repr(value).encode())
        for child in elem.elems:
            h.update(digest(child))
        return h.digest()

    unchanged = []
    for ident, elem in by_id.items():
        if ident not in edited_ids and elem.id != b"AnimationStack":
            unchanged.append(digest(elem) == digest(read_ids[ident]))
    assert all(unchanged), "Unrelated FBX data changed"
    result = {"output": str(output), "version": read_version, "bytes": output.stat().st_size,
              "source": str(source_path), "edited_translation_curve_count": len(edited_ids),
              "preserved_other_objects": len(unchanged), "other_objects_identical": all(unchanged),
              "frame_time_span_ticks": [int(times[0]), int(times[-1])],
              "timing_metadata_updated": metadata_updates,
              "interpolation": "LINEAR on root and compensated translation channels"}
    dump(WORK / f"{output_name}_preserved_export.json", result)
    return result


def validate_roundtrip_chunk(output_name, test_scene_name, test_root_name, test_mesh_name, begin, end):
    report = json.loads((WORK / f"{output_name}_edit.json").read_text(encoding="utf-8"))
    root, mesh = bpy.data.objects[report["root"]], bpy.data.objects[report["mesh"]]
    base = next(s for s in bpy.data.scenes if root.name in s.objects)
    test = bpy.data.scenes[test_scene_name]
    new_root, new_mesh = bpy.data.objects[test_root_name], bpy.data.objects[test_mesh_name]
    assert set(root.data.bones.keys()) == set(new_root.data.bones.keys())
    assert len(mesh.data.vertices) == len(new_mesh.data.vertices)
    assert list(new_root.animation_data.action.frame_range) == report["frame_range"]
    original = bpy.data.actions[report["original_action"]]
    modified = bpy.data.actions[report["modified_action"]]
    order = [list(new_root.pose.bones.keys()).index(name) for name in root.pose.bones.keys()]
    samples = np.arange(report["frame_range"][0], report["frame_range"][1] + 0.25, 0.5)
    old_frame, old_subframe = base.frame_current, base.frame_subframe
    rows = []
    try:
        for sample in samples[begin:end]:
            frame, subframe = math.floor(sample), float(sample % 1)
            bpy.context.window.scene = base
            assign_action(root, original)
            base.frame_set(frame, subframe=subframe)
            _, bones, vertices = evaluate(root, mesh)
            bpy.context.window.scene = test
            test.frame_set(frame, subframe=subframe)
            nr, nb, nv = evaluate(new_root, new_mesh)
            nb = nb[order]
            rows.append({"frame": float(sample),
                         "max_bone_position_error_m": float(np.linalg.norm(nb[:, :3, 3] - bones[:, :3, 3], axis=1).max()),
                         "max_bone_linear_matrix_error": float(np.abs(nb[:, :3, :3] - bones[:, :3, :3]).max()),
                         "max_vertex_error_m": float(np.linalg.norm(nv - vertices, axis=1).max()),
                         "root_world_m": nr[:3, 3].tolist()})
    finally:
        bpy.context.window.scene = base
        assign_action(root, modified)
        base.frame_set(old_frame, subframe=old_subframe)
    dump(WORK / f"{output_name}_roundtrip_check_{begin:03d}_{end:03d}.json", rows)
    return {"sample_count": len(rows), "max_bone_position_error_m": max(r["max_bone_position_error_m"] for r in rows),
            "max_bone_linear_matrix_error": max(r["max_bone_linear_matrix_error"] for r in rows),
            "max_vertex_error_m": max(r["max_vertex_error_m"] for r in rows)}


def summarize_roundtrip(output_name):
    report = json.loads((WORK / f"{output_name}_edit.json").read_text(encoding="utf-8"))
    rows = []
    for path in sorted(WORK.glob(f"{output_name}_roundtrip_check_*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8")))
    expected = list(np.arange(report["frame_range"][0], report["frame_range"][1] + 0.25, 0.5))
    assert [r["frame"] for r in rows] == expected
    positions = np.array([r["root_world_m"] for r in rows])
    speeds = np.diff(positions @ np.array(report["direction"])) * report["fps"] * 2
    result = {"samples": len(rows), "max_bone_position_error_m": max(r["max_bone_position_error_m"] for r in rows),
              "max_bone_linear_matrix_error": max(r["max_bone_linear_matrix_error"] for r in rows),
              "max_vertex_error_m": max(r["max_vertex_error_m"] for r in rows),
              "actual_min_speed_m_s": float(speeds.min()), "actual_max_speed_m_s": float(speeds.max()),
              "nonpositive_intervals": int((speeds <= 0).sum())}
    result["passed"] = (result["max_bone_position_error_m"] <= POSITION_TOL and
                        result["max_bone_linear_matrix_error"] <= LINEAR_MATRIX_TOL and
                        result["max_vertex_error_m"] <= POSITION_TOL and
                        result["actual_min_speed_m_s"] >= MIN_SPEED - 1e-5 and result["nonpositive_intervals"] == 0)
    dump(WORK / f"{output_name}_roundtrip_validation.json", result)
    return result
