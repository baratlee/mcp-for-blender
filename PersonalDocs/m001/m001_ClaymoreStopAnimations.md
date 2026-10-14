# m001：Blender 修改大剑起步与停步动画

> **迁移说明（2026-10-13）**：本文从 Sampler 工程 `PersonalDocs` 迁入本仓库，Sampler 侧已删除。
> - 文中 `Saved/Blender/m001/…` 证据目录已按用户决定删除，路径仅作历史记录，文件不存在。
> - `G:\Workspace\AssetModified` 下的素材与交付未动；UE 侧验收门禁文档仍在 Sampler 工程内。
> - 本文早期由 Codex 维护，文中“Codex”字样为当时的执行者记录。

- 父任务：LT009（Blender 相关事项与开发维护）。
- 编号：m001 / LT009-m001。
- 创建日期：2026-09-13。
- **已过时（2026-10-14 用户确认）**：本任务的成果物不再使用、不再跟进；本文只作为 [RootMotionRetiming](../LT009/RootMotionRetiming.md) 的方法来源与历史记录。
- 状态（截至 2026-09-16）：进行中；两个 Run Stop、RunStart、两个 Sprint Stop、RunStart_End 和 SprintStart 共七段修改副本、Blender 世界运动对照及 FBX 回读均通过，待用户查看与 UE 侧验收。
- 用户目标：修改 `G:\Workspace\AssetModified\m001` 下本任务指定的动画序列，另存新序列，使根运动严格单调、持续前进且尽量接近原曲线，同时保持除根节点外所有骨骼和角色最终网格的世界运动不变。
- 素材目录：原始 FBX 在 `G:\Workspace\AssetModified\m001\Input`，交付在 `...\m001\Output`（原 `RootMonotonic`）；2026-10-14 由原 `AssetModified\1` 迁入，本文路径已同步，但交付目录里的 README 与 verification 仍写旧路径。
- 可复用要求与恢复入口：[LT009 当前上下文](../LT009/Context.md)；下文按处理批次保留详细证据。

## 输入资源

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| `G:\Workspace\AssetModified\m001\Input\AS_Vera_Claymore_RunLeftStop.FBX` | 4489008 | `8106F50A637518348100673A167A9B148380AC69DD46FBF480B8EA50B93BB50C` |
| `G:\Workspace\AssetModified\m001\Input\AS_Vera_Claymore_RunRightStop.FBX` | 4489008 | `A73B35D0D51CBA5C5CBFA09EA44216F0542465DFA38E638D5A919B8C8B59C450` |

## 首次导入检查步骤

1. 备份当前 Blender 场景，记录导入前状态。
2. 导入 `AS_Vera_Claymore_RunLeftStop.FBX`。
3. 核对 FBX 元数据、导入结果、骨骼和 Mesh 绑定、Action 与时间范围。
4. 采样最终骨骼和变形网格、检查若干动画帧的视口表现。
5. 保存检查结果和导入后的工作副本；核对源 FBX 未改变。

证据目录：`Saved/Blender/m001/20260913-164138/`。

## 首次导入检查结果（2026-09-13）

结论：`AS_Vera_Claymore_RunLeftStop.FBX` 可以导入当前 Blender，绑定的 Action 可以驱动骨骼及最终变形网格，时间轴播放可推进。该结论仅覆盖导入链路，不表示动画质量、滑步或 UE 往返已验收。

