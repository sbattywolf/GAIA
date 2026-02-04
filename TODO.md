# GAIA Backlog (prioritized)

Last updated: 2026-02-04

This file is a human-friendly prioritized backlog. The canonical, machine-tracked todo list is kept in the repository's task tracker (manage_todo_list). Use this file for quick triage.

1. Merge PR & tag
   - Status: not-started
   - Notes: After final review, merge `chore/add-smoke-checks` and tag a small release noting CI and Telegram scaffolding fixes.

2. Finalize CI smoke
   - Status: in-progress
   - Notes: CI smoke checks added; consider optional `pip install -e .` fallback for any failing runner and add Telegram mock integration tests to the matrix.

3. Add secret scanning
   - Status: not-started
   - Notes: Install `detect-secrets` baseline and add pre-commit/CI checks.

4. Remove secrets from history
   - Status: not-started
   - Notes: If secrets were ever committed, coordinate history rewrite (git filter-repo/BFG) and rotate credentials.

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
   - Status: not-started
   - Notes: Draft filter-repo rules and share a one-line plan with collaborators before rewriting history.

9. Validate CI and imports (monitoring)
   - Status: completed 2026-02-04
   - Notes: Smoke import + pytest passed across matrix after `.pth` writer and YAML fixes.

10. Maintenance & housekeeping
    - Status: mixed (see manage_todo_list)
    - Notes: Review remaining items via the machine-tracked todo list.
