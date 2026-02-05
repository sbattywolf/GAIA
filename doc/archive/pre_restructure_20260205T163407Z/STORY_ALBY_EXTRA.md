**Alby — Extra: mapping and next tasks**

Summary:
- Alby is the agent runtime pattern: CLI-first agents under `agents/` that append NDJSON events and audit traces.

Files & mappings:
- `agents/backlog_agent.py` — canonical agent example (creates GitHub issues via `gh` and appends events).
- `agents/` — other small agents; `agents.json` contains agent metadata.

Backlog items:
- Standardize agent template and helper utilities (append_event, write_audit). Add `agents/README.md`.
- Local harness to run agents with `--dry-run` and `--exec` flags.

Acceptance tests:
- Agents append expected events to `events.ndjson` and write audit rows to `gaia.db` when run in dry-run and exec modes.

Next step:
- Create `agents/README.md` with template and example usage.