| 检查项 | 结果与依据 |
|---|---|
| 环境 | 当前 GUI 实例 Blender 5.2.1 LTS；MCP Add-on 1.6，协议 5/5 |
| 导入结果 | `FINISHED`，耗时约 1.63 秒；导入日志仅有 `FBX version: 7300`，未出现警告或错误 |
| 导入设置 | `use_anim=True`、`anim_offset=1`、`global_scale=1`；`use_manual_orientation=False`、`automatic_bone_orientation=False`、`ignore_leaf_bones=False`、`bake_space_transform=False`；其余采用当前 FBX 导入操作器默认值 |
| 模型与骨骼 | `SK_Vera_Bd13002` Mesh：38,739 顶点、61,820 面；`Root_M` Armature：131 根骨骼。FBX 的 131 个 LimbNode 名称与导入骨骼名称完全一致，无缺失或额外骨骼 |
| Root 与蒙皮绑定 | FBX 的 `Root_M` 类型为 Root，在 Blender 中对应 Armature 对象；顶层骨骼为 `Bip001`、`ik_root`。Mesh 的 Armature 修改器指向 `Root_M`，对象父级也为 `Root_M` |
| Action | `Root_M\|Unreal Take\|Base Layer` 绑定在 Armature；共 1,319 条 FCurve、159,894 个关键帧点 |
| 时间范围 | 60 FPS，帧 1–126。FBX 实际曲线关键时间 0–96,221,162,500，按 46,186,158,000 ticks/s 换算为 2.083333 秒；加导入偏移 1 后与 Blender 范围一致 |
| 最终动画求值 | 帧 1、32、63、94、126 的全部骨骼矩阵和全部最终网格顶点均为有限值；顶点数量稳定。非首帧顶点相对首帧发生变化，证明蒙皮实际受动画驱动 |
| 视口检查 | 帧 1、63、126 可见从抬腿动作到站立收尾的姿势变化；抽查姿势未见明显炸网格、断肢或骨骼拉伸。使用灰色 Solid 显示，材质与贴图未验收 |
| 实时播放 | `animation_play` 启动成功；随后读回仍在播放，帧从 1 推进到 34；检查后停止并回到第 1 帧 |
| 源文件保护 | 导入后两个 FBX 的 SHA-256 与上表一致；右侧文件未导入 |

### 交付与现场状态

- 导入前场景备份：before_import.blend。原场景尚未保存，备份包含原有 Cube、Light、Camera。
- 导入后工作文件：m001_RunLeftStop_import_check.blend。当前 Blender 保持打开此文件，时间轴 1–126、60 FPS，停在第 1 帧。
- 导入对象位于 `m001_RunLeftStop_Import` 集合。原有 Cube、Light、Camera 保留，当前视口隐藏；视口显示设置仅用于清楚观察角色。
- 视口证据：帧 1、帧 63、帧 126。
- 结构与求值证据：import_result.json、evaluated_animation_check.json、source_key_time_range.json、playback_check.json。

## MCP 能力探索：时长与根运动读取（2026-09-13）

- 已用 MCP 在当前 Blender 中读取绑定 Action、对象级 FCurve，并逐帧读取依赖图求值后的 `Root_M.matrix_world`；共采样帧 1–126，采样后恢复到用户原有的第 1 帧。
- 当前根运动由 `Root_M` Armature 对象承载；对象无父级、约束、Driver 或 NLA Track。其位置 FCurve、对象位置与求值后世界坐标在所有整数帧一致，最大差值为 0。
- 场景为 METRIC，`scale_length=1`。下述数值为 Blender 世界坐标，换算为 cm；未当作 UE 坐标轴或 UE 运行时位移。
- 当前 Blender Action 的首末关键帧间隔为 `(126-1)/60 = 2.083333 s`。源 FBX Take 的 LocalTime 声明为 `2.066667 s`；曲线在声明范围外还有 1 个尾帧。逐一比较全部 FCurve，帧 125 与帧 126 的数值完全相同，最大差值为 0。
- 根节点起点为 `(0, 0, 0) cm`，终点为 `(3.568086, -60.793865, 0) cm`；首末净位移长度 `60.898483 cm`，逐帧累积路径长度 `74.275533 cm`。整段 Z 坐标恒为 0，世界旋转变化为 0°。
- 根位移并非单调前进：例如 0.5 s 时 Y 为 `-49.446806 cm`，1.0 s 时为 `-43.869850 cm`，随后继续到 `-60.793865 cm`。这描述导入动画的数据，不构成滑步或 Bug 裁决。
- 已验证能力包括读取时间范围与帧率、关键帧及插值方式、逐帧根平移/旋转、每帧位移和速度，以及导出数值报告。当前数据不能替代 UE 中的 Root Motion 提取、Mover 消费和 Actor/Capsule 实際位移。
- 完整报告：root_motion_inspection.json；逐帧坐标和速度：root_motion_samples.csv。
- 本轮未改动动画关键帧、骨骼或源 FBX，未保存覆盖 `.blend`。

## 严格单调根运动与世界运动保持：实施结果

