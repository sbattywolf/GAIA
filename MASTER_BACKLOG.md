# MASTER BACKLOG (canonical)

This is the canonical MASTER_BACKLOG for the repository. It consolidates `doc/todo-archive.ndjson` and daily snapshot documents. Keep this file as the single source for human-readable backlog progress; use `doc/todo-archive.ndjson` as the machine source of truth.

Generated/Updated: 2026-02-06T12:50:00Z

## History (daily snapshots)

- **2026-02-06**: daily snapshot created. Deltas: marked `T002`, `T003`, `T004`, `T005`, `T007` completed. See daily files:
  - [06_02_project_overview.md](06_02_project_overview.md)
  - [06_02_todo_list.md](06_02_todo_list.md)

Future daily snapshots: create a new dated file `DD_MM_PROJECT.md` and add one-line summary here.

## Progress snapshot (representative)


| ID | Task | Priority | Status | % Complete | Delta % | Est Hrs | Hours Spent | Scrum Pt | Score | Last Updated |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| T001 | Purge leaked tokens (filter-repo plan) | critical | pending | 0% | 0% | 24.0 | 0.0 | 13 | 100 | 2026-02-05 |
| T002 | Add detect-secrets + pre-commit | high | completed | 100% | +100% | 2.5 | 2.5 | 8 | 50 | 2026-02-06T12:40:00Z |
| T003 | Mock Telegram harness | high | completed | 100% | +100% | 2.0 | 2.0 | 8 | 50 | 2026-02-06T12:40:00Z |
| T004 | Retryer backoff tests | high | completed | 100% | +100% | 1.0 | 1.0 | 8 | 50 | 2026-02-06T12:40:00Z |
| T005 | Normalize todos into NDJSON | medium | completed | 100% | +100% | 1.0 | 1.0 | 5 | 20 | 2026-02-06T12:30:00Z |
| T006 | Create GH issues for critical/high items | high | pending | 0% | 0% | 1.0 | 0.0 | 8 | 50 | 2026-02-05 |
| T007 | Run pytest smoke and record results | medium | completed | 100% | +100% | 0.5 | 0.5 | 2 | 10 | 2026-02-06T12:40:00Z |
| T008 | alby_agent dry-run prototype | high | pending | 0% | 0% | 16.0 | 0.0 | 8 | 50 | 2026-02-05 |

Totals (selected): Est Hrs=48.0, Completed Hrs=7.0, Pending Hrs=41.0

## Versioning & snapshot policy

- Canonical file: `MASTER_BACKLOG.md` (this file). Keep it updated with a human-friendly table and an append-only `History` section.
- Machine source: `doc/todo-archive.ndjson` — update this file when task statuses change. Prefer NDJSON for automation and issue creation.
- Daily snapshots: create `DD_MM_project_overview.md` and `DD_MM_todo_list.md` (or similar) for each working day; add a one-line summary into `History` above.

## Restore / Crash-resume pointer

- See `doc/agent_session_recovery.md` for the agent session lifecycle, resume rules, and the `.copilot/session_state.json` schema. Keep that document authoritative for automated recovery.

## How to update

1. Update `doc/todo-archive.ndjson` for machine changes (status, est_hours, result).
2. Update `MASTER_BACKLOG.md` table (human-readable) with owner/scrum points as needed.
3. Create dated snapshot files and append a one-line delta to the `History` section.

---

(file maintained by agent tooling; manual edits allowed but prefer PRs for significant changes)
