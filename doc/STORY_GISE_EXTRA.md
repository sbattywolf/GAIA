**Gise — Extra: mapping and next tasks**

Summary:
- Gise composes agents and provides orchestration, scheduling, and enriched telemetry.

Files & mapping:
- `agents/sequence_worker.py` (exists) — worker pattern for composed runs.
- `agents/controller_agent.py` — coordinator for sequences.

Backlog items:
- Define a simple composition manifest format and a `gise_agent.py` prototype.
- Add trace correlation for composed runs (trace_id linking events and db rows).

Acceptance tests:
- Run a composed task and ensure events include a `trace_id` present across steps.

Next step:
- Scaffold `gise_agent.py` and a sample composed manifest under `examples/`.
