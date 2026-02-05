**Scheduler — Story**

Overview:
- Purpose: schedule recurring or delayed agent runs (cron-like) and emit schedule events to the system.

Backlog mapping:
- Not yet present; scheduler responsibilities include triggering `agents/` runs, recording schedules in simple JSON, and emitting scheduled-run events.

Acceptance criteria:
- A lightweight scheduler process or CLI that reads a schedule file, triggers agent tasks, and records traces in `gaia.db` and `events.ndjson`.
- Respect safety policy: scheduled actions requiring execution must still pass through approval if policy requires it.

Next steps:
- Prototype `scripts/simple_scheduler.py` that can run in the background and invoke agents by CLI with `--dry-run` by default.
- Add tests for schedule parsing and trigger logic.
