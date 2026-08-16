# Zeus Local AI Framework - Master Guide v3

Updated 30 July 2026 from the full implementation history.

This package is documentation and a continuation handover. It does not replace the repository runtime files.

## Confirmed architecture

- Raspberry Pi 4: Home Assistant, kept separate.
- GTX 1070 Ubuntu: Zeus Edge always-on, Telegram, deterministic routing, Home Assistant access and local Ollama fallback.
- RTX 3090: future Zeus Brain for software coding, Home Assistant engineering, dashboards, automation analysis, Open WebUI and carefully evaluated MCP.
- QNAP: optional future backup/log/artefact store, never a synchronous dependency of Zeus Edge.

## Current result

Milestone 1 and Milestone 2 have been implemented and validated with unit tests and Telegram tests. Zeus answers the supported deterministic queries quickly. The next planned work is Milestone 3: read-only inventory plus Home Assistant areas, aliases and labels.

Read in order:

1. `docs/00_CURRENT_STATE.md`
2. `docs/01_ARCHITECTURE_AND_DECISIONS.md`
3. `docs/02_ROADMAP_1070.md`
4. `docs/03_HOME_ASSISTANT_LABEL_PILOT.md`
5. `docs/04_OPERATIONS_AND_RECOVERY.md`
6. `docs/05_REMOTE_WORK_AND_WORK_DEVICE_BOUNDARY.md`
7. `prompts/NEXT_AGENT_PROMPT_M3.md`
