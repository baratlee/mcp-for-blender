# LT009 context and m001 animation workflow update

User explicitly requested on 2026-09-14: summarize the lessons and requirements and save them to LT009 context.

Authoritative current context: G:\baratli_BARATLI-PC1_4572\Sampler\PersonalDocs\Work\LT009\Context.md. The LT009 task file and repository memory index now route there. Detailed execution history remains in PersonalDocs\Work\m001\m001_ClaymoreStopAnimations.md. Read the context for exact settings, constraints, evidence paths and current file names.

Supersede stale m001 summaries: the first imported animation had 131 bones, 60 FPS and frames 1-126, NOT 31 bones, 30 FPS or frames 1-26. m001 has now delivered six modified clips: RunLeftStop, RunRightStop, RunStart, SprintLeftStop, SprintRightStop, RunStart_End. All passed Blender world-pose and FBX roundtrip checks; UE import/runtime acceptance is still unperformed and m001 remains active.

Persisted user requirements: Blender asset work uses unused lowercase m### subtasks under LT009; same-task additional clips remain in m001. Root motion must progress strictly with finite positive speed and fit the original root curve, while compensating pelvis, all other bones and final world mesh motion. This stop/end batch uses 10 cm/s; Start must be inspected separately. Existing RunStart was retained because only its last 1/60-second interval was slow, about 1 cm/s.

Keep source FBX unchanged. Deliver <source_stem>_RootMonotonic.FBX in G:\Workspace\AssetModified\1\RootMonotonic. Revisions overwrite the existing generated output names; user explicitly rejected new V2 FBX names. Verify delivered bytes by SHA-256 and parse actual delivered root curves; Blender changes or timestamps alone do not prove delivery.

Use the recorded UE Animation Sequence export defaults for LT009 only (FBX 2013 Binary, Preview Mesh on, LOD/Force Front XAxis/Map Skeletal Motion to Root off, ordinary-body Morph Targets off). Do not mix UE export, Blender import and UE reimport settings.

Implementation/evidence safeguards: identify Root_M as the Blender Armature object, compensate Bip001 and ik_root; 9 translation curves only. Preserve FBX structure because standard Blender export failed this batch's 0.01 mm world-pose tolerance. Preserve actual key times and document the source Take's one-frame-short span. Include float32 speed margin, whole/half-frame evaluated world-pose checks and fresh FBX reimport. Current context distinguishes root-trajectory projection allowances from world-pose tolerance and explains speed-floor feasibility limits.
