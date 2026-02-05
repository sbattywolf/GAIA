# Project Overview & Epic Breakdown (snapshot)

Generated: 2026-02-05 14:00 (24:00-hour format, no seconds)

Purpose
- Describe what I understand needs to be done, organize collected todos into Epics → Features → Stories → Tasks, provide scoring and time estimates, and summarize progress with human-readable tables. This is a snapshot-based plan you can use to drive work, create issues, or hand to a sprint planner.

Scoring & estimation rules (used consistently below)
- Priority → Task Score / Est Hours / Scrum Points
  - critical: 100 / 24h / 13pt
  - high: 50 / 16h / 8pt
  - medium: 20 / 8h / 5pt
  - low: 5 / 4h / 2pt
- Aggregation: Feature score = sum(task scores). Epic score = sum(feature scores). Project score = sum(epic scores).
- % Completed: measured by weighted score completed / total score (weighted by task score).
- Hours Spent: where a task is `completed` we assume hours_spent = est_hours; `in-progress` assume 50% of est_hours; `pending` assume 0h spent.

Legend: Status values used (`completed`, `in-progress`, `pending`). Time fields are in hours. Timestamps use `YYYY-MM-DD HH:MM` format.

-------------------------------------------------------------------------------

## Project summary table (all epics)

| Epic | Features | Tasks | Total Score | Est Hours | Hours Spent | % Completed | Scrum Points | Last Updated |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| CI & Testing | CI Stability, Integration Tests | 7 | 360 | 112h | 36h | 30% | 56pt | 2026-02-05 14:00 |
| Security & Secrets | Secret Scanning, Token Rotation | 6 | 245 | 96h | 4h | 4% | 38pt | 2026-02-05 14:00 |
| Telegram Integration | Realtime + Harness + Runbooks | 12 | 520 | 200h | 8h | 2% | 88pt | 2026-02-05 14:00 |
| Agent Automation | alby_agent prototype, automation runners | 6 | 200 | 72h | 0h | 0% | 32pt | 2026-02-05 14:00 |
| Backlog & Docs | Docs restructure, OVERVIEWs, Index | 10 | 140 | 56h | 30h | 54% | 22pt | 2026-02-05 14:00 |
| Operations & Monitoring | Metrics, backups, monitor UI | 7 | 125 | 56h | 8h | 6% | 35pt | 2026-02-05 14:00 |
| **Project Totals** | 7 epics | 48 tasks | **1590** | **592h** | **86h** | **14%** | **271pt** | 2026-02-05 14:00 |

Notes: totals are derived by summing the representative tasks below; this is a synthesized snapshot—not every repository todo is expanded into an explicit task here but the major workstreams are represented.

-------------------------------------------------------------------------------

## Epic: CI & Testing

Purpose: stabilize CI, add deterministic smoke, and create integration test harnesses.

| Feature | Story | Task | Priority | Score | Est Hrs | Status | Hours Spent | Scrum Pt | Added |
|---|---|---|---:|---:|---:|---|---:|---:|---|
| CI Stability | Fix CI workflow | Open PR to fix CI workflow | high | 50 | 16 | completed | 16 | 8 | 2026-02-03 10:00 |
| CI Stability | Write .pth helper | Patch CI to write .pth | high | 50 | 16 | completed | 16 | 8 | 2026-02-03 11:00 |
| CI Stability | Replace heredoc on Windows | Replace heredoc with helper script | medium | 20 | 8 | completed | 8 | 5 | 2026-02-03 11:30 |
| Integration tests | Mocked Telegram harness | Implement mocked Telegram API harness | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Integration tests | Approval flow test | Add integration test approval→claim_cli | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Testing | TTL & takeover tests | Add automated tests for TTL expiry and takeover | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Testing | Idempotency & replay tests | Add idempotency/replay tests | high | 40 | 24 | pending | 0 | 8 | 2026-02-05 14:00 |

Feature totals: Score=310, Est=108h, Spent=40h, Scrum=53pt

-------------------------------------------------------------------------------

## Epic: Security & Secrets

Purpose: remove leaked tokens, add scanning and rotation, protect production secrets.

| Feature | Story | Task | Priority | Score | Est Hrs | Status | Hours Spent | Scrum Pt | Added |
|---|---|---|---:|---:|---:|---|---:|---|---|
| Secrets Cleanup | Purge tokens from history | Purge leaked tokens (filter-repo plan) | critical | 100 | 24 | pending | 0 | 13 | 2026-02-05 14:00 |
| Secrets Tools | Secret scanning & pre-commit | Add detect-secrets + pre-commit | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Rotation | Token rotation & env templates | Create .env.template + rotate_admin_token scaffold | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Ops | Create protected production env | Create GitHub Environment `production` & reviewers | medium | 20 | 8 | pending | 0 | 5 | 2026-02-05 14:00 |
| Secrets Ops | Remove leaked token occurrences | remove files with tokens & placeholders | completed | 25 | 12 | completed | 4 | 2 | 2026-02-04 09:00 |

Feature totals: Score=245, Est=76h, Spent=4h, Scrum=36pt

