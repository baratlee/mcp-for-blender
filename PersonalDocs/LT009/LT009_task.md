---
name: task-lt009-blender-maintenance-development
description: LT009——Blender 相关事项、工具开发与工作流维护
metadata:
  node_type: memory
  type: project
  task_id: LT009
  status: active
  modified: 2026-10-14
---

# LT009 Blender 相关事项与开发维护

> **迁移说明（2026-10-13）**：本文从 Sampler 工程 `PersonalDocs` 迁入本仓库，Sampler 侧已删除。
> - `Saved/Blender/m001/…` 证据目录已删除，文中路径仅作历史记录。
> - 文中“Codex”是早期的执行者记录。

## 目标与边界

- 长期伞形任务：Blender 问题调查、工作流维护、脚本／Add-on 开发、资产处理，以及与 Sampler 内容管线的协作。
- **动画编辑只针对人形或类人形角色**（用户 2026-10-14 要求）；非人形（四足、载具、道具等）不在本任务范围。
- **每次编辑都必须满足 [AnimEditQuality.md](AnimEditQuality.md) 的质量限制**，交付前附检查报告；脚本未实现前，至少手动核对第 2～4 节的硬性项。
- 具体事项提出时逐项登记；开始前先确认目标、影响范围和成功标准，不预设方案或交付物。
- Blender 工具侧、导出文件、UE／Sampler 内三层验证分别记录，不互相替代。
- 本任务不授权修改工程代码或资产、启动 Blender、批处理、编译、PIE、Automation 或 Perforce 操作，需按具体事项单独获得授权。

## 子任务索引

| 编号 | 内容 | 状态 |
|---|---|---|
| [m001](../m001/m001_ClaymoreStopAnimations.md) | 大剑起步／停步动画：根运动严格单调化（模式 A） | **已过时**：成果物不再使用、不再跟进 |
| [m002](../m002/m002_StopAnimations.md) | 系列停步动画调整（模式 B） | **已过时**：成果物不再使用、不再跟进 |

两者的方法与教训已提炼进 RootMotionRetiming；文档与素材保留作历史记录（2026-10-14 用户确认）。

- 根运动节奏类修改的方法（模式选择、合同模板、流程、反面教训）：[RootMotionRetiming.md](RootMotionRetiming.md)。新任务先按它定合同，不重新讨论方法。
- 动画编辑质量的可程序化判定（骨长、关节、承重脚、运动感）：[AnimEditQuality.md](AnimEditQuality.md)。检查脚本尚未实现。
- 工具链（导出、导入、实现、交付、验证门禁）：[Context.md](Context.md)。
- 素材目录：`G:\Workspace\AssetModified\m###\{Input,Work,Output}`，见 [目录约定](Context.md#目录约定2026-10-14-起)；m001、m002 已于 2026-10-14 迁入。

## 事项维护规则

- 每个事项记录目标、状态、相关文件、关键决策、验证证据和下一步。
- Blender 资源创作／修改使用小写 `m###` 编号，分配前查重；同一任务的追加资源归入原子任务。
- 其他工具维护事项保留稳定小节，只有形成独立长期责任时才新建 LT。
- 结论注明 Blender 版本、目标格式或运行环境等适用条件，不把版本相关行为当通用事实。

## 待办

1. 新的同类需求：分配新 m 编号，按 RootMotionRetiming 选模式、填合同。
2. 把 AnimEditQuality 的检查写成通用脚本；在首个案例上标定“待标定”阈值并回填文档。

## 环境与安装历史

2026-09-01 首次安装的是上游 `ahujasid/blender-mcp`，经 Codex 连接。安装时的状态：

| 项 | 当时的值 |
|---|---|
| Blender | `D:\Blender 5.2\blender.exe`，5.2.1 LTS |
| Add-on | `...\Blender\5.2\scripts\addons\blender_mcp.py`，版本 1.6，协议 5 |
| MCP 启动 | `uvx --python 3.11 blender-mcp`，`UV_PYTHON_PREFERENCE=only-managed`、`DISABLE_TELEMETRY=true` |
| Codex 配置 | `C:\Users\baratli\.codex\config.toml`，MCP 名 `blender` |
| 验证 | 持久启用、端口 9876 连接、只读场景查询与视口截图通过；场景写入未测 |

- m001 期间（至 2026-09-16）一直是 Add-on 1.6／协议 5；写入、保存、FBX 导出均已实际跑通。
- 据本仓库 `.claude/CLAUDE.md`，2026-09-26 已改用本仓库插件（版本 1.7，协议 11）。当前状态以实查为准。
- MCP 使用经验与坑见 [Context.md](Context.md#mcp-使用经验)。
