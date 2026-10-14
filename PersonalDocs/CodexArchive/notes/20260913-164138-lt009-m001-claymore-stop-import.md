# LT009-m001 已创建：Blender 修改双侧大剑停步动画

- 用户于 2026-09-13 明确要求新增 m 子任务，修改 G:\Workspace\AssetModified\1 下的两个动画序列，并先测试其中一个导入当前 Blender 的过程。
- 正式任务记录已创建：G:\baratli_BARATLI-PC1_4572\Sampler\PersonalDocs\Work\m001\m001_ClaymoreStopAnimations.md。后续 m001 状态以该记录及实际资源为准。
- 编号 m001 现已占用，父任务为 LT009；下一可分配序号为 m002，实际分配前核对最新记录。这取代此前编号规则中“尚无具体子任务、下一编号 m001”的状态。
- 输入为 AS_Vera_Claymore_RunLeftStop.FBX 和 AS_Vera_Claymore_RunRightStop.FBX，均位于 G:\Workspace\AssetModified\1。
- 当前状态：m001 进行中。已将左侧动画导入当时运行的 Blender 5.2.1 LTS，通过导入、最终骨骼/网格求值、若干帧视口和实时播放检查；右侧尚未导入，具体动作修改要求尚待用户提供。
- 左侧导入结果：1 个 Mesh、1 个 Armature、131 根骨骼、1 个绑定 Action；60 FPS、帧 1–126；源 FBX 的 LimbNode 名称与 Blender 骨骼名称一致，实际曲线时间范围也一致。Root_M 为 Armature 对象，包含对象级动画；其子级顶层骨骼为 Bip001、ik_root。
- 证据与工作文件目录：G:\baratli_BARATLI-PC1_4572\Sampler\Saved\Blender\m001\20260913-164138。导入前备份为 before_import.blend，导入后工作副本为 m001_RunLeftStop_import_check.blend，另有 JSON 检查报告及帧 1、63、126 的 PNG 截图。
- 操作结束时当前 Blender 打开上述工作副本，时间轴设为 1–126、60 FPS，停止播放并停在第 1 帧；原 Cube/Light/Camera 保留但视口隐藏。此现场状态需在后续操作前重新读取。
- 两个源 FBX 均未修改，前后 SHA-256 相同。这里只证明 Blender 导入链路，不构成动作质量、滑步、材质贴图、UE 导出往返或 UE 运行时验收。
