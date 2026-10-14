# 用户确认的 UE 动画序列 FBX 导出默认参数（用于 Blender）

- 更新类型：新增用户偏好；用户于 2026-09-13 明确要求将本轮建议保存为默认参数。
- 工程：G:\baratli_BARATLI-PC1_4572\Sampler。
- 任务标识：按用户最新原文记为 LT090。此前对话及当前工程台账中的 Blender 任务为 LT009，台账未找到 LT090；保留这一编号差异，不据此创建、改号或重编号长期任务。检索 LT090、LT009、UE 导出动画到 Blender、FBX Export Options 时应能找到此约定。
- 适用范围：从 UE 导出单个 Animation Sequence 为 FBX，导入 Blender 查看或编辑动画。不能将此约定扩展为所有 FBX 场景、静态模型或 Sequencer 导出的通用默认值。

| FBX Export Options 选项 | 用户确认的工作流默认值 |
|---|---|
| FBX Export Compatibility | FBX 2013 |
| ASCII | 不勾，使用 Binary |
| Export Preview Mesh | 勾选，把人物模型一起导出，方便在 Blender 观察动作 |
| Level Of Detail | 不勾 |
| Force Front XAxis | 不勾 |
| Map Skeletal Motion to Root | 不勾 |
| Export Morph Targets | 普通身体动画不勾；需要表情或形变时勾选 |
| 其余选项 | 保持默认 |

补充：只有明确需要纯骨骼动画、无需附带人物模型时，才关闭 Export Preview Mesh。Map Skeletal Motion to Root 用于将 Actor 运动映射到根骨骼，不应仅因为动画带 Root Motion 而开启。

这是用户确认的工作流偏好，不等同于 UE 所有选项的出厂默认值。UE 导出窗口会记住上次设置，使用时应核对上述项目。本次仅记录参数，未修改 UE/Blender 设置；这组参数尚无本轮实际 FBX 导入或往返验证证据。
