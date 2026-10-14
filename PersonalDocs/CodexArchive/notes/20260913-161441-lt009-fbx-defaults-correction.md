# 更正：LT009 的 UE 动画序列 FBX 导出默认参数

用户于 2026-09-13 明确更正：「撤销，我说错了是LT009」。

此更正取代 20260913-161301-lt090-ue-fbx-to-blender-defaults.md 中的任务编号和编号差异说明：撤销 LT090 归属及检索别名，正确且唯一的归属为 LT009（Blender 相关事项与开发维护）。编号已由用户澄清，不再记录为待确认。保留用户要求记忆的 FBX 参数，不撤销参数本身。

工程：G:\baratli_BARATLI-PC1_4572\Sampler。
适用范围：UE 单个 Animation Sequence 导出 FBX，导入 Blender 查看或编辑动画。

| FBX Export Options 选项 | LT009 工作流默认值 |
|---|---|
| FBX Export Compatibility | FBX 2013 |
| ASCII | 不勾，使用 Binary |
| Export Preview Mesh | 勾选，把人物模型一起导出 |
| Level Of Detail | 不勾 |
| Force Front XAxis | 不勾 |
| Map Skeletal Motion to Root | 不勾 |
| Export Morph Targets | 普通身体动画不勾；需要表情或形变时勾选 |
| 其余选项 | 保持默认 |

明确只需要纯骨骼动画时可关闭 Export Preview Mesh。Map Skeletal Motion to Root 不因动画带 Root Motion 而自动开启。这是用户确认的工作流默认参数，不是所有 FBX 导出的通用设置；本次仅更正记忆，无 UE/Blender 设置变更，也无实际 FBX 导入或往返验证。
