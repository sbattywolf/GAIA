# Sprint 1 Backlog — GAIA (2 week sprint)

Created: 2026-02-05 00:30 (UTC)

Goal: Stabilize pre-prod validation, finish docs consolidation, and prepare safe secret-rotation steps for owner review.

Stories (prioritized)

1) Stabilize pre-prod E2E (Priority: High) — 8 pts
- Description: Fix flaky readiness checks, ensure mock token service `/health` is reliable across runners, and make E2E run consistently in GitHub Actions.
- Acceptance: `ci-e2e-preprod.yml` runs green on `backlog/prototype` for the simple infra smoke-check; test timeout flakiness reduced; CI logs surface mock stderr.
- Docs: `tests/e2e/test_preprod_infra.py`, `scripts/mock_token_service.py`.

2) Create GitHub Environments & secret separation (Priority: High) — 5 pts
- Description: Create `dev` and `pre-prod` Environments in the repo, migrate secrets, and document usage in `doc/ENVIRONMENTS.md`.
- Acceptance: `pre-prod` environment exists and CI workflow references it; secrets documented.

3) Coordinate secret rotation runbook (Priority: High) — 5 pts
- Description: Work with owners to rotate external tokens, run detect-secrets check, and prepare history-rewrite dry-run checklist.
- Acceptance: Owners acknowledged; `doc/HISTORY_REWRITE_PLAN.md` updated with owner signoff instructions.

4) Audit & update key docs (Priority: Medium) — 5 pts
- Description: Update `doc/SECRETS.md`, `doc/ROTATION_PILOT_README.md`, and consolidate runbooks into canonical files listed in `doc/MASTER_DOC_INDEX.md`.
- Acceptance: Canonical files exist, deprecated copies moved to `doc/archive/` with `-deprecated` suffix.

5) Implement rotation pilot runner (Priority: Medium) — 8 pts
- Description: Flesh out the rotation pilot runner (non-production token), add canary steps and smoke-check job, and add monitoring hooks for failures.
- Acceptance: Actionable job exists in `.github/workflows/` and a smoke-check script demonstrates rotation on a non-production token.

6) Telegram notifications: stats & frequency (Priority: Low) — 3 pts
- Description: Validate `telegram_updates.json` population, add telemetry in `scripts/send_periodic_status.py`, and recommend frequency changes in `doc/TELEGRAM_STATS_SUMMARY.md`.
- Acceptance: At least one week of data available or a deploy plan to gather data.

7) Cleanup archived docs (Priority: Low) — 2 pts
- Description: After stakeholder review, remove originals from `doc/originals-to-delete/` or move to `doc/archive/legacy/` per `doc/archive/REVIEW.md` guidance.
- Acceptance: PR merged to delete or archive originals with reviewer approvals.

Owners and estimates are placeholders — please adjust owners and estimates in the PR discussion.

Next steps
- Create branch `sprint/1`, add this file, open PR to `backlog/prototype` and request product + docs review.
- Triage and move stories into issues/cards and estimate in planning meeting.
