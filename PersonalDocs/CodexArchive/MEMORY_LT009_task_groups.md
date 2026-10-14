# Task Group: Sampler LT009 m001 root-motion FBX refit and delivery audit

scope: Resume or review LT009 Blender root-motion asset work; preserve source FBX, canonical output naming, and the distinction between Blender/round-trip checks and UE runtime acceptance.
applies_to: cwd=G:\\baratli_BARATLI-PC1_4572\\Sampler; reuse_rule=read `PersonalDocs/Work/LT009/Context.md` first for current settings and evidence; asset paths and delivery state are checkout-specific.

## Task 1: Deliver m001 Claymore stop/start RootMonotonic FBX batch

### rollout_summary_files

- rollout_summaries/2026-09-13T07-43-17-JrQp-lt009_blender_fbx_root_motion_workflow_and_m001_context_upda.md (cwd=\\?\G:\\baratli_BARATLI-PC1_4572\\Sampler, rollout_path=C:\\Users\\baratli\\.codex\\sessions\\2026\\09\\13\\rollout-2026-09-13T15-43-17-01a099b8-722e-73c0-a171-f08fa00f2b05.jsonl, updated_at=2026-09-14T05:49:16+00:00, thread_id=01a099b8-722e-73c0-a171-f08fa00f2b05, success: context updated; Blender/FBX checks passed, UE acceptance unperformed)

### keywords

- LT009, m001, RootMonotonic.FBX, Root_M, Bip001, ik_root, 10 cm/s, SHA-256, FBX 2013 Binary, world-pose, RunLeftStop, SprintRightStop

## User preferences

- when delivering revised FBX assets, the user required source FBX unchanged, canonical `<source_stem>_RootMonotonic.FBX` names, and explicitly rejected new V2 names -> overwrite only the generated canonical outputs and prove the delivered bytes and root curves. [Task 1] [ad-hoc note]
- when organizing Blender work, use unused lowercase `m###` subtasks under LT009; additional clips for the same work stay in m001. [Task 1] [ad-hoc note]

## Reusable knowledge

- Current LT009 context is `PersonalDocs/Work/LT009/Context.md`; detailed execution history is `PersonalDocs/Work/m001/m001_ClaymoreStopAnimations.md`. The batch delivered RunLeftStop, RunRightStop, RunStart, SprintLeftStop, SprintRightStop, and RunStart_End; UE import/runtime acceptance remains unperformed. [Task 1] [ad-hoc note]
- For this stop/end batch, root motion must have finite positive speed and follow the original root curve while compensating pelvis, all other bones, and final world mesh motion. Use 10 cm/s; inspect Start separately. The retained RunStart only slows in its final 1/60-second interval (about 1 cm/s). [Task 1] [ad-hoc note]
- Identify `Root_M` as the Blender Armature; compensate `Bip001` and `ik_root`; expect nine translation curves. Preserve actual key times and the source Take's one-frame-short span. Validate float32 speed margin, whole/half-frame world pose, a fresh FBX reimport, SHA-256, and parsed delivered root curves. [Task 1] [ad-hoc note]
- LT009-only UE Animation Sequence export defaults: FBX 2013 Binary; Preview Mesh on; LOD, Force Front XAxis, Map Skeletal Motion to Root, and ordinary-body Morph Targets off. Do not mix UE export, Blender import, and UE reimport settings. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Standard Blender export failed this batch's 0.01 mm world-pose tolerance; preserve FBX structure rather than assuming a normal export is interchangeable. Blender changes/timestamps alone do not prove delivery. [Task 1] [ad-hoc note]

## Task 2: Restore LT009 context and verify Blender MCP read-only health

### rollout_summary_files

- rollout_summaries/2026-09-11T04-27-18-0wnI-blender_mcp_read_only_health_check.md (cwd=\\?\\G:\\baratli_BARATLI-PC1_4572\\Sampler, rollout_path=C:\\Users\\baratli\\.codex\\sessions\\2026\\09\\11\\rollout-2026-09-11T12-27-18-01a08eb8-4d0d-7561-8dd7-91a24d832bbe.jsonl, updated_at=2026-09-11T04:47:10+00:00, thread_id=01a08eb8-4d0d-7561-8dd7-91a24d832bbe, success: read-only connectivity confirmed)

### keywords

- LT009, blender-mcp, Blender 5.2.1 LTS, get_addon_status, get_scene_info, get_viewport_screenshot, protocol_version=5, addon_version=1.6, telemetry_consent=true, 127.0.0.1:9876, DISABLE_TELEMETRY

# Task Group: Blender MCP local installation and safe connectivity checks

scope: Use the recorded Windows Blender MCP setup for read-only scene inspection; treat scene-writing and telemetry decisions as separate, user-authorized work.
applies_to: cwd=C:\Users\baratli and G:\baratli_BARATLI-PC1_4572\Sampler; reuse_rule=paths, installed versions, and listener status are machine/time-specific; recheck before live use.

## Task 1: Install, connect, and document blender-mcp

### rollout_summary_files


### keywords

- LT009, blender-mcp, Blender 5.2.1 LTS, uvx, install-addon, get_addon_status, get_scene_info, 127.0.0.1:9876, execute_blender_code, telemetry_consent

## Reusable knowledge

- LT009 is the Sampler long-term route for Blender, `.blend`, `bpy`, Add-ons, import/export, DCC tools, and content-pipeline work. Observed installation: Blender `D:\Blender 5.2\blender.exe` 5.2.1 LTS, managed Python 3.11 via `uvx --python 3.11 blender-mcp install-addon`, and enabled Add-on at `C:\Users\baratli\AppData\Roaming\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py`. [Task 1]
- Prove connectivity with Add-on status, `127.0.0.1:9876` listener/connection, and a minimal read-only `get_scene_info`/screenshot闂備胶鍋ㄩ崕鏌ュ绩缁ㄥ嵓 tool signatures alone. This setup passed those read-only checks; scene writes, saving, and rollback remain untested. [Task 1]

## Failures and how to do differently

- PowerShell may block `codex.ps1`; use `C:\Users\baratli\AppData\Roaming\npm\codex.cmd`. Background Blender's `cannot start server in background mode` is expected and does not invalidate Add-on installation. [Task 1]
- `DISABLE_TELEMETRY=true` did not make the Add-on runtime consent false (`telemetry_consent=true`). Treat `execute_blender_code` as high-impact: save the `.blend` and confirm scope before any write. [Task 1]

