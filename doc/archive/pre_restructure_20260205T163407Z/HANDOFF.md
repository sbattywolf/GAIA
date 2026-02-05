Gaia — Handoff for a new chat session

Date: 2026-02-02

Purpose
- Move active work to a fresh chat thread and keep this session clean.
- Provide the new chat with everything needed to resume: context, commands, files, and a suggested starting prompt.

Quick resume steps
1. Open the repository root and the Gaia docs:
   - `Gaia/doc/CONCEPT.md`
   - `Gaia/doc/SESSION_SUMMARY.md`
   - `Gaia/doc/media/dashboard-mock.png`
   - `Gaia/doc/media/telegram-flow.png`
2. Start the development venv (if not already):
```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```
3. Start the prototype SSE server for local debugging (optional):
```powershell
set PROTOTYPE_USE_LOCAL_EVENTS=1
python AGENT_TASKS\agent_runtime\monitoring_prototype\serve_prototype_with_data.py
```
4. Open `http://localhost:8001/` and use the Stream Debug panel (Init Footer Stream, Start Stream).

Key files to review
- `AGENT_TASKS/agent_runtime/alby_0_2/scripts/send_chat_message.py` — event emitter
- `AGENT_TASKS/agent_runtime/monitoring_prototype/serve_prototype_with_data.py` — SSE tailer/server
- `AGENT_TASKS/agent_runtime/monitoring_prototype/index.html` — debug UI
- `Gaia/doc/CONCEPT.md` — concept, workflows, and next steps
- `Gaia/doc/SESSION_SUMMARY.md` — recent snapshot and resume commands

Suggested new-chat starter prompt
```
I want to continue the Gaia agent backlog work. Resume from the last snapshot in this repo. Key files: Gaia/doc/CONCEPT.md, Gaia/doc/SESSION_SUMMARY.md. Start by scaffolding `Gaia/agents/backlog_agent.py` that uses the `gh` CLI to create and update issues and writes NDJSON events to `Gaia/events.ndjson`. Make sure actions are idempotent and produce audit entries in SQLite.
```

Notes for the new chat
- The prototype server was stopped and a session snapshot was created (`SESSION_CHANGES.txt`).
- Two wireframe PNGs were generated under `Gaia/doc/media/` for the dashboard and Telegram flow.
- If you want me to continue the work in this same machine, open a new chat and paste the suggested starter prompt above; I will scaffold the agents and run small tests locally.

-- end of handoff

Additional quick test (added 2026-02-03):

- A fake pending command was created to exercise on-reply approval routing and monitoring. Task name: `FAKE_ONREPLY_TEST_2026`, id: `fa1cde9e-1234-4bcd-8f1a-0fa1cde00001`.
- The pending item lives in `.tmp/pending_commands.json` and is marked with `is_test` so UI and bot flows will treat it as a test (Proceed disabled until explicitly allowed).

When handing off, mention this test id so the next operator can validate Telegram approval and on-reply behavior.

Don Ciccio - online agent

**Child-doc pattern for follow-ups**

When you want to propose follow-up tasks without modifying the parent story, create a child doc using this pattern:

- `doc/<StoryName>.<AgentName>.<TodoTaskName>.extra.md`

Include a `Parent: <StoryName>` header and brief acceptance criteria. During the next iteration, collect these child docs and add them to the parent TODO list for triage.


**Alert delivery preference**

Per current decision: prefer Telegram-first delivery for alerts (use `TELEGRAM_NOTIFY_CHAT` / `CHAT_ID` in `.tmp/telegram.env`). If Telegram is unavailable, the script falls back to console output; future iterations may add webhook or external monitoring fallbacks.

**Auto-requeue runbook**

Use `scripts/auto_requeue.py` to safely requeue eligible permanent failures back into the retry queue. Defaults are conservative (max 3 retries, 72 hours age, max 10 items per run). Example dry-run:

