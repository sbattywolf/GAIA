# CHECKPOINT_1: Purge Plan & Approval (git history token purge)

Date: 2026-02-07

Summary
- Purpose: describe the safe, reviewed process to remove leaked tokens and sensitive artifacts from git history using `git filter-repo` (or equivalent), with explicit approvals and rollback steps.
- Scope: operate only on repository `GAIA` branch `feat/update-sprint-2026-02-06` (work branch). No forced changes to `main`/`master` until approved and coordinated.

Stakeholders & Approvers
- Requestor: sprint owner / security lead.
- Reviewers: at least two maintainers with push rights.
- Final approval: explicit text approval recorded here and in an issue/PR comment by a maintainer.

Preconditions (must be completed before destructive actions)
1. Create and push a backup branch of current repo state: `backup/before-filter-repo-2026-02-07`.
2. Export `gaia.db` audit snapshot and copy `events.ndjson` and `doc/todo-archive.ndjson` to `./.tmp/backup/`.
3. Produce and share `doc/todo-archive.dryrun.diff` and have at least one reviewer confirm canonicalization.
4. Confirm secrets scan baseline (detect-secrets) and list of leaked candidate files.

Approval Statement (to be filled by approver)
"I, <name>, approve the planned `git filter-repo` purge on branch `feat/update-sprint-2026-02-06` as described in CHECKPOINT_1.md. I confirm backups exist and I accept the rollback plan." — Sign with username and UTC timestamp.

Execution Checklist (dry-run first)
1. Locally run a `git filter-repo` dry-run to identify affected commits and verify file removal mapping.
2. Review and validate the dry-run output with reviewers.
3. If accepted, run the filter-repo rewrite on a local clone, then run the following verification steps.

Commands (examples)
```powershell
# create backup branch
git checkout -b backup/before-filter-repo-2026-02-07
git push origin backup/before-filter-repo-2026-02-07

# clone mirror for rewrite work
git clone --mirror . repo-mirror.git
cd repo-mirror.git

# dry-run (example: list files to remove)
git filter-repo --analyze

# apply mapping (after review) -- EXAMPLE only, do not run until approved
git filter-repo --invert-paths --paths-from-file ../.tmp/filter-repo-paths.txt

# push rewritten branch to remote on a feature branch name
git remote add origin-rewrite <origin-url>
git push origin-rewrite --force --all
```

Verification
- Run `git rev-list --objects --all | grep <sensitive-pattern>` to ensure removals.
- Run CI smoke (pytest smoke) and confirm no regressions.
- Validate `doc/todo-archive.ndjson` and `gaia.db` sync (run validation script).

Rollback Plan
- If rewrite causes unexpected data loss or breakage:
  - Restore from `backup/before-filter-repo-2026-02-07` by checking out the branch and force-pushing to the feature branch.
  - If remote was overwritten, re-push the backup branch with force: `git push origin backup/before-filter-repo-2026-02-07:refs/heads/feat/update-sprint-2026-02-06 --force`.

Post-Action Tasks
- Update `events.ndjson` with an audit entry describing the purge action and trace_id.
- Record an entry in `gaia.db` audit table via `orchestrator.py` or manual SQL insert.
- Open PR/issue summarizing the purge with hashes of rewritten commits and listing the files removed.

Risk Notes
- This is destructive with respect to commit history and requires collaborators to reclone or reset local branches; coordinate widely.
- Keep all backups and dry-run artifacts indefinitely until team confirms safe.

Checklist: Approvals
- [ ] Backup created and pushed
- [ ] Dry-run reviewed
- [ ] Approver signature present below

Approver signature:

Name: ____________________  Date(UTC): ______________  Signature: ______________________
# CHECKPOINT_1 — Proposed History Rewrite / Secret Removal

Generated: 2026-02-06T14:00:00Z

Purpose: propose a controlled, reviewed git history rewrite to remove confirmed sensitive files and provide rotation guidance.

Attached artifacts:
- doc/sprints/analysis/secrets_inventory_20260206.md
- .tmp/detect_secrets_scan_20260206.json
- .tmp/detect_secrets_priority_20260206.csv

High-priority candidates (top 50):

- external\openclaw\.secrets.baseline  (289 findings; types: Hex High Entropy String;Private Key;Secret Keyword)
- .secrets.baseline  (10 findings; types: Hex High Entropy String;Secret Keyword)
- external\openclaw\.detect-secrets.cfg  (4 findings; types: Private Key;Secret Keyword)
- external\openclaw\src\logging\redact.test.ts  (4 findings; types: Base64 High Entropy String;Hex High Entropy String;Private Key)
- external\openclaw\src\config\config.env-vars.test.ts  (3 findings; types: Secret Keyword)
- doc\archive\pre_restructure_20260205T163407Z\HISTORY_REWRITE_PLAN.md  (1 findings; types: GitHub Token)
- external\openclaw\apps\ios\fastlane\Fastfile  (1 findings; types: Private Key)
- external\openclaw\src\gateway\client.test.ts  (1 findings; types: Private Key)

Planned steps (dry-run first):
1. Create a branch `checkpoint/remove-secrets-1` from `main`.
2. Run `git filter-repo --paths-from-file .tmp/sensitive_files_candidates.txt --replace-text replacements.txt` in dry-run mode on the branch.
3. Review results and ensure no unrelated files removed.
4. If confirmed, prepare replacements and open PR for human review.
5. After merge, rotate any exposed credentials and record rotation steps in `doc/rotation_playbooks/`.

Approval: Add a single-line `APPROVATO` entry below to approve proceeding, and record approver and UTC timestamp.

APPROVATO: 
