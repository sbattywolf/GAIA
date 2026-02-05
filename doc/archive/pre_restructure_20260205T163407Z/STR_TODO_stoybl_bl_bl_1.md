**STR_TODO_stoybl_bl_bl_1**

- **Story**: stoybl bl bl 1
- **Short key**: stoybl_bl_bl_1
- **Created**: 2026-02-03

Overview
- Primary feature: integrate durable claim primitives into operator flows and ensure safe, auditable approvals for queued commands.
- This STR splits the work in focused sub-stories: claims integration, test coverage, runbook/run procedures, and CLI/UI ergonomics.

Top-level tasks (source: `.tmp/todolists/...current`)
- `t1` Implement claim primitives integration — Wire `scripts/claims.py` into monitor server and CLI; ensure audit traces (in-progress)
- `t2` Evaluate TODO classification and apply — normalize classifications for the work (in-progress)
- `t3` End-to-end functional test (phase 1) — focused unit-first tests for admin requeue → retry worker → audit traces (todo)
- `t4` Tests: multi-agent concurrency & idempotency — simulate concurrent agents and assert at-most-once (todo)
- `t5` Update runbook: agent-task workflow & token usage — document in `doc/HANDOFF.md` (todo)
- `t6` Prepare follow-up part2 (CLI/UI + runbook) — create part2 draft (todo)
- `t7` CLI/UI controls — Add monitor UI buttons and CLI commands to inspect/claim/release (todo)
- `t8` Runbook entry — Document claiming workflow and token guidance in `doc/HANDOFF.md` (todo)
- `t_final` Governance: finalize todo-list best-practice rule (todo)

Strategy & decomposition
- Goal: keep each sub-story small, testable, and independently deliverable.
- For each top-level task create an STR sub-doc (claims, tests, runbook, cli-ui) with:
  - Purpose and acceptance criteria
  - Minimum viable implementation steps
  - Tests to validate behavior
  - Rollout and rollback notes

Files created from this STR (sub-stories)
- `doc/STR_TODO_stoybl_bl_bl_1_claims.md` — claim primitives integration details
- `doc/STR_TODO_stoybl_bl_bl_1_tests.md` — tests and fixtures
- `doc/STR_TODO_stoybl_bl_bl_1_runbook.md` — runbook edits and operator examples
- `doc/STR_TODO_stoybl_bl_bl_1_cli_ui.md` — CLI and monitor UI improvements

Acceptance (meta):
- Each sub-story has a PR with code, tests, and a short runbook snippet.
- `gaia.db` audit traces include a `trace_id` for the approval actions and show the lifecycle: queued → claimed → approved/denied → processed.
- Concurrency tests show no duplicate side-effects (idempotent processing verified).

Next steps
- Generate the sub-story docs (claims, tests, runbook, cli-ui) and iterate.
