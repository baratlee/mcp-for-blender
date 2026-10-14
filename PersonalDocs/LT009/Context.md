# LT009 上下文：Blender 动画资源与 FBX 工作流

> **迁移说明（2026-10-13）**：本文从 Sampler 工程 `PersonalDocs` 迁入本仓库，Sampler 侧已删除。
> - `Saved/Blender/m001/…` 证据目录已删除，文中路径仅作历史记录。
> - 文中“Codex”是早期的执行者记录。

内容更新至 2026-09-20，2026-10-14 整理结构。子任务状态见 [LT009 任务索引](LT009_task.md#子任务索引)。

## 恢复顺序

1. 入口是 [LT009_task.md](LT009_task.md)；改根运动节奏的任务先读 [RootMotionRetiming.md](RootMotionRetiming.md)，再按需查本文。
2. m001、m002 已过时；需要查历史实施细节时再打开它们的文档。
3. 用只读调用核对 Blender 连接、版本和当前场景；场景、连接和文件内容都会变化，不能把上次快照当作现状。

## 目录约定（2026-10-14 起）

素材目录按 m 编号组织，与 `PersonalDocs/m###/` 一一对应：

```
G:\Workspace\AssetModified\
└─ m###\
   ├─ Input\    原始 FBX 与参考 FBX；放入后只读，不写回
   ├─ Work\     中间产物：候选 .blend、试导出 FBX、验证 json，按 <时间戳>\ 分批
   └─ Output\   验证通过的交付 FBX，及同名 .blend、README、verification
```

- 重做时覆盖 Output 中的同名文件（用户明确不要 V2 文件名），覆盖前把旧版备份到 `Work\`。新任务文件名为 `<源主名>_m###.FBX`（用户 2026-10-14 确认）；m001 沿用 `_RootMonotonic`。
- 只有通过 FBX 回读并核对哈希的文件才进 `Output\`。
- 2026-10-14 已把旧目录 `1\`、`2\` 迁入新结构（84 个文件，迁移前后 SHA-256 一致）：

| 子任务 | 旧位置 → 新位置 | 备注 |
|---|---|---|
| m001 | `1\` 根目录 → `m001\Input\`；`1\RootMonotonic\` → `m001\Output\` | 交付沿用 `_RootMonotonic` 后缀；`RunLeftStop.zip` 是两段 Run Stop 源 FBX 的压缩包，归 Input；`m001\Work\` 未建 |
| m002 | `2\` 根目录 → `m002\Input\`；`2\m002\<时间戳>\` → `m002\Work\<时间戳>\` | 历史 v002 `_m002.FBX` 移到 `m002\Work\`；`Output\` 为空 |

- 文档里旧的 `1\`、`2\` 路径已改。交付目录里的 README、verification、`.blend` 内部记录仍是旧路径，按历史记录看待。

## 修改方法

根运动节奏类修改（m001、m002 及以后同类任务）的方法、模式选择、合同模板和反面教训，统一见 [RootMotionRetiming.md](RootMotionRetiming.md)。本文只管工具链：导出、导入、实现、交付和验证。

## UE 导出到 Blender：LT009 默认值

仅适用于 UE 单个 Animation Sequence 导出 FBX 供 Blender 编辑；是用户确认的工作流默认值，不是软件出厂默认值，不扩展到静态模型或 Sequencer。

| FBX Export Options | 工作流默认值 |
|---|---|
| FBX Export Compatibility | FBX 2013 |
| ASCII | 关闭，使用 Binary |
| Export Preview Mesh | 开启（明确只要纯骨骼动画时可关） |
| Level Of Detail | 关闭 |
| Force Front XAxis | 关闭 |
| Map Skeletal Motion to Root | 关闭，不因动画含 Root Motion 自动开启 |
| Export Morph Targets | 普通身体动画关闭；需要表情／形变时另定 |
| 其余选项 | 保持默认 |

- 导出窗口会记住上次设置，逐项核对。
- 说明 UE 回导参数前，先核对 Sampler 同级自研 Engine 的实际版本、Interchange／Legacy 路径和真实属性名，不混用其他版本界面。

## Blender 导入与结构核对

m001 时期验证的环境：Blender 5.2.1 LTS、Add-on 1.6、协议 5（当前插件版本见 LT009_task“环境与安装历史”）。数据集为 60 FPS、METRIC、`scale_length=1`。

```python
bpy.ops.import_scene.fbx(
    filepath=source_path,
    use_anim=True, anim_offset=1, global_scale=1,
    use_manual_orientation=False,
    automatic_bone_orientation=False,
    ignore_leaf_bones=False,
    bake_space_transform=False,
)
```

其余参数用操作器默认值；上面的显式参数不都是“非默认”。换版本时查实际 RNA 默认值和源码。

- 每个输入放独立场景；先备份当前 `.blend`，记录既有 Action 与输入／交付文件哈希。
- 本组骨架：一个 Armature、一个 Mesh，131 根非根骨骼、38,739 顶点。根骨 `Root_M` 是 Armature 对象（见术语表），只查 `pose.bones` 会误判为没有根运动。
- 根对象缩放 0.01，无父级、约束、Driver、NLA，旋转／缩放恒定。这些是复用补偿脚本的前提，不可推广到任意骨架。
- 区分 Blender 米、FBX 厘米与 UE 坐标约定，避免多乘 100 或翻错轴。
- 时长按实际关键帧算：`(last-first)/fps`，不是帧数除以 fps。FBX 时间单位为 46,186,158,000 ticks/s。
- 本组源 FBX 的 Take 声明都比实际末键短一帧：保留全部实际帧，导出时把 Take 对齐末键并记录差异，不裁尾帧。其他来源要重新核对。

## 模式 A 实现：根运动单调拟合与补偿

约束与参数取值见 [RootMotionRetiming.md](RootMotionRetiming.md) 第 3、5 节。逐帧线性插值，不承诺速度／加速度连续。

入口：[root_monotonic.py](../m001/scripts/root_monotonic.py)。先核对源码和适用条件再执行；脚本默认 `MIN_SPEED=0.01`，收尾段由调用方显式设为 0.1。

- 算法（单调回归）见 RootMotionRetiming 第 5 节；这里只记实现细节。
- 复制原 Action，只改根与 `Bip001`、`ik_root` 的 XYZ 共九条平移曲线；原 Action 用 fake user 保留并核对哈希。
- 补偿公式 `P_new = inverse(A_new) * A_old * P_old`，显式处理根的旋转／缩放和骨骼参考姿势；最终以求值后的世界骨骼矩阵和变形网格为准。
- 侧向偏离实测：SprintLeftStop 0.7515 mm（允许 1 mm），RunStart_End 6.8413 mm（允许 10 mm）。它与世界姿态误差容差是两个约束。
- 存储精度余量用 `account_for_storage_precision=True` 打开。
- 分层 Action 按 `layers → strips → channelbags → fcurves` 读取；切换 Action 时同时设置 slot。

## FBX 导出与交付

1. 在工作区生成并验证新文件，保留原始输入。标准 Blender 导出探针在 m001 曾产生约 0.026 mm 回读误差（超过 0.01 mm 容差），“导出成功”不等于正确交付。
2. 采用 `export_preserved_fbx`：以原 FBX（或哈希一致的副本）为底，保留 7300／FBX 2013 Binary、骨架、蒙皮和其他曲线，只转写改过的曲线并对齐时间范围。m001 只转写九条平移曲线，其余 1,945 个对象逐一核对一致；模式 B 会改旋转曲线，该导出方式尚未在模式 B 上验证。
3. 写入前明确输入副本与输出的绝对路径，输出限定在工作区，验证通过后才复制到交付目录。覆盖前保留旧副本；遇只读属性就报告，不强制清除。
4. 同步可编辑 `.blend`、README 和验证报告，报告注明文件哈希和证据目录；旧报告标明历史范围。
5. 自动审批曾把“验证 + 导出”合并调用误判为覆盖源文件：拆成两步，用哈希一致的工作区副本和明确的新输出路径，不绕过审批。

## 验证与交付判定

**通用**

- 在每个整帧和半帧对照全部世界骨骼矩阵与最终变形网格（含盆骨、实体脚、IK 分支），不只看局部 FCurve 或单根骨骼。
- 回读：最终 FBX 重新导入隔离场景，与导出前已验证的 Blender 结果对照。每段分别记录修改前后、FBX 回读、文件交付三层证据。
- 原 Action 哈希不变，帧范围不变。

**模式 A 额外要求**

- 修改后的世界姿态应与原动画相同；m001 容差为世界位置 `1e-5 m = 0.01 mm`、世界矩阵线性部分 `1e-6`。
- 首末根位置不变，投影速度正且有限。

**模式 B**

- 身体与腿按合同修改，不与原动画比世界姿态；按 RootMotionRetiming 第 7 节做姿态合理性检查，并确认只有合同允许的曲线变化。

**交付与边界**

- 复制到交付目录后核对 SHA-256 与已验证输出一致，并直接解析交付 FBX 的根曲线、时间和速度。修改时间、`.blend` 已保存、复制成功都不足以证明交付正确。
- 以上只裁决 Blender／FBX 局部合同，不证明 UE 压缩、Root Motion 提取、Mover／Actor／Capsule 消费、碰撞、混合或运行时滑步。UE 验收按 [动画测试门禁](G:/baratli_BARATLI-PC1_4572/Sampler/Docs/Testing/AnimationTestAcceptance.md)，需用户授权。

## MCP 使用经验

- 新一轮先用只读调用核对连接和版本。同一时刻只运行一个连接该 Add-on 的 MCP 客户端。
- 后台模式（`--background`）的 Blender 不运行 Add-on 的 socket 服务，端到端验证要用 GUI 进程。
- `execute_blender_code` 能执行任意 Python：写操作前保存场景并限定目标。撤销链路未完整验证，所以保留编辑前 `.blend` 和原 Action。
- `execute_blender_code` 的 `user_prompt` 传用户当前目标原文，拆步骤时不替换成自己的子目标。
- 持久模块放进 `bpy.app.driver_namespace`；不要假定上次调用的顶层变量还在，每次显式导入所需模块。
- 调整视口后先 `region_3d.update()` 再截图；居中用最终变形顶点的包围盒，不用未变形网格中心。
- 环境有 NumPy，没有 SciPy／Matplotlib；现有拟合不依赖后两者。
- PowerShell 读 JSON 注意 UTF-8 BOM；`foreach` 聚合结果先赋变量再转 JSON。
- 遥测：MCP 进程的 `DISABLE_TELEMETRY=true` 当时没有关掉 Add-on 的 `telemetry_consent`，以运行时返回值为准。

### 未实施

- Blender 内 Codex 聊天面板（经 `codex app-server` + Blender MCP，接口标注 experimental）：2026-09-14 只讨论过方案，未开发、未安装、未验证。
