**Alby — Story (reference: Alby 4)**

Overview:
- Purpose: agent runtime and orchestration layer for lightweight automations and integrations (inspired by Alby 4 design).

Backlog mapping:
- Agents live under `agents/` (example `agents/backlog_agent.py`).
- Key features: CLI-first agents, NDJSON event emission, optional external calls (e.g., `gh`).

Acceptance criteria:
- Standardized agent interface: parse args, perform action, append to `events.ndjson`, write audit to `gaia.db`.
- Safe dry-run mode and explicit flags for external side-effects.
- Local harness to run agents with env loading and sandboxing.

Next steps:
- Document common agent utilities and example templates in `agents/README.md`.
- Implement agent harness CLI to run agents with `--dry-run` and `--exec` toggles.