```powershell
$env:PYTHONPATH='.'; python scripts/auto_requeue.py --dry-run
```

To actually requeue:

```powershell
$env:PYTHONPATH='.'; python scripts/auto_requeue.py
```

Adjust policy with environment vars:

- `AUTO_REQUEUE_MAX_RETRIES` (default 3)
- `AUTO_REQUEUE_MAX_AGE_HOURS` (default 72)
- `AUTO_REQUEUE_MAX_PER_RUN` (default 10)

**Monitor UI admin guard**

The monitor includes an admin requeue API at `POST /admin/requeue`. Protect it with an admin token by setting `MONITOR_ADMIN_TOKEN` in `.tmp/telegram.env` or the environment. The server accepts the token via header `X-Admin-Token` or query param `?token=`. Example:

```powershell
# dry-run: just view pending
python -m scripts.monitor_server --host 127.0.0.1 --port 8080

# requeue index 0 using token
curl -X POST "http://127.0.0.1:8080/admin/requeue?token=YOUR_TOKEN" -H "Content-Type: application/json" -d '{"index":0}'
```


**Claim locking and concurrency**

The agent claim primitives in `scripts/claims.py` use a simple file-lock pattern to ensure at-most-once semantics when multiple agents attempt to claim the same story/todolist concurrently.

- Lock file location: the lock for a claim file lives next to the claim file with the suffix `.lock`. Example:

   - Claim file: `.tmp/claims/<story>.<todolist>.json`
   - Lock file: `.tmp/claims/<story>.<todolist>.json.lock`

- Lock semantics:
   - The code uses an exclusive-create pattern (`os.O_CREAT | os.O_EXCL`) to atomically create the lock file. This blocks other claimers by returning a `FileExistsError` when the lock already exists.
   - Lock acquisition attempts for claim/release/refresh operations retry for a short default timeout (5s). If the lock cannot be acquired within the timeout the operation returns a `lock-timeout` result so callers can retry or surface an error.
   - The lock protects the entire read-modify-write (RMW) sequence: callers read any existing claim, decide whether takeover is allowed (TTL expiry), and then write the new claim object atomically. Holding the lock for the full RMW prevents the classic race where two agents read "no existing claim" and both write.
   - The lock is released in a `finally` block so it's robust against exceptions in the critical section.

- Claim write atomicity:
   - Claim writes use a temp-file + `os.replace()` pattern with an fsync on the temp file to ensure durable writes before the atomic rename.
   - On Windows this was a source of races (PermissionError) under heavy concurrency; the lock-file pattern remedies that by serializing access to the rename step and the surrounding RMW.

- Operator guidance & CLI examples:
   - To inspect a claim (JSON output):

      ```powershell
      python -c "from scripts.claims import inspect_claim; import json; print(json.dumps(inspect_claim('my_story','default'), indent=2))"
      ```

   - To attempt a claim (returns `(success, payload_or_reason)`):

      ```powershell
      python -c "from scripts.claims import claim; import json; print(claim('my_story','default','operator','agent-1','fp-123'))"
      ```

   - To release a claim:

      ```powershell
      python -c "from scripts.claims import release; print(release('my_story','default', agent_id='agent-1'))"
      ```

- Troubleshooting:
   - If an operation returns `lock-timeout` the operator can either retry the action after a short delay or inspect the lock file. Example:

      ```powershell
      dir .tmp\claims\my_story.*.json.lock
      type .tmp\claims\my_story.*.json.lock  # lock files are empty, presence is the signal
      ```

   - Stale locks: if the lock file persists due to a crashed process, remove it manually after verifying no active agent is running the claim operation:

      ```powershell
      del .tmp\claims\my_story.*.json.lock
      ```

   - Tests: concurrency behavior is exercised by `tests/test_claims_concurrency.py`. Run the test suite to validate race fixes locally on Windows and Linux:

      ```powershell
      $env:PYTHONPATH='.'; pytest -q tests/test_claims_concurrency.py -q --basetemp .tmp/pytest
      ```

   - Audit traces: claim actions emit audit traces to `gaia.db` (see `gaia.db.write_trace()` and `tail_traces()`) so you can correlate who acquired or released a claim.

