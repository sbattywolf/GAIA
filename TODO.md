# GAIA Backlog (prioritized)

Last updated: 2026-02-06

This file is a human-friendly prioritized backlog. The canonical, machine-tracked todo list is kept in the repository's task tracker (manage_todo_list). Use this file for quick triage.

1. Merge PR & tag
   - Status: completed (PR #105 merged)
   - Notes: PR #105 (`Add centralized secrets management with encryption and rotation support`) merged 2026-02-05; consider tagging a patch release documenting rotation and audit steps.

2. Finalize CI smoke
   - Status: completed
   - Notes: Quick `pytest` smoke run passed (115 passed, 1 skipped). Consider expanding matrix and adding Telegram mock to CI.

3. Add secret scanning
   - Status: in-progress
   - Notes: `detect-secrets` baseline run performed with a regex fallback; integration into CI/pre-commit is pending final config and reliability fixes.

4. Remove secrets from history
   - Status: blocked / pending CHECKPOINT approval
   - Notes: CHECKPOINT process and dry-run migration created; do not perform destructive history rewrite until approvals and communication plan complete.

5. Create `production` environment
   - Status: not-started
   - Notes: Add GitHub Environment `production`, add rotated secrets, and require reviewers before deployment.

6. Add auto-merge workflow
   - Status: not-started
   - Notes: Merge PRs automatically when CI passes and required approvals are present.

7. Integrate `external/openclaw`
   - Status: not-started
   - Notes: Decide whether to vendor, submodule, or package; add a lightweight wrapper and usage docs.

8. Purge leaked tokens plan
   - Status: in-progress
   - Notes: Candidate inventory generated (`doc/sprints/analysis/candidates.ndjson`, 14,579 entries). Prioritized CHECKPOINT issues (#110..#129) created for manual triage.

9. Validate CI and imports (monitoring)
   - Status: completed 2026-02-04
   - Notes: Smoke import + pytest passed across matrix after `.pth` writer and YAML fixes.

10. Maintenance & housekeeping
    - Status: mixed (see manage_todo_list)
    - Notes: Review remaining items via the machine-tracked todo list.
