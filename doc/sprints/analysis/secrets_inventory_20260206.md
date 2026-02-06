# Secrets Inventory — 2026-02-06

Generated: 2026-02-06T13:20:00Z

Purpose: inventory candidate files/locations that may contain secrets or tokens to inform `filter-repo` rules and CHECKPOINT creation.

Search patterns: token, secret, password, TELEGRAM, telegram.env, API_KEY, PRIVATE_KEY, AWS_ACCESS, aws_secret, auth_token

Findings (candidate locations / context)

- `tests/test_failed_reply_retryer.py` and related tests: write `TELEGRAM_BOT_TOKEN` to test env files for test fixtures (safe; test tokens).
- `tests/*.py` evidence: many tests set `TELEGRAM_BOT_TOKEN`, `PGPASSWORD` and other env vars in test fixtures. These are test-only values and should be excluded from filter-repo rules or replaced with placeholders.
- `scripts/*` and `agents/*` usage: modules reference `telegram.env` and `ENV_FILE` in tests; look for runtime `.tmp/*.env` files.
- `.copilot/session_state.json`: contains session metadata; ensure no secrets are persisted here.
- `doc/archive/pre_restructure_20260205T163407Z/*`: historical JSON files (EPC_Telegram.*) — these may contain tokens in payloads or examples; include them in inventory for manual review.
- `tests/test_secrets.py`: demonstrates secrets handling; includes sample `secrets.key` and encrypted files in temp directories — verify backups don't include real keys.

Candidate files to include in `sensitive.txt` for filter-repo dry-run
- doc/archive/pre_restructure_20260205T163407Z/** (review each JSON for secret fields)
- *.env, .tmp/*.env, .tmp/*telegram*.json
- any `.key` or `.enc` files found in repo history

Next steps (recommended)
1. Run `detect-secrets scan` across repo to generate baseline and refine candidate list (we added detect-secrets earlier; run now in dry-run mode).
2. Collect all historical commits with potentially sensitive filenames and add to `sensitive.txt` for `git filter-repo --paths-from-file sensitive.txt --replace-text replacements.txt` dry-run.
3. Create `CHECKPOINT_1.md` summarizing the planned replacements and impact (branch, timeline, PR, required approvals).
4. Only after explicit approval, perform non-destructive rewriting steps and rotate any exposed credentials.

Commands to run (dry-run examples)

```powershell
# detect-secrets baseline (dry-run)
detect-secrets scan > .tmp/detect_secrets_scan_20260206.json

# produce list of candidate filenames using git log (example)
git rev-list --all | ForEach-Object { git ls-tree -r --name-only $_ } | Select-String -Pattern '\.env|telegram|secrets|\.key|\.enc' | Sort-Object -Unique > .tmp/sensitive_files_candidates.txt
```

Inventory created by: GAIA agent (automated search). Save this file as artifact for `CHECKPOINT_1.md` creation.

Scan summary (generated from `.tmp/detect_secrets_scan_20260206.json`):

- Total findings: ~200+ (many are entries inside `external/openclaw` and `.secrets.baseline` files).
- High-priority candidates:
	- `doc/archive/pre_restructure_20260205T163407Z/HISTORY_REWRITE_PLAN.md`: flagged as `GitHub Token` (review immediately).
	- `external/openclaw/*`: numerous `Private Key`, `Hex High Entropy String`, and `Secret Keyword` findings; these appear to be third-party or vendored code — review for real secrets vs. test/sample data.
	- Any `*.env`, `.tmp/*.env`, and files under `doc/archive` should be manually inspected for real credentials.

Redaction note: findings are hashed in the scanner output; do not paste raw secrets into repository files. For human review, open the identified files locally and redact examples before committing.

Added next-actions (automated):
1. Produce `sensitive_files_candidates.txt` (git-paths list) and include `doc/archive/...`, `*.env`, `.tmp/*`, and any `.key`/`.enc` files. (task)
2. Draft `CHECKPOINT_1.md` describing the planned `git filter-repo` replacement rules and branch/PR workflow. (task)
3. Run a controlled `git filter-repo --dry-run` using `sensitive_files_candidates.txt` on a disposable branch, capture results, and inspect removed content. (task)
4. If secrets are confirmed leaked, rotate credentials and document rotation steps and timelines. (epic — may require external API access per provider).

Artifacts created:
- `.tmp/detect_secrets_scan_20260206.json` — full scanner output (329 KB).
- `.tmp/sensitive_files_candidates.txt` — (not yet created) to be produced by the follow-up command in next-actions.
