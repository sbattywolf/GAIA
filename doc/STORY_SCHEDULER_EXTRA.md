**Scheduler — Extra: mapping and next steps**

Summary:
- Scheduler responsibilities: schedule recurring/delayed agent runs and emit schedule events.

Backlog items:
- Prototype `scripts/simple_scheduler.py` that reads `schedules.json` and triggers agents in `agents/` via CLI in dry-run mode.
- Add tests for schedule parsing and trigger behavior.

Acceptance tests:
- Scheduler triggers a scheduled run and produces `events.ndjson` entries with `type: schedule.triggered` and correlating `trace_id`.

Next step:
- Scaffold `scripts/simple_scheduler.py` and a sample `schedules.json` in `examples/`.
