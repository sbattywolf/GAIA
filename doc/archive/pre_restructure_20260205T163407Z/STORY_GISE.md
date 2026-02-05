**Gise — Story (reference: Gise 0.3)**

Overview:
- Purpose: a higher-level orchestration agent that composes smaller agents (Alby-style) and provides policy, scheduling, and enriched telemetry.

Backlog mapping:
- `agents/` contains simple agents; Gise is the composition layer and may host worker loops and scheduled tasks.
- Features: traceable runs, per-agent configuration, and safe tool access.

Acceptance criteria:
- Ability to declare and run composed tasks locally.
- Trace and event correlation in `events.ndjson` and `gaia.db`.
- Configurable safety policy (who can approve/trigger actions), and integration hooks to the Telegram approval flow.

Next steps:
- Design a minimal `gise_agent.py` that can schedule or trigger Alby agents and append composed events.
- Add configuration schema for agent composition and per-agent permissions.
