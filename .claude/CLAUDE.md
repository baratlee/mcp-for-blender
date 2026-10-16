# 本项目的本机记忆

仅与本项目（mcp-for-blender）相关的本机事实。带日期的均为观测值，以实查为准。

> **跨机器注意：** 本文件和 `PersonalDocs/` 里的绝对路径（`G:\Workspace\...`、`G:\baratli_BARATLI-PC1_4572\...`、`D:\Blender 5.2` 等）都是 BARATLI-PC1 上的值。换电脑时按实查替换，不要照用。素材目录和 P4 工作区不在 git 里，需要另行准备。

## MCP 客户端接入（2026-10-14 起）

- 仓库根目录的 `.mcp.json` 是项目级配置，随 git 共享。它声明 `blender` 服务端，启动命令是 `uv run --directory . mcp-for-blender`，跑本仓库源码，与本仓库插件版本一致；同时设了 `DISABLE_TELEMETRY=true`。
- 每台电脑首次在本仓库启动 `claude` 时，需要用户批准这个项目级服务端，批准前 `claude mcp list` 显示 `Pending approval`。
- Codex 有两层配置：
  - 项目级 `.codex/config.toml`（2026-10-15 加入，随 git 共享）：启动命令、环境变量与 `.mcp.json` 相同，两个文件要一起改。
  - 用户级 `~/.codex/config.toml`（只在本机）：同名的 `blender` 跑上游 PyPI 包 `blender-mcp`。
  - 未验证：Codex 是否加载项目级配置（可能要求先信任本项目），以及两层同名时哪层生效。用 Codex 前先实查。

## 改插件后的部署流程

Blender 只从自己的 `scripts\addons` 加载插件，不读本仓库。改完根目录 `addon.py` 后：

```bash
cp addon.py src/blender_mcp/bundled/addon.py && uv run mcp-for-blender install-addon
```

然后在 Blender 里把插件关掉再打开（或重启），再点 Start MCP Server。不要直接改 Blender 目录里的副本，下次 `install-addon` 会覆盖它。

## 联通性自检（不依赖 MCP 客户端）

对插件 socket 直接发 JSON 可绕过 MCP 服务端单测插件这一侧：`{"type":"ping"}` 应返回 `pong: True`，`{"type":"get_addon_info"}` 可读到 `protocol_version`（应等于 `addon_manager.EXPECTED_ADDON_PROTOCOL_VERSION`）。发命令前先确认 Blender 进程在运行且端口在监听（`Get-NetTCPConnection -State Listen -LocalPort 9876`）。

## 已核实的状态（BARATLI-PC1，2026-09-26）

- 插件端口 9876，监听 127.0.0.1；未设置 `BLENDER_PORT` / `BLENDER_HOST` 环境变量。
- 已装插件与仓库 `addon.py` 逐字节一致，协议版本 11，插件版本 1.7。
- 2026-10-14：Claude Code 原本没有配置 Blender MCP，已改为用 `.mcp.json` 接入（见上节）。服务端能独立完成 MCP `initialize` 握手；服务端到插件的完整链路仍未测过。
- uv 缓存中 `archive-v0/8-sKVQUpzFPgpIzt` 含 `__editable__.mcp_for_blender-2.1.0.pth`，是指向本仓库的开发模式安装，别清。

## LT009：人形动画编辑（2026-10-13 从 Sampler 迁入）

用 Blender MCP 修改 UE 导出的人形动画 FBX。用户提到 LT009、m###、根运动、步幅、停步动画时，先读 `PersonalDocs/LT009/` 下的文档（`PersonalDocs/` 与 `.claude/` 的记忆一样随 git 纳入版本库，规则见 `.gitignore` 末尾）：

| 文件 | 用途 |
|---|---|
| `LT009_task.md` | 入口：范围、子任务索引、待办 |
| `RootMotionRetiming.md` | 方法：术语（第 0 节为准）、模式 A／B、合同模板、流程、反面教训 |
| `AnimEditQuality.md` | 质量判定：可程序化检查与阈值（硬性） |
| `Context.md` | 工具链：目录约定、导入导出、实现、验证、MCP 经验 |

- 只编辑人形或类人形动画；每次编辑都必须满足 `AnimEditQuality.md`，交付前附检查报告（检查脚本未实现前，手动核对其第 2～4 节硬性项）。
- 改根运动节奏的需求，按 `RootMotionRetiming.md` 选模式、填合同，不重新讨论方法。
- 子任务 `m###` 新建前查重。m001、m002 成果物已过时（2026-10-14），不跟进、不复核，文档只作历史与方法来源；`CodexArchive/` 同样只作参考。
- 素材：`G:\Workspace\AssetModified\m###\{Input,Work,Output}`。Input 只读，中间产物进 Work，验证通过才进 Output。
- Blender／FBX 通过不代替 UE 验收；门禁文档 `G:\baratli_BARATLI-PC1_4572\Sampler\Docs\Testing\AnimationTestAcceptance.md`。
