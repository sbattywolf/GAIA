**RECOVERY / Handoff Document**

Purpose
- Provide a single-file checkpoint and recovery instructions if an agent session stops unexpectedly.

Location
- Session state: `.copilot/session_state.json`
- Sprint report: `doc/sprints/05_02_sprint_report.md`
- Roadmap: `doc/roadmaps/roadmap_v2.md`

Quick status (snapshot)
- last_sync: 2026-02-05T11:00:00Z
- sprint_goal: Stabilize automation guards and approval flow
- current_task_id: TASK-001
- status: IN_PROGRESS
- plan_approved: false
- next_immediate_step: Run pytest -q tests/ to validate repository state

What to do to resume (checklist)
1. Open this repository and ensure you're on the expected branch (usually `main`).
2. Validate Python environment and run tests:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q tests/
```

3. Inspect `.copilot/session_state.json` to see `next_immediate_step` and `steps_completed`.
4. Review `doc/sprints/05_02_sprint_report.md` for sprint context and remaining items.
5. If you need to continue automation work, see `doc/sprints/05_02_part3_mock_telegram.md` and `05_02_part4_retryer.md` for how to run the mock server and notifier.

Important files to inspect
- `agents/mock_telegram.py` — local Telegram mock server (used in CI).
- `agents/telegram_notifier.py` — notifier that posts via `send_message()` (uses Retryer).
- `agents/retryer.py` — retry helper used across agents.
- `.github/workflows/mock-telegram-ci.yml` — CI job that runs mock+tests and uploads artifacts.
- `doc/sprints/analysis/` — artifacts from secrets inventory and grep scans.

Restart tips & best practices
- Always rotate any leaked tokens immediately (check `doc/sprints/analysis/REDACTED_MAP.txt`).
- Do not run destructive history rewrite steps until `CHECKPOINT_1` is approved.
- Use the mock Telegram server for integration tests — it is dependency-free and recorded to an NDJSON file for debugging.
- When resuming, run `pytest -q tests/test_mock_telegram.py tests/test_retryer.py tests/test_telegram_notifier.py` first.

If you hand me this file after a crash
- I will read `.copilot/session_state.json` and this `RECOVERY.md`, run the `next_immediate_step`, and continue the backlog from the recorded `next_immediate_step`.

Contacts / Notes
- Owner recorded in sprint artifacts: `sbattywolf` (see `doc/sprints/` files).

--

Recent automated actions
- A background detect-secrets scan was started and is writing logs/artifacts to `doc/sprints/analysis/`.
- New starter scripts were added for safe, dry-run automation:
	- `scripts/collect_candidates.py` — parses analysis files and emits `doc/sprints/analysis/candidates.ndjson`.
	- `scripts/rotate_token_stub.py` — records dry-run rotation events to `events.ndjson` and writes a stub report to `doc/sprints/analysis/rotation_stub_report.json`.

Next steps (you can ask me to run these):
- Run `python scripts/collect_candidates.py` to convert scan artifacts into candidate NDJSON.
- Run `python scripts/rotate_token_stub.py --dry-run` to generate a dry-run rotation report and audit events (no revokes).

- Merge daily sprint documents:

	We maintain per-day sprint files (e.g. `05_02_sprint_report.md`). To simplify history
	and handoffs, run the `scripts/merge_daily_sprints.py` script to concatenate all
	the day's sprint artifacts into a single `DD_MM_YY_merged.md` file in `doc/sprints/`.

	Example (run in PowerShell):

```powershell
# merge for UTC today
.venv\Scripts\python scripts/merge_daily_sprints.py
# merge for a specific date
#.venv\Scripts\python scripts/merge_daily_sprints.py --date 2026-02-05
```

	The script looks for files that start with `DD_MM_YY_` or `DD_MM_`.
	We recommend running it after midnight UTC (or as part of a daily CI job) and
	storing the merged file as the canonical daily snapshot (e.g. `06_02_26_merged.md`).

## Autonomous Runner (8-hour safe mode)

We provide a small runner to operate the non-destructive automation tasks autonomously for a limited period (e.g. 8 hours). The runner performs periodic scans, candidate collection, and dry-run rotation simulations — it will NOT perform any real revokes.

Usage (start it in background):

```powershell
# runs for 8 hours, every 10 minutes
.venv\Scripts\python scripts/autonomous_runner.py --duration 28800 --interval 600
```

What it does:
- Run `scripts/detect_secrets_proto.py` (scan) and append logs to `doc/sprints/analysis/`.
- Run `scripts/collect_candidates.py` to generate `doc/sprints/analysis/candidates.ndjson`.
- Run `scripts/rotate_token_stub.py --dry-run` to simulate rotations and append events to `events.ndjson`.
- Writes activity to `doc/sprints/analysis/autonomous_runner.log`.

Safety notes:
- The runner never performs real revokes or destructive operations.
- Any real revocation must be manually requested with `--revoke` and is gated behind `scripts/await_checkpoint.py` (CHECKPOINT approval).
- To stop the runner early, kill the process or remove the runner PID file in `.tmp/runner.pid` if present.

Backup & rollback:
- A backup of the workspace was created before this run in `.backup/` with a timestamped folder. Use that to restore files if needed.

Recovery loop guidance:
- If the runner encounters repeated errors (timeouts, missing deps), pause it and run the failing command interactively to diagnose.
- Break large tasks into smaller steps and re-run the failing step alone (e.g. `python scripts/collect_candidates.py`).

## Verify autonomous runner `detect_secrets_proto` success

Add this verification to make recovery safe and reproducible. Use these checks when resuming or validating the runner.

- **Check log tail (PowerShell):**

```powershell
Get-Content -Path doc/sprints/analysis/autonomous_runner.log -Tail 200
```

- **Quick grep for successful detect run (PowerShell):**

```powershell
# look for entries where detect_secrets_proto rc == 0
Get-Content doc/sprints/analysis/autonomous_runner.log -Tail 500 | Select-String -Pattern '"detect_secrets_proto".*"rc"\s*:\s*0'
```

- **Python check (cross-shell):**

```powershell
.venv\Scripts\python - <<'PY'
import json
ok=False
with open('doc/sprints/analysis/autonomous_runner.log','r',encoding='utf-8') as fh:
	for line in fh:
		try:
			obj=json.loads(line)
		except Exception:
			continue
		for step in obj.get('steps',[]):
			if step.get('name')=='detect_secrets_proto' and step.get('rc')==0:
				ok=True
				break