The locking pattern is intentionally simple and filesystem-backed so it works across processes and survives agent restarts. If you need stronger guarantees at scale consider using a single-node coordination service (e.g., SQLite advisory locks, Redis, or a small leader/coordinator process).



**Alert script (runbook)**

Use `scripts/alert_on_metrics.py` to run a periodic check of metrics. Example PowerShell invocation (dry-run):

```powershell
$env:PYTHONPATH='.'; python scripts/alert_on_metrics.py --dry-run
```

To run with default thresholds and actually notify via Telegram (requires `.tmp/telegram.env` with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_NOTIFY_CHAT`):

```powershell
$env:PYTHONPATH='.'; python scripts/alert_on_metrics.py
```

Customize thresholds:

```powershell
python scripts/alert_on_metrics.py --threshold telegram.retry.moved_permanent=2 --threshold telegram.retry.attempt.error=20
```


Behavior change (2026-02-03):

**Runbook (expanded)**

- **Prepare environment**: ensure `.tmp/telegram.env` exists and contains at minimum:
   - `TELEGRAM_BOT_TOKEN` — bot token
   - `CHAT_ID` or `TELEGRAM_NOTIFY_CHAT` — admin chat to notify
   - `ALLOW_COMMAND_EXECUTION=0` (default) or `1` to enable real execution
   - `TELEGRAM_APPROVER_IDS` — comma-separated Telegram user IDs allowed to approve

- **Start the approval listener (PowerShell)**

```powershell
$envFile = Join-Path -Path $PWD -ChildPath '.tmp/telegram.env'
if (Test-Path $envFile) { Get-Content $envFile | ForEach-Object { if ($_ -match '^(?:\s*#)?\s*([^=]+)=(.*)$') { $k=$matches[1].Trim(); $v=$matches[2].Trim(); Set-Item -Path env:$k -Value $v } } }
Start-Process -NoNewWindow -FilePath python -ArgumentList 'scripts/approval_listener.py','--poll','5','--continue-on-approve' -PassThru
```

- **Stop the listener**: locate PID in `.tmp/approval_listener.pid` and stop the process (or use Task Manager on Windows). Remove `.tmp/approval_listener.pid` when stopped.

- **Run commands safely (avoid REPL quoting issues)**: use the safe runner to load `.tmp/telegram.env` and execute a CLI script.

```powershell
python scripts/run_with_env.py -- python scripts/tg_command_manager.py execute <command-id> --execute
```

- **Approve / deny via CLI** (local manual override):

```powershell
python scripts/tg_command_manager.py approve <id>
python scripts/tg_command_manager.py deny <id>
python scripts/tg_command_manager.py list
```

- **Check traces & events**:
   - Tail `events.ndjson` to observe `approval.requested`, `command.approved`, `command.executed(.dryrun)`, and audit events.
   - Inspect `gaia.db` `command_audit` table for matching rows.

- **Cleanup runtime artifacts** (dry-run first):

```powershell
python scripts/cleanup_tmp.py --archive --dry-run
# then to apply
python scripts/cleanup_tmp.py --archive --clean --yes
```

- **Run tests locally** (dev environment):

```powershell
# create venv (if needed)
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt  # contains pytest
python -m pytest -q --basetemp .tmp/pytest
```

- **Supervision & deployment notes**:
   - For production-like runs, supervise `scripts/approval_listener.py` with a Windows Scheduled Task, NSSM service wrapper, or a monitored background process.
   - Ensure `.tmp/telegram.env` permissions are restricted and maintain `.tmp/telegram.env.bak` for emergency rollback.

- **Emergency rollback**:
   - If a listener misbehaves, stop the process, archive `.tmp` (`scripts/cleanup_tmp.py`), and inspect `events.ndjson` + `gaia.db` for audit records before restarting.

- **CI suggestion**:
   - Add a lightweight GitHub Actions job that installs test deps and runs `pytest -q --basetemp .tmp/pytest` to validate changes in PRs.

Quick monitor & recovery commands (operators)

- Start monitor UI locally:

```powershell
python -m scripts.monitor_server --host 127.0.0.1 --port 8080
# open http://127.0.0.1:8080
```

- Inspect and requeue failed Telegram replies:

```powershell
python scripts/telegram_queue_admin.py --list
python scripts/telegram_queue_admin.py --requeue <index_or_id>
```

- Run approval listener (background):

```powershell
Start-Process -NoNewWindow -FilePath python -ArgumentList 'scripts/approval_listener.py','--poll','5','--continue-on-approve' -PassThru
```

-- end runbook additions

**Closure Note (2026-02-03)**

- **Story Extra (candidate for next iteration)**: Add a scoped story named "Improve observability & automated remediation" that implements: (1) additional metrics counters for duplicate skips, requeues, retry attempts, and permanent-failed growth; (2) a small alert script that can be run as a scheduled check (PowerShell / cron) which reads `.tmp/metrics.json` and raises an operator notification if thresholds are exceeded; (3) a lightweight dashboard that surfaces permanent-failed items and allows one-click requeue. This story should be evaluated next iteration and broken into 2–3 tickets.

- **Acceptance criteria:**
   - Metrics counters exist and are emitted for requeue, duplicate-skip, retry attempts, and permanent failures.
   - An alert script `scripts/alert_on_metrics.py` (or PowerShell equivalent) can be run manually and triggers when thresholds are exceeded.
   - A minimal UI page under the monitor that lists permanent failed items and provides a requeue action which calls `telegram_queue_admin.py --requeue`.
   - Tests cover metrics persistence and alert script behavior; CI runs these checks.

- **Conflicts / open questions (to review later):**
   - Where should alerting notifications surface (Telegram notify chat vs external monitoring)?
   - Allowed scope for automatic requeue (manual review vs auto-retry policy).
   - Privilege model for requeue UI actions (who is allowed to requeue/remove permanent items?).

- **Archived snapshot:**
   - Snapshot of `.tmp` taken at close: move `.tmp` to `.tmp.archive.20260203` before branching for the next iteration. Keep `events.ndjson` append-only and preserve `gaia.db` in backups.

Don Ciccio - online agent

**Story finalization note (stoybl bl bl 1)**

- Archived the active `.current` todolist to `.tmp/todolists/archive/stoybl_bl_bl_1.TD-stoybl_bl_bl_1.assistant.TD-stoybl_list.archived.2026-02-03T000000Z.json`.
- Created a reusable TODO template at `doc/TODO_TEMPLATE.md` based on the runbook 'Working the Todo List' guidance.
- Created a fresh `.current` todolist for the next phase at `.tmp/todolists/stoybl_bl_bl_1.TD-assistant.TD-stoybl_list.current` with `t3` marked in-progress.
- This finalization step follows the runbook: archive runtime snapshots, add closure note, and continue with prioritized next tasks.

**Enforcing the Final Task (tooling)**

To make the "finalization" step actionable and easily validated across operators, a small helper script was added: `scripts/enforce_todolist_final.py`.

- Validate current todo lists (ensure final task contains `MANDATORY`, `FINAL`, or `FINALIZATION`):

```powershell
python scripts/enforce_todolist_final.py --validate
```

- Create a `.finalized` marker after manual verification (prevents accidental appends):

```powershell
python scripts/enforce_todolist_final.py --finalize
```

The script looks under `.tmp/todolists/*.current`, prints the last task for each file, and returns a non-zero exit code if a final marker is missing. Operators should run `--validate` before archiving and `--finalize` once they are ready to mark the story closed.