用户明确要求另存新动画序列，根运动不得倒退、停顿或瞬移，尽可能贴合原轨迹；盆骨及其他非根骨骼和最终网格的世界运动保持不变。用户已明确授权实施。

- 算法：沿原起终点方向拟合进度，速度下限为 `0.01 m/s`。令 `u(t)=s(t)-v_min*t`，对 u 做固定端点、带上下界的等权最小二乘单调回归；恢复 s 后逐帧线性插值，保证正速度与有限斜率。首末位置、60 FPS、Blender 1–126 帧保持一致，根 Z、旋转和缩放不变。
- 补偿：对 `Bip001`、`ik_root` 分支应用与 `P_new = inverse(A_new) * A_old * P_old` 等价的平移补偿，处理 Root_M 的 0.01 缩放及骨骼参考姿势；其他局部动画曲线保留。
- 修改副本：[root_monotonic.py](scripts/root_monotonic.py) 复制原 Action，编辑根及两个一级分支的共 9 条平移曲线。两个原始 Action 的曲线哈希前后保持一致。
- 验证：每段对所有 131 根非根骨骼和 38,739 个最终网格顶点执行 251 个整帧/半帧对照。位置容差在验证前固定为 `1e-5 m`（0.01 mm），世界矩阵线性部分容差为 `1e-6`；两段均通过，原 FBX 哈希与输入表一致。

| 最终 FBX 回读项目 | 左侧 | 右侧 |
|---|---:|---:|
| 根最大位置调整 | 3.612672 cm | 18.609592 cm |
| 根位置调整 RMS | 1.486837 cm | 7.719014 cm |
| 最低根速度（浮点实测） | 0.999499 cm/s | 0.999928 cm/s |
| 最高根速度 | 210.443846 cm/s | 196.150303 cm/s |
| 停顿或回退区间数 | 0 | 0 |
| 最大骨骼世界位置误差 | 0.000152 mm | 0.000141 mm |
| 最大网格世界位置误差 | 0.000374 mm | 0.000473 mm |
| 骨骼世界旋转/缩放矩阵差值 | 0 | 0 |

### FBX 输出方式

标准 Blender 导出探针在时间对齐后仍出现约 0.026 mm 的回读姿势误差，未作为交付结果。最终从源 FBX 保留骨架、蒙皮和其他曲线，直接转写验证过的 9 条平移曲线，设置为线性插值；其余 1,945 个 FBX 对象内容逐一核对一致。

保留 FBX 7300 Binary 格式。源 Take 声明比实际曲线短一帧，输出的 Take/时间范围元数据对齐到实际曲线末端 2.083333 秒，保持 Blender 1–126 帧。最终 FBX 重新导入后骨骼名称、数量、时间范围以及世界运动对照均通过。

### 交付与证据

- 交付目录：`G:\Workspace\AssetModified\m001\Output`。新 FBX 分别为 `AS_Vera_Claymore_RunLeftStop_RootMonotonic.FBX`、`AS_Vera_Claymore_RunRightStop_RootMonotonic.FBX`；可编辑工程为 `m001_ClaymoreStop_RootMonotonic.blend`，附 README 和验证汇总。
- 编辑前备份：before_root_edit.blend。
- 完整证据：`Saved/Blender/m001/20260913-172626/`，含每段 `_edit.json`、`_validation.json`、`_roundtrip_validation.json`、全部分段采样、FBX 对象一致性报告及未采用的导出探针。
- 可编辑场景为 `m001_LeftStop`、`m001_RightStop`。原 Action 和测试场景均保留；自动审批拒绝了测试数据清理，采用保留数据的安全替代方式完成另存。

## 验证边界

- 本阶段完成两段动画副本的根运动修改、Blender 对照与 FBX 回读验证。
- UE 回导、Root Motion 提取、Mover/Actor/Capsule 消费、碰撞和运行时视觉/滑步验收尚未执行。
- Blender 视口和求值结果不能替代 UE 中的最终动画表现验收。

## 后续

### 第二批追加处理（2026-09-13）

用户新增 `AS_Vera_Claymore_RunStart.FBX`、`AS_Vera_Claymore_SprintLeftStop.FBX`、`AS_Vera_Claymore_SprintRightStop.FBX`，明确要求同样处理并注意 Start 类型；作为 m001 的同一处理事项继续执行。