print('detect_secrets_proto OK' if ok else 'detect_secrets_proto NOT OK')
PY
```

- **If `NOT OK`:**
  - Inspect the last runner entry to see the failing `steps` snippet and error message.
  - Run the failing command interactively to reproduce (example):

```powershell
# run detect scan interactively
.venv\Scripts\python scripts/detect_secrets_proto.py --timeout 300
```

- **Restart runner (PowerShell):**

```powershell
# stop by PID (if known) then start background runner
if (Get-Process -Id (Get-Content .tmp/runner.pid -ErrorAction SilentlyContinue) -ErrorAction SilentlyContinue) { Stop-Process -Id (Get-Content .tmp/runner.pid) -Force }
Start-Process -NoNewWindow -FilePath .venv\Scripts\python.exe -ArgumentList 'scripts\\autonomous_runner.py --duration 28800 --interval 600' ; Write-Output 'Autonomous runner started (background)'
```

Place this verification in the recovery checklist and run it after any restart or code change to ensure the runner is performing scans correctly.

## Recent Verification (2026-02-06)

Summary of non-destructive checks performed on 2026-02-06 UTC:

- **Runner PID:** `.tmp/runner.pid` exists (pid 26672).
- **Runner logs:** `doc/sprints/analysis/autonomous_runner.log` present; short-run log at `.tmp/autonomous_runner.log` contains recent start/stop entries. Logs show repeated `detect_secrets_proto` timeouts (rc 124) during background runs.
- **Detect baseline:** `doc/sprints/analysis/detect_secrets_scan.txt` exists (137 lines). Head of file contains multiple GitHub PAT-like matches and backup references.
- **Candidates:** `doc/sprints/analysis/candidates.ndjson` contains 14,579 candidate entries (sample entries present).
- **Prioritized checkpoints:** `doc/sprints/analysis/prioritized_issues` contains 20 `CHECKPOINT_*.md` files, `SUMMARY.md`, and `ISSUES_CREATED.ndjson` mapping to issues #110–#129.
- **PR #105 status:** PR 105 (`Add centralized secrets management with encryption and rotation support`) is merged (mergedAt: 2026-02-05T23:51:41Z) by `sbattywolf`. No reviews were recorded and no issues were closed automatically by the PR (closingIssuesReferences empty).

Actionable checklist (safe, non-destructive verification):

1. Confirm PID and process (if expected): `Get-Content .tmp/runner.pid` and validate process with `Get-Process -Id <pid>`.
2. Tail the runner log and look for successful `detect_secrets_proto` runs (rc == 0):

```powershell
Get-Content doc/sprints/analysis/autonomous_runner.log -Tail 200
Get-Content doc/sprints/analysis/autonomous_runner.log -Tail 500 | Select-String -Pattern '"detect_secrets_proto".*"rc"\s*:\s*0'
```

3. If `detect_secrets_proto` keeps timing out, run it interactively with a longer timeout to debug:

```powershell
.venv\Scripts\python scripts/detect_secrets_proto.py --timeout 600
```

4. Verify candidate counts and a small sample (non-destructive):

```powershell
(Get-Content doc/sprints/analysis/candidates.ndjson).Length  # total lines (PowerShell)
python -c "import json,sys; print([json.loads(l)['type'] for l in [open('doc/sprints/analysis/candidates.ndjson').readline() for _ in range(3)]])"
```

5. Confirm prioritized checkpoint issues were created and review their mapping file:

```powershell
Get-Content doc/sprints/analysis/prioritized_issues/ISSUES_CREATED.ndjson -Tail 50
```

6. Confirm PR #105 merge metadata (read-only):

```powershell
gh pr view 105 --repo sbattywolf/GAIA --json number,state,title,author,mergedAt,mergedBy,mergeCommit,closingIssuesReferences
```

7. If everything above looks correct, record verification in the session trace or proceed to human triage for CHECKPOINTs. If any step shows failing behavior, pause the runner, run the failing command interactively, and capture logs for triage.

## Sprint freeze (2026-02-06)

- A sprint-freeze snapshot was recorded to `doc/sprints/SPRINT_2026-02-06_FROZEN.md` to preserve the current triage state.
- Session state saved to `.copilot/session_state.json` with `current_task_id` set to 9 (triage in-progress).
- To resume this sprint, open `doc/sprints/SPRINT_2026-02-06_FROZEN.md` and follow the `next_immediate_step` recorded in `.copilot/session_state.json`.

## Stopping background automation

- As requested, background runner processes should be stopped and PID files removed. Use the restart commands in the "Autonomous Runner (8-hour safe mode)" section above to resume when ready.

