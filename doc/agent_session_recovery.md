Session sync note: single source of truth
- On startup, the agent will load `gaia.db` and prefer `backlog` table contents for runtime decisions. If `gaia.db` is missing, the agent will create it and import `doc/todo-archive.ndjson` as the initial state using `agents/sync_backlog_to_db.py`.
- After import, agents must write a `recovery.sync` event to `events.ndjson` and an `audit` row to `gaia.db` with details of the import (rows imported, timestamp, trace_id).
# Agent Session Recovery & Lifecycle (GAIA)

Purpose
- This document defines the session lifecycle, how agents persist progress, and the recovery/resume procedure after hangs, crashes, or restarts. It is the single authoritative doc agents should read to determine initialization and end-of-session steps.

Scope
- Startup initialization
- Persistent session state format
- Decision rules for resume vs rollback vs manual checkpoint
- Cleanup rules for background processes and external side-effects
- Restore procedure and verification checks
- Training checklist for agents/operators

Files of interest
- `.copilot/session_state.json` — session state persisted by agents
- `events.ndjson` — append-only event log for audit and reconciliation
- `gaia.db` — SQLite audit DB created by `orchestrator.py`
- `doc/todo-archive.ndjson` — machine backlog state
- `MASTER_BACKLOG.md` — human-readable consolidated backlog

Session state schema (recommended)
- `current_task_id`: str | null
- `steps_completed`: list[str]
- `next_immediate_step`: str | null
- `last_sync`: ISO8601 UTC timestamp
- `trace_id`: uuid
- `process_map`: dict — mapping of step -> process metadata { pid, cmd, started_at, stdout_path, stderr_path }
- `events_cursor`: int — byte offset in `events.ndjson` last processed
- `notes`: optional free-text

Agent behavior (on normal operation)
1. At startup, agent writes a `session.start` trace to `events.ndjson` and `gaia.db`.
2. Before executing a step, agent records the step id and process metadata into `.copilot/session_state.json` and writes an `action.started` trace.
3. On step completion, write `action.completed` trace and mark `steps_completed`.
4. Persist state after every step (atomic write to `.copilot/session_state.json`).

Crash / hang detection
- Monitor last `last_sync` timestamp; if older than configured threshold (e.g., 5 minutes for interactive tasks, 30 minutes for batch), mark session as `stale` and begin recovery checklist.

Recovery decision matrix (high-level)
- If last action is `completed`: resume at next step.
- If last action is `started` and `process_map` lists a running PID:
  - Query process health. If process still alive, determine if it is idempotent or has external side-effects.
  - If external side-effects unknown or irreversible, create `CHECKPOINT_<n>.md` and require human approval before destructive rollback.
  - If idempotent and safe, re-run the step or wait for PID to finish (configurable).
- If `process_map` contains failed/terminated processes: examine logs and `events.ndjson`, then decide to retry, rollback, or manual inspect.

Rollback vs resume rules
- Prefer non-destructive resume by default.
- For operations that modify remote state (API calls, DB migrations, token rotations): require explicit checkpoint approval before rollback or replay that may duplicate side-effects.
- For local-only operations (file writes, tests): safe to re-run after cleaning temporary artifacts.

Recommended recovery steps (automated)
1. Read `.copilot/session_state.json` into memory.
2. Lock the agent (create `.tmp/agent_recovery.lock`) to avoid concurrent recovery runs.
3. For each `process_map` entry:
   - Check PID; if running and marked `detachable`, either leave running and record state, or kill if `orphanable` is false.
   - For long-running external requests, attempt to query remote endpoint to know current status (idempotency key recommended).
4. Reconcile `events.ndjson` from `events_cursor` to end — build a short timeline and write `recovery.timeline` to `.tmp/`.
5. If any step has external side-effects and no checkpoint found, create `CHECKPOINT_<n>.md` with summary and set recovery to `awaiting-approval`.
6. If safe to resume, update `.copilot/session_state.json` `last_sync`, set `next_immediate_step` and proceed.
7. Write `session.recovered` trace to `events.ndjson` and `gaia.db` with `status: ok|manual-review|required-rollback`.
8. Remove `.tmp/agent_recovery.lock`.

Manual operator checklist (if recovery requires human action)
- Inspect `.tmp/recovery.timeline` and recent traces in `gaia.db`.
- Read `CHECKPOINT_<n>.md` and confirm whether to `rollback`, `continue`, or `abort`.
- If rollback: list the rollback steps in the checkpoint, run them in dry-run first, then execute.

Agent training / procedures to create backlog items and resume
- To create a backlog item: append NDJSON line to `doc/todo-archive.ndjson` with required fields (`id`, `title`, `status`, `priority`, `est_hours`, `added_at`).
- To mark progress: update the NDJSON by appending a corrected line with same `id` and new `status` (machine consumers should read the latest line per id), or prefer a small helper script `agents/update_todo.py` to perform atomic updates.
- To resume after crash: run `python scripts/restore_session.py --session-state .copilot/session_state.json` (script to be implemented) which will follow the automated recovery steps above.

File integrity & log cleanup
- On recovery, if written files are suspected corrupt, run integrity checks (hash compare to backups) or move suspect files to `.tmp/corrupt/` and mark for manual review.
- Keep logs in `.tmp/logs/` with timestamps; do not truncate until manual review confirms no needed data.

Audit & Trace
- Every recovery action must be traced into `gaia.db` for postmortem.
- Include `trace_id` in traces so operations can be correlated across services.

Examples & quick commands
- Dump session state:
```powershell
python - <<'PY'
import json
print(json.dumps(json.load(open('.copilot/session_state.json')), indent=2))
PY
```
- Show last 200 events:
```powershell
Get-Content events.ndjson -Tail 200
```

Open items & future work
- Implement `scripts/restore_session.py` and a helper `agents/update_todo.py`.
- Add idempotency keys to all external requests in agent code.
- Provide automated `CHECKPOINT` generator for potentially destructive flows.

---

Maintainer: GAIA Agent — update this doc when process or file locations change.
