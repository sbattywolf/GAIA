# TODOs — Top 3 Features (by priority)

This document lists detailed, actionable TODOs for the top 3 features in `doc/EPC_Telegram.current`, intended to drive work and track progress. Create per-story `.current` and `.draft` files as needed and record impediments in `.tmp/gise_status/impediments/`.

Features covered (priority order):
- `F-helper-gise-part2` — Helper Gise — Prototype & Acceptance (score 34)
- `F-helper-gise-part1` — Helper Gise — Foundation (score 21)
- `F-helper-gise.STR_TestGise.part2` — STR_TestGise part2: acceptance & governance (score 21)

Format: each feature broken into stories, each story lists tasks with suggested priorities and acceptance criteria.

=================================================================

Feature: F-helper-gise-part2 — Prototype & Acceptance

Story: stoy_alby_prototype
- t41: Run prototype dry-runs (high)
  - Run `scripts/alby_agent.py --dry-run` over current drafts.
  - Acceptance: generator produces merge-candidate JSON files; no remote side-effects; validator reports 0 errors.

- t41a: Run prototype live archive+validate+tests (high)
  - Execute `scripts/alby_agent.py` on a copy of drafts with `PROTOTYPE_USE_LOCAL_EVENTS=1` to avoid remote GH calls.
  - Acceptance: archives created under `doc/archive/`, merge candidates created under `.tmp/merged_candidates/`, audit rows inserted to `gaia.db` (local), tests pass.

- t41b: Collect timings & metrics (medium)
  - Measure runtime of validate/tests/archive steps to help estimate story sizes.
  - Acceptance: CSV or JSON timings written to `.tmp/metrics/alby_prototype_timings.json`.

Story: stoy_alby_acceptance
- t42: Prepare mocked Telegram harness for acceptance flows (high)
  - Implement a simple HTTP stub that mimics Telegram Bot API for local acceptance tests.
  - Acceptance: `approval_listener.py` + test harness runs end-to-end without external network.

- t43: Run acceptance scenario: create claim → approve → archive event (high)
  - Execute scripted scenario against mocked Telegram; assert events.ndjson entries and gaia.db traces.
  - Acceptance: assertions pass; evidence artifacts stored in `.tmp/acceptance_runs/`.

- t44: Add idempotency and replay tests (high)
  - Tests to ensure duplicate updates do not trigger duplicate side-effects.
  - Acceptance: tests in `tests/` asserting idempotency.

- t45: Document prototype results and update scoring (medium)
  - Add results to `doc/EPC_Telegram_report_addendum.md` with re-estimates.
  - Acceptance: report committed and referenced in PR.

=================================================================

Feature: F-helper-gise-part1 — Foundation

Story: stoy_alby_scan (high)
- t38: Scan repository and collect examples (high)
  - Run automated scans to locate ALby references, patterns, and useful tests.
  - Acceptance: `doc/OPENCLAW_SCAN.md` or `doc/STORY_ALBY.md` updated with references.

Story: stoy_alby_design (high)
- t39: Design agent architecture (high)
  - Produce component sketch: scanner, validator, archiver, candidate-writer, auditor.
  - Acceptance: `doc/STORY_ALBY.md` updated with architecture and CLI interface.

Story: stoy_alby_scaffold (high)
- t40: Implement `scripts/alby_agent.py` scaffold (high)
  - CLI with `--dry-run`, `--story`, `--archive`, `--validate` flags; safe defaults.
  - Acceptance: dry-run mode runs locally and prints candidate paths; live mode writes to `.tmp/merged_candidates/` when `--confirm` provided.

- t40a: Add unit tests for merge heuristics (medium)
  - Tests that assert expected merge-candidate metadata and provenance fields.
  - Acceptance: `tests/test_alby_agent_merge.py` covers main cases.

- t40b: Add safe-quoting and execution guards (high)
  - Enforce `ALLOW_COMMAND_EXECUTION=0` default and require explicit opt-in.
  - Acceptance: code prevents shell injection and not-executing commands by default.

Story: stoy_env_and_secrets (medium)
- t40c: Implement safe env loading and `.env.template` (medium)
  - Provide `.env.template` and docs for secure storage/permissions for `.tmp/telegram.env`.
  - Acceptance: `SECRETS_TESTING.md` contains recommended file perms and rotate script scaffold.

- t40d: Add verbose debug logging for claim acquisition (medium)
  - Temporary logging toggles to help diagnosis; gated behind `LOG_LEVEL` env var.
  - Acceptance: debug logs available when enabled.

=================================================================

Feature: F-helper-gise.STR_TestGise.part2 — Acceptance & Governance

Story: stoy_acceptance_flow (critical)
- t2: Run full acceptance scenario end-to-end (high)
  - Create claim, approve via mocked Telegram, assert gaia.db traces and events.ndjson entries.
  - Acceptance: end-to-end test artifacts stored and assertions pass.

- d1: Regression: claim takeover when TTL expired (high)
  - Simulate TTL expiry and ensure takeover semantics work as defined.
  - Acceptance: regression test passes; documented in `doc/STR_Telegram.current` notes.

- d2: Document chat-history lookup and audit steps (medium)
  - Add runbook section describing how to extract chat history and attach to audit traces.
  - Acceptance: `doc/STR_Telegram.current` updated with runbook section and example commands.

- g2: Run acceptance flow and record timestamps in gaia.db (high)
  - Ensure audit timestamps and trace IDs are persisted and cross-linked to events.ndjson entries.
  - Acceptance: sample audit entries present in `gaia.db` and query examples available.

- t_final: Governance closure (critical)
  - Collect chat history, evidence, attach to PR, and mark story closed.
  - Acceptance: story `STR_TestGise` marked completed in canonical epic and PR includes evidence.

=================================================================

Impediments & recording
- For each task, create entries in the corresponding `.draft.json` file under `doc/` named like `EPC_Telegram.<feature>.<story>.draft.json` using the `impediments` array to capture blockers.
- Log run-time errors to `.tmp/gise_status/impediments/<timestamp>_<taskid>.log`.

Workplan (suggested immediate sequence)
1. Implement foundation scaffolds: `F-helper-gise-part1` (`t38,t39,t40`) — get dry-run working.
2. Run prototypes (dry-run) for `F-helper-gise-part2` (`t41`), collect timings (`t41b`).
3. Spin up mocked Telegram harness and run acceptance flows for STR (`stoy_alby_acceptance`, `stoy_acceptance_flow`).
4. Iterate on heuristics, add tests, update docs and scoring.

Notes
- Files created by generators: per-story `.current.json` and `.draft.json` already present under `doc/` (stoy_auto scaffolds). Update those with real tasks when you accept this plan.
- Notifications: autonomous runner will post 10-minute updates to configured Telegram chat summarizing progress and percent-complete metrics.
