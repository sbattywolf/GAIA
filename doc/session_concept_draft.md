## Session Concept Draft — Stabilize Auto-Mode & Approval Flow

Goal
----
- Produce a minimal, safe, auditable automation stack for this session that: enforces a kill-switch for autonomy, ensures secret-loading for background runners, and makes approval request/ack behavior deterministic and traceable.

Scope
-----
- Enforce `.tmp/autonomous_mode.json` as the single source-of-truth for enabling autonomous actions.
- Ensure `scripts/env_loader.py` is called by background runners to load `.private/.env` secrets.
- Standardize approval events to include `request_id` and `trace_id`; make `approval.received` include `request_trace`.
- Provide an extractor and unit tests that reliably pair `approval.request` → `approval.received` and produce ack artifacts.

Components
----------
- Runner guard: small helper that aborts action if `.tmp/autonomous_mode.json` shows `autonomous: false`.
- Env loader: existing `scripts/env_loader.py` — ensure invoked from runners and watchdogs.
- Approval schema: update emitters and listeners to include `request_id` and `request_trace` fields.
- Ack generator: create ack files under `.tmp/approval_ack_{request_id}.json` (idempotent).
- Observability: write audit rows to `gaia.db` and append `events.ndjson` entries for major state changes.

Acceptance Criteria
-------------------
1. Background runners never perform external actions unless `.tmp/autonomous_mode.json` explicitly enables autonomy.
2. Approval extractor pairs requests with receipts deterministically (unit tests pass).
3. Missing acks can be auto-created and will produce `approval.ack.created` audit events.
4. Telegram notifications remain queued when credentials are absent; will send when `.private/.env` contains tokens and `ALLOW_COMMAND_EXECUTION=1`.

Next Steps (Implementation Plan)
--------------------------------
1. Add a small `guard_autonomy()` helper and call it at the start of `scripts/gise_autonomous_runner.py` and `scripts/automation_runner.py` (T1).
2. Patch runners to call `scripts/env_loader.py` before any side-effecting actions (T2).
3. Update approval producers to attach `request_id` and `trace_id` (T3).
4. Add unit tests under `tests/test_approval_extractor.py` (T5).
5. Wire audit writes to `gaia.db` where appropriate (T7).

Short-term Timeline
-------------------
- Day 0 (this session): implement guard (T1), patch runner to call env_loader (T2), run dry-run (no external calls).
- Day 1: finalize approval schema (T3), implement tests (T5), persist audit writes (T7).

Risks & Mitigations
-------------------
- Risk: accidental external actions — Mitigation: conservative default (`autonomous: false`) and require explicit `ALLOW_COMMAND_EXECUTION`.
- Risk: leaked secrets — Mitigation: `.private/.env` remains gitignored; add scanner for accidental commits.

Trace
-----
- Linked session sprint: session_sprint_20260205T092742Z.json
- Todo list: .tmp/todolist_session_20260205T094000Z.json