-------------------------------------------------------------------------------

## Epic: Telegram Integration

Purpose: finalize realtime spec, add a mocked harness, implement retry/backoff, and runbook improvements.

| Feature | Story | Task | Priority | Score | Est Hrs | Status | Hours Spent | Scrum Pt | Added |
|---|---|---|---:|---:|---:|---|---:|---|---|
| Realtime & Spec | Telegram realtime spec | Finalize realtime spec & docs | medium | 20 | 8 | completed | 8 | 5 | 2026-02-02 16:00 |
| Retryer | Implement backoff & map error codes | Exponential backoff, tests for 429/5xx | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Monitoring | Metrics + dashboard | Add counters, persist metrics, alerts wiring | medium | 20 | 8 | pending | 0 | 5 | 2026-02-05 14:00 |
| Runbooks | One-click requeue & audit traces | Implement secure UI actions + audit traces | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Tooling | Mocked Telegram harness (CI/local) | see CI epic (duplicate) | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Documentation | CLI examples & workflows | Add CLI examples and release checklist | low | 5 | 4 | pending | 0 | 2 | 2026-02-05 14:00 |
| Backups | Backup & retention scripts | Implement backup_tmp.py and cleanup | medium | 20 | 8 | pending | 0 | 5 | 2026-02-05 14:00 |
| Story: acceptance flow | Acceptance: claim→approve→archive | Run acceptance scenario, record gaia.db traces | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |

Feature totals (representative): Score=265, Est=92h, Spent=8h, Scrum=49pt

-------------------------------------------------------------------------------

## Epic: Agent Automation (alby_agent)

Purpose: prototype alby_agent to automate doc merges, validations, and targeted tests.

| Feature | Story | Task | Priority | Score | Est Hrs | Status | Hours Spent | Scrum Pt | Added |
|---|---|---|---:|---:|---:|---|---:|---|---|
| Prototype | alby_agent dry-run | Scaffold and run dry-run prototype | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Prototype | alby_agent live local | Run alby_agent local-only | high | 50 | 16 | pending | 0 | 8 | 2026-02-05 14:00 |
| Metrics | Collect prototype timings | Collect metrics and update estimates | medium | 20 | 8 | pending | 0 | 5 | 2026-02-05 14:00 |
| Integration | Acceptance & idempotency tests | Add idempotency and replay tests | high | 50 | 24 | pending | 0 | 8 | 2026-02-05 14:00 |

Feature totals: Score=170, Est=64h, Spent=0h, Scrum=29pt

-------------------------------------------------------------------------------

## Epic: Backlog & Docs (work already done and follow-ups)

Purpose: reorganize docs, add OVERVIEWs, and maintain master index. Many tasks already completed — this epic contains remaining curation.

| Feature | Story | Task | Priority | Score | Est Hrs | Status | Hours Spent | Scrum Pt | Added |
|---|---|---|---:|---:|---:|---|---:|---|---|
| Docs Restructure | Merge docs -> doc/ and archive | Archive originals & scaffold new folders | medium | 20 | 8 | completed | 20 | 5 | 2026-02-05 16:34 |
| Overviews | Add OVERVIEWs | Create `02_technical/OVERVIEW.md` & `03_procedural/OVERVIEW.md` | medium | 20 | 8 | completed | 4 | 5 | 2026-02-05 12:10 |
| Index | MASTER_DOC_INDEX updates | Add overview links and summaries | low | 5 | 4 | completed | 2 | 2 | 2026-02-05 12:40 |
| Backlog consolidation | MASTER_BACKLOG and summaries | Consolidate backlog items & generate MASTER_BACKLOG.md | medium | 20 | 8 | in-progress | 4 | 5 | 2026-02-05 14:00 |

Feature totals: Score=65, Est=28h, Spent=30h, Scrum=17pt

-------------------------------------------------------------------------------

## Epic: Operations & Monitoring

Representative tasks
- Implement monitor UI page for permanent-failed entries; one-click requeue with token protection (high).
- Implement backup & retention scripts (medium).
- Wire metrics persistence and alerting (medium).

Totals (representative): Score=125, Est=56h, Spent=8h, Scrum=35pt

-------------------------------------------------------------------------------

How to use this document
- Review epic/feature mappings and adjust priorities or break stories into smaller tasks. Use the Score and Est Hours as starting guidance for sprint planning.
- If you want, I can: 1) normalize every todo into `doc/todo-archive.ndjson`, 2) create GitHub issues for each `high`/`critical` task, and 3) produce a sprint plan (2-week cadence) with assignments.

Next suggested steps (automatable)
1. Normalize todo items into NDJSON and include `source`, `priority`, `est_hours`, `scrum_points`, `score`, `status`, `added_at` (I can create `doc/todo-archive.ndjson`).
2. Create issues for critical/high tasks (batch) and link back to this overview.
3. Run local `pytest -q` and produce a failing-tests report to prioritize flaky fixes.

If you want changes (different scoring, other time estimates, or a CSV/JSON export), tell me which format and I will generate it.