- 三段均完成根位移严格单调化、`Bip001`/`ik_root` 补偿、原 Action 保护、Blender 世界姿态及最终 FBX 回导验证。源文件及第一批动作内容未改变。
- RunStart 主体本来单调，仅末尾重复帧需要修正；最大根位置调整 0.166667 mm，保留原起步加速。两个 Sprint Stop 最大调整分别为 18.164689 cm、0.345863 cm。
- SprintLeftStop 的侧向偏离为 0.751502 mm，明确允许最多 1 mm 的输入轨迹投影范围，将根拟合到首末连线；最终角色世界位置验收容差仍为 0.01 mm。
- 两个 Sprint 首次候选的实测最低速度受到 float32 舍入影响，略低于 1 cm/s 的验收范围；候选 Action 和报告保存在 `PrecisionProbe` / `precision_probe/`。最终拟合按存储精度加入约 0.00755 cm/s 的速度余量，未放宽验收阈值。
- RunStart 检查 117 个整帧/半帧采样点，两个 Sprint 各 283 个；每段覆盖全部 131 根非根骨骼与 38,739 个最终顶点。FBX 回读最大骨骼世界位置误差小于 0.0005 mm，最大网格世界位置误差小于 0.0014 mm，旋转/缩放矩阵差为 0，非正速度区间为 0。
- 全部保持 60 FPS。实际曲线范围：RunStart 1–59 帧 / 0.966667 s；两个 Sprint 1–142 帧 / 2.35 s。源 Take 分别声明 0.95 s 和 2.333333 s，沿用第一批约定将输出 Take 对齐实际末键，不裁尾帧。
- 证据与编辑前备份：`Saved/Blender/m001/20260913-200834/`。实现脚本快照为 `root_monotonic_used.py`，源哈希见 `source_manifest.json`，汇总见 `verification_m001_Batch2.json`。
- 新 FBX 均使用 `_RootMonotonic` 后缀，可编辑工程为 `m001_Claymore_RootMonotonic_Batch2.blend`，说明为 `README_m001_Batch2.md`；交付目录继续使用 `G:\Workspace\AssetModified\m001\Output`，不覆盖第一批文件。
- 本批未执行 UE 导入、压缩或运行时验收；m001 保持进行中，待用户查看。

### Run Stop V2：增加平缓段推进量（2026-09-13）

- 用户反馈两个 Run Stop 修改版存在过于平缓的根位移区间，并明确选择“根位移持续、明显推进，同时尽量贴合原曲线”。
- 第一版实测：Left 的 27–71 帧 / 0.433333–1.166667 s 仅推进 0.733333 cm，114–126 帧仅推进 0.2 cm；Right 的 17–126 帧 / 0.266667–2.083333 s 仅推进 1.816667 cm，占时长的 87.2%。1 cm/s 下限满足正速度，但未达到用户要求的明显推进。
- 本次仅为两个 Run Stop 生成 `_RootMonotonic_V2` 副本，将模块本次调用的 `MIN_SPEED` 设为 0.1 m/s，启用存储精度余量，保持固定首末位置及逐帧最小二乘拟合。原脚本默认值和第二批三个动画不变。
- 相同三个区间的 V2 推进量为 7.334721 cm、2.000378 cm、18.170097 cm。相对原始动画的最大根位置调整为 Left 5.711311 cm、Right 33.111535 cm；由盆骨与 IK 一级分支补偿。
- 每段完成 251 个整帧/半帧的全部骨骼及网格验证，并通过最终 FBX 回读；最大骨骼世界位置误差 0.000225 mm，最大网格世界位置误差 0.000402 mm，旋转/缩放差值为 0，非正速度区间为 0。
- 保留两段 60 FPS、1–126 帧、2.083333 s 的第一版时间范围。两个源 FBX 和此前 18 个 Action 的哈希均保持一致。
- 证据与编辑前备份：`Saved/Blender/m001/20260913-205932/`。新工程为 `m001_Claymore_RunStops_RootMonotonic_V2.blend`；报告为 `verification_RunStops_V2.json`；交付目录仍为 `G:\Workspace\AssetModified\m001\Output`，新增文件不覆盖第一版和第二批。
- 本轮未执行 UE 导入或运行时验收，m001 继续等待用户查看根轨迹效果。

