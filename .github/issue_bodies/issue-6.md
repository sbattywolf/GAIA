Scaffold and run `alby_agent` dry-run prototype to validate doc merges and event emission without side-effects.

Tasks:
- Add `--dry-run` flag to `agents/online_agent.py` and ensure local-only mode.
- Wire event outputs to local `events.ndjson` for review.
- Metrics: measure timings and record traces in `gaia.db`.

Priority: high
Est hours: 16
Scrum points: 8
