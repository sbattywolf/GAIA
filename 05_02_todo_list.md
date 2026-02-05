# Consolidated TODOs — snapshot

Source: aggregated from `tasks/todo.json`, `backlogs/todolist_rebuild_*.json`, `doc/archive/*` task lists, and repository TODO markers (tests/scripts).

This file is intended as a single, human-friendly snapshot of completed vs open work items and inferred actionables from code/tests. Items are grouped: 1) Completed (most-recent first as available), 2) Open — ordered by priority (critical → high → medium → low), 3) Inferred/enrichment from code & tests. Each item includes a short source pointer where available.

## A — Completed (selected, most-recent-visible first)
- Remove leaked token occurrences — completed. (source: `tasks/todo.json` id:4)
- Open PR to fix CI workflow — completed. (source: `tasks/todo.json` id:9)
- Patch CI to write .pth to user site-packages — completed. (source: `tasks/todo.json` id:11)
- Replace heredoc with helper script — completed. (source: `tasks/todo.json` id:12)
- Finalize external/openclaw conversion / add reuse docs / add README — completed. (source: `tasks/todo.json` ids:13,14,17)

## B — Open / Pending (ordered by priority)

Critical
- MANDATORY: Final governance checks and closure (collect chat history and all docs; attach evidence and close story). (source: `doc/archive/EPC_Telegram.current*.archived`, id: `t_final`) 

High
- Run acceptance scenario: create claim → approve → archive event; record gaia.db traces. (source: `doc/archive/EPC_Telegram.current*.archived`, id: `t2`) 
- Implement mocked Telegram API harness for CI/local tests (helps integration tests / idempotency). (source: `doc/archive/EPC_Telegram.current*.archived`, id: `t17`)
- Add integration test exercising approval listener → UI → approve → claim_cli flow. (source: `doc/archive/*`, id: `t18`)
- Add idempotency and replay tests for integration flows. (source: `doc/archive/*`, id: `t19`)
- Add automated tests for TTL expiry and takeover semantics; finalize `CLAIM_DEFAULT_TTL`. (source: `doc/archive/*`, id: `t22`)
- Map HTTP error codes for retryer and implement exponential backoff with jitter; add tests for 429/5xx. (source: `doc/archive/*`, ids: `t23`,`t24`,`t25`)
- Design and run `alby_agent` prototype in dry-run to automate merges/archives/validation/tests, then collect metrics. (source: `doc/archive/*`, ids: `t38`–`t42`)

Medium
- Add unit tests for approval extractor and ensure deterministic approval matching. (source: `backlogs/todolist_rebuild_*.json` T5, code: `scripts/approval_extractor.py`)
- Add counters and persist metrics to `.tmp/metrics.json` and wire alerts to `gaia.db`. (source: `doc/archive/*`, ids: `t26`,`t27`,`t28`)
- Implement scripts/backup_tmp.py and retention/cleanup scripts. (source: `doc/archive/*`, ids: `t32`,`t33`)
- Add verbose debug logging for claim acquisition (temporary) and helper to export chat history to `.tmp/exports`. (source: `doc/archive/*`, ids: `gd1`,`gd2`)
- Ensure env_loader is used by background jobs and schedule smoke tests. (source: `backlogs/todolist_rebuild_*`, T2, T1)

Low
- Populate CLI examples in doc/STR_Telegram.current#CLI-Examples and release checklist updates. (source: `doc/archive/*`)

## C — Inferred / Enrichment (items found in code, tests, templates, and archive notes)
- Run full `pytest -q` locally and in CI, collect failing tests and flip failing flaky tests to stable; add retry or fix root causes. (inferred from many new tests and CI changes)
- Add secret scanning with `detect-secrets` and pre-commit hooks; update `.secrets.baseline`. (matches existing task in `tasks/todo.json` id:5)
- Create `.env.template` and document `.tmp/telegram.env` handling and permissions. (source: `doc/archive/*`, id: `t12`, `t11`)
- Add CLAIM_DEFAULT_TTL env and tests; document tradeoffs. (inferred & archived) 
- Wire `gaia.db` audit traces for UI-initiated actions (requeues, approvals). (inferred from orchestrator and tests)
- Add monitor UI page for permanent-failed entries and one-click requeue protected by token/approval. (archived tasks)

## D — Sources scanned (high-level)
- `tasks/todo.json` — workspace todo list (primary).
- `backlogs/todolist_rebuild_20260205T101500Z.json` — rebuilt todo list snapshot.
- `doc/archive/` — many archived task lists and JSON task arrays (EPC_Telegram.*, EPC_Telegraf.*, STR_TestGise.*) — rich source of prioritized work items.
- `doc/05_backlog/` — consolidated backlog files and INDEX.
- grep scan for `TODO`/`todo` markers across repo (tests, scripts, templates) — used to infer missing test and CI work.

## E — Next actions I can take (suggested)
1. Normalize all todo items into a single NDJSON file `doc/todo-archive.ndjson` with fields: id, title, description, status, priority, source, created_at. (recommended)
2. Create GitHub issues for critical/high items not yet tracked as issues (optionally in batches).
3. Open PR to add `05_02_todo_list.md` (I will commit & push now). 

---
Generated: 2026-02-05T (local snapshot)