### Run Stop 交付文件名（2026-09-13）

用户明确要求不使用 V2 文件名，直接覆盖此前制作导出的文件。已将经验证的 10 cm/s 根速度版本覆盖到交付目录原有的 `AS_Vera_Claymore_RunLeftStop_RootMonotonic.FBX`、`AS_Vera_Claymore_RunRightStop_RootMonotonic.FBX`。两文件 SHA-256 分别为 `A19F2E494BDB8537D9783CA47FFE4C1A0A002F78601D2A052014BB1EB7F2CFE7`、`49DFC0C1B83AF8A9267F656FE4A1FAA4EF39435E580AFCB77E032BD6C9ADD3BE`，与已验证的工作区输出逐一一致。父目录原始输入 FBX 未修改；带 V2 的工作区文件及验证报告仍作为本轮证据。

### 其余三段复查与 Sprint Stop 覆盖（2026-09-13）

用户要求检查其余三个动画，必要时重新生成；沿用“根位移持续、明显推进，同时尽量贴合原曲线”及覆盖原导出文件名的约定。

- RunStart 仅最后 58–59 帧（0.016667 秒）低于 10 cm/s，实测约 1.001358 cm/s，没有持续的平缓区间；保留现有 FBX 和起步加速曲线。文件与 Action 哈希均与此前验证结果一致，完整姿态验证沿用相同数据的第二批证据。
- SprintLeftStop 的 35–103 帧原交付仅推进 1.141885 cm，130–142 帧仅推进 0.672216 cm；SprintRightStop 的 103–142 帧仅推进 0.654912 cm。两个 Sprint 从原始 Action 重新拟合，根速度下限为 10 cm/s，含存储精度余量；保持首末位置、60 FPS、1–142 帧 / 2.35 秒及世界姿态补偿。
- 同一区间的新推进量分别为 11.341895 cm、2.001511 cm、6.504910 cm。相对原始动画的最大根位置调整分别为 SprintLeftStop 21.757714 cm、SprintRightStop 6.045863 cm。
- 每个 Sprint 完成 283 个整帧/半帧采样，检查全部 131 根非根骨骼和 38,739 个最终网格顶点，并通过最终 FBX 重新导入对照。回读最低根速度分别为 10.006698 cm/s、10.004997 cm/s，非正速度区间均为 0；最大骨骼世界位置误差 0.000453 mm，最大网格世界位置误差 0.001108 mm，旋转/缩放矩阵差为 0。位置容差仍为 0.01 mm。
- 已覆盖交付目录原有的两个 Sprint `_RootMonotonic.FBX`，未新增 V2 文件名；同步覆盖 `m001_Claymore_RootMonotonic_Batch2.blend`、`README_m001_Batch2.md` 和 `verification_m001_Batch2.json`。FBX SHA-256 分别为 `8DC028B5A76CB98C53268E6D65E0894F9E671EB866EA8B50787053F7A6A0489C`、`57D621D3457D39ECFDC2438C8627E270CEFE8846CC6EAACB48074218C2EB7AE5`；复制后逐一核对一致。
- 五个原始输入 FBX、RunStart 导出和两个 Run Stop 导出均未变化。此前 22 个 Action 曲线内容保留，旧 Sprint 修改动作以 `_Archived_1cms` 后缀保存。当前工作工程停在 `m001_SprintLeftStop` 第 69 帧。
- 本次证据与编辑前备份位于 `Saved/Blender/m001/20260913-212126/`；覆盖前交付副本位于其中 `previous_delivery/`，复制校验见 `delivery_verified.json`。未执行 UE 导入或运行时验收。

### RunStart_End 追加处理（2026-09-14）

用户新增 `G:\Workspace\AssetModified\m001\Input\AS_Vera_Claymore_RunStart_End.FBX`，明确要求按 m001 同样处理。源 SHA-256 为 `AC4647BF36D98C9760630939547363AF399C7187A9C0D0AAB139229D3586E06F`。

