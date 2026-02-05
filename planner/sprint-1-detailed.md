# Sprint 1 — Detailed Backlog (Minimal slices)

Goal: Stabilize CI + E2E preprod readiness, seed sprint with small idempotent tasks, enable safe automation and approvals.

Sprint length: 2 weeks (or as needed). Keep pieces small (<= 4 hours / 1-2 story points where possible).

Top-level stories (ordered by priority):

1. E2E readiness and mock verification (Est: 4h)
   - Micro: Harden `scripts/mock_token_service.py` health endpoint (0.5h)
   - Micro: Fix flaky wait/retry in `tests/e2e/test_preprod_infra.py` (1h)
   - Micro: Add small container startup backoff script `scripts/wait_for_services.sh` (1h)
   - Micro: Run two CI runs and capture logs (1.5h)

2. Sprint onboarding automation (Est: 6h)
   - Micro: Create sprint issues template and checklist (`planner/sprint-issue-template.md`) (1h)
   - Micro: Ensure `PROJECT_V2_NUMBER` secret exists and workflow uses it (done) (0.5h)
   - Micro: Test `sprint_onboard.yml` by labeling a staging issue (2h)
   - Micro: Apply minor fixes and re-run onboarding (2.5h)

3. Automation runner + approval (Est: 3h)
   - Micro: Add `scripts/automation_runner.py` that requests file-based approvals (done) (1h)
   - Micro: Add `scripts/approve_listener.py` to convert operator approval into ack (done) (0.5h)
   - Micro: Add `scripts/supervisor.ps1` and a short `scripts/run_20h.ps1` launcher (0.5h)
   - Micro: Smoke test end-to-end (1h)

4. Secrets & token rotation pilot (Est: 6h)
   - Micro: Document secrets naming and set repo secrets (2h)
   - Micro: Add `scripts/set_repo_tokens.ps1` idempotent helper (2h)
   - Micro: Dry-run token rotation simulation (2h)

5. Observability & logging (Est: 4h)
   - Micro: Ensure `events.ndjson` gets appended for each action (1h)
   - Micro: Add `scripts/collect_logs.ps1` to gather logs and DB snapshot (1h)
   - Micro: Configure periodic Telegram heartbeat (1h)
   - Micro: Add a lightweight `doc/AUTOMATION_RUNBOOK.md` draft (1h)

Notes and constraints:
- Keep tasks idempotent.
- Prefer interactive approvals for sensitive actions.
- Postpone large-scale log rotation — capture now and schedule rotation later.

Acceptance criteria:
- CI E2E test passes locally twice in a row.
- Onboard workflow can add issues to Projects V2 for a labeled test issue.
- Automation runner can request an approval and proceed after ack.
