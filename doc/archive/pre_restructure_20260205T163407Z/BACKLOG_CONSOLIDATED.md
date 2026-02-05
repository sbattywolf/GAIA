# GAIA Consolidated Backlog

This file consolidates backlog items and stories extracted from `doc/`.

Top Epics & High-Level Stories
- Epic: F-helper-gise-part2 (Prototype & Acceptance)
  - Run prototype dry-runs and generate merge-candidate JSONs.
  - Run live archive+validate with local-only events.
  - Build mocked Telegram harness for acceptance; run end-to-end acceptance scenarios.
  - Add idempotency and replay tests; document results.

- Epic: F-helper-gise-part1 (Foundation)
  - Scan repo and collect examples; produce design docs.
  - Scaffold `scripts/alby_agent.py` with `--dry-run` and `--confirm` safe modes.
  - Unit tests for merge heuristics and safety guards.
  - Add `.env.template` and secrets handling guidance.

- Epic: Controller + Sequences (from `doc/TASKS.md`)
  - Implement Controller HTTP API endpoints (`/api/controller/*`).
  - Add UI controls to `monitor/templates/sequences.html`.
  - Systemd/service deployment artifacts and MyNAS deploy acceptance.

- Epic: CI & Repro (flake triage)
  - Harden repro workflow (pip/pytest retries) and deterministic smoke artifact (done).
  - Validate artifact upload/download end-to-end; fix upload step when no files found.
  - Add CI job-level logging for artifact folder contents before `upload-artifact`.

- Epic: Docs & Playbooks
  - Consolidate runbooks into `doc/PLAYBOOK_2026-02-03T000000Z.md` and `doc/MASTER_DOC_INDEX.md`.
  - Generate `doc/MASTER_DOC_INDEX.md` from docs (automation suggested in `DOCS_STRATEGY.md`).

Cross-cutting Tasks
- Add CI doc-check that new/changed docs include `Created:` or `Updated:` timestamp header.
- Add maintainers map `doc/MAINTAINERS.md` (owners by area).
- Create small automation to extract `TODO` and checkbox items from `doc/` into backlog JSON.

Immediate next priorities (ordered)
1. Validate repro workflow smoke-artifact upload/download (blocking for triage).
2. Implement Controller API endpoints (from `doc/TASKS.md` step 2).
3. Scaffold `scripts/alby_agent.py` dry-run mode and tests (F-helper-gise-part1).
4. Create `doc/MASTER_DOC_INDEX.md` (auto-generated) and `doc/MAINTAINERS.md`.

Notes
- Detailed per-feature tasks are preserved in existing `doc/STR_TODO_*` files; this consolidated backlog lists top-priority epics and immediate next actions.
- I can convert these backlog items into GitHub Issues or a kanban board on request.
