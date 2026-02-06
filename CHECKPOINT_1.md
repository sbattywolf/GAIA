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
