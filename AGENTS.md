# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Commands

pytest is not a declared dependency (not in `pyproject.toml` or `uv.lock`), so pull it in ad hoc:

```bash
uv run --with pytest pytest -q                                   # full suite
uv run --with pytest pytest tests/test_safe_mode.py -q           # one file
uv run --with pytest pytest tests/test_polyhaven.py::test_name   # one test
```

Run the server / CLI from the checkout:

```bash
uv run mcp-for-blender                  # MCP server over stdio (waits silently for a client)
uv run mcp-for-blender --port 9877      # --host/--port override BLENDER_HOST/BLENDER_PORT
uv run mcp-for-blender install-addon    # copy bundled addon.py into Blender's addons dir
uv run mcp-for-blender addon-paths      # list detected Blender addons dirs
```

There is no configured linter/formatter. The package was renamed from `blender-mcp` to `mcp-for-blender`; both names still appear intentionally for backward compatibility.

## Architecture

Two processes talk over a TCP socket (default `localhost:9876`) using plain JSON: request `{"type", "params"}`, response `{"status", "result" | "message"}`. There is no length prefix — the server keeps reading until the bytes parse as complete JSON.

1. **Blender addon** — `addon.py` (single ~6k-line file, runs inside Blender, imports `bpy`). `BlenderMCPServer` accepts connections on a background thread, but commands are pushed onto a queue and executed by one persistent `bpy.app.timers` callback on Blender's main thread (`_drain_command_queue`); `bpy` must never be touched from the socket thread. Dispatch is the `handlers` dict in `_execute_command_internal`; integration handlers (Poly Haven, Sketchfab, Poly Pizza, Hunyuan3D, Hyper3D, Tripo) are added only when enabled in the UI. Premium mode (`premium_active()`) reroutes 3D-generation calls to a hosted API instead of the user's own keys.
2. **MCP server** — `src/blender_mcp/server.py` (FastMCP). Each `@mcp.tool()` forwards to the addon via a single global `BlenderConnection`; `send_command` holds a lock across send+receive because responses are matched to requests purely by order on the stream.

### Addon ↔ server version coupling

- **`addon.py` exists twice**: repo root and `src/blender_mcp/bundled/addon.py` (the copy shipped in the wheel and installed by `install-addon`). They must be byte-identical — `tests/test_addon_manager.py` enforces it. Edit the root file, then copy it over the bundled one.
- `ADDON_PROTOCOL_VERSION` in `addon.py` and `EXPECTED_ADDON_PROTOCOL_VERSION` in `addon_manager.py` must be bumped together when the command surface changes. The server handshakes via `get_addon_info` on first connect.
- The server auto-updates through `uvx` but the addon only changes when the user reinstalls it, so new server tools/arguments must degrade cleanly against older addon protocols (see `_addon_protocol()` usage in `server.py` and `tests/test_addon_compat.py`).

### Cross-cutting server modules

- `telemetry_decorator.py` — `@telemetry_tool` / `@trajectory_tool` wrap tools (stacked under `@mcp.tool()`). Tools report failure by *returning* a string starting with `error`/`failed to` rather than raising; the decorator classifies results on that.
- `telemetry.py`, `trajectory.py` — usage telemetry and opt-in trajectory capture to Supabase. Consent lives in the addon preferences (off by default); `consent_prompt.py` asks once via MCP elicitation. `DISABLE_TELEMETRY=true` turns everything off.
- `safe_mode.py` — opt-in (`BLENDER_MCP_SAFE_MODE=1`) deny-by-default AST allowlist applied to `execute_blender_code` scripts *before* they reach the socket. It only guards the MCP path, not the addon socket itself.
- `premium_hint.py` — one-per-conversation Premium mention appended to generation status replies.

### Tests

Tests never run Blender. Addon behavior is tested by reading `addon.py` as source text (`tests/conftest.py` exposes `ROOT_ADDON`), and server tools are tested by monkeypatching `server.get_blender_connection` with a fake whose `send_command` records calls.