- 原动画为 60 FPS、1–122 帧 / 2.016667 秒，首末净位移 22.161839 cm，有 40 个帧间隔停顿或回退；最大侧向偏离 6.841287 mm。
- 沿用收尾动画 10 cm/s 的根速度下限，含存储精度余量；固定首末位置并沿首末连线最小二乘拟合，通过 `Bip001`、`ik_root` 分支补偿。该片段的输入投影允许范围为 10 mm，角色世界位置验证容差仍为 0.01 mm。根最大位置调整 28.132127 cm，RMS 12.397273 cm；原 Action 曲线保持不变。
- 根 Z、旋转、缩放和全部关键帧时间保持不变；源 Take 声明 2 秒，沿用此前规则将输出 Take 对齐实际末键 2.016667 秒。
- 修改前后及 FBX 重新导入均覆盖 243 个整帧/半帧采样、全部 131 根非根骨骼及 38,739 个最终网格顶点。回读最低根速度 10.000854 cm/s，最高 129.596794 cm/s，停顿或回退区间为 0；骨骼最大世界位置误差 0.000361 mm，网格最大世界位置误差 0.000485 mm，旋转/缩放矩阵差为 0。
- 初次合并验证/导出调用被自动审批以可能覆盖原始输入为由拦截；已改为分别验证，并使用哈希一致的工作区输入副本导出新文件，后续审批及导出通过。源文件始终保留，另外 1,945 个 FBX 对象内容逐一一致。
- 已交付 `Output/AS_Vera_Claymore_RunStart_End_RootMonotonic.FBX`，SHA-256 为 `FC56F56F7594D1824D2DC7A05ACF68956E54B70914A60E842DF02D6968031EC8`。复制后核对哈希，并直接解析交付文件内的根曲线：最低速度 10.000883 cm/s，122 个关键帧，无停顿或回退区间。
- 同目录新增 `m001_Claymore_RunStart_End_RootMonotonic.blend`、`README_RunStart_End.md`、`verification_RunStart_End.json`。工程停在 `m001_RunStart_End` 第 61 帧；此前 26 个 Action、五个交付 FBX 及六个源 FBX 的哈希均保留。
- 完整证据、编辑前备份及交付核对位于 `Saved/Blender/m001/20260914-125147/`；本次未执行 UE 导入、压缩或运行时验收。

用户查看新动画并反馈根速度下限或拟合效果；如需 UE 回导和运行验证，按具体授权推进。m001 尚未标记关闭。

### SprintStart 追加处理（2026-09-16）

- 用户要求 `AS_Vera_Claymore_SprintStart` 一起处理，归入 m001。源 FBX 保留，SHA-256 为 `b4c55881527210e334378837e78318c97e1e6a951199891bd76a1f020dfbebb9`。
- 60 FPS、1–20 帧、0.316667 秒，净位移 195.400751 cm；原轨迹只有最后一个区间停顿，前两个区间约 8.67 cm/s。沿用 RunStart 的 1 cm/s 下限并加入存储精度余量，保留主体加速；最大根调整 0.167449 mm，首末位置不变。
- 全部 131 根骨骼、38,739 顶点完成 39 个整帧/半帧修改前后及 FBX 回读对照。回读最低速度 1.004294 cm/s，无非正速度区间；最大骨骼世界位置误差 0.000238 mm，网格误差 0.000638 mm，线性矩阵差 0；原 Action 不变。
- FBX 保留 7300 Binary，九条平移曲线之外的 1,945 个对象内容一致。已交付 `G:\Workspace\AssetModified\m001\Output\AS_Vera_Claymore_SprintStart_RootMonotonic.FBX`，SHA-256 为 `ad8351a9e2ede8a357b92e3107db2cb35a229deefb28ea21b7ffa81d7c18df92`，与经回读验证的工作区输出一致。
- 同目录交付 `m001_Claymore_SprintStart_RootMonotonic.blend`、`verification_SprintStart.json`、`README_SprintStart.md`。证据与编辑前场景备份位于 `Saved/Blender/m001/20260916-SprintStart/`；现场停在 SprintStart 第 10 帧。
- 本轮 Blender 5.2.1 LTS、Add-on 1.6、协议 5，服务期望协议 7，实际调用成功；未升级插件。未执行 UE 导入、压缩或运行时验收，m001 保持进行中。本轮后累计七段修改副本。
