# GAIA Runbook (quick commands)

This file provides copy-paste ready commands to run and manage the GAIA approval listener, safely execute commands, run tests, and clean runtime artifacts.

1) Prepare environment

PowerShell (load `.tmp/telegram.env` into environment):

```powershell
$envFile = Join-Path -Path $PWD -ChildPath '.tmp/telegram.env'
if (Test-Path $envFile) {
  Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*([^#=]+)=(.*)$') {
      $k=$matches[1].Trim(); $v=$matches[2].Trim(); Set-Item -Path env:$k -Value $v
    }
  }
}
```

2) Start approval listener (background)

```powershell
Start-Process -NoNewWindow -FilePath python -ArgumentList 'scripts/approval_listener.py','--poll','5','--continue-on-approve' -PassThru
```

3) Stop listener

- Read PID: `Get-Content .tmp/approval_listener.pid` (if present)
- Kill process (Task Manager or `Stop-Process -Id <pid>` in PowerShell)

4) Approve / Deny / List (CLI)

```powershell
python scripts/tg_command_manager.py list
python scripts/tg_command_manager.py approve <id>
python scripts/tg_command_manager.py deny <id>
```

5) Safe execution (loads `.tmp/telegram.env` then runs command)

```powershell
python scripts/run_with_env.py -- python scripts/tg_command_manager.py execute <command-id> --execute
```

6) Check events & DB

```powershell
Get-Content events.ndjson -Tail 50
# or use PowerShell to inspect gaia.db with sqlite3
python - <<'PY'
import sqlite3
print(list(sqlite3.connect('gaia.db').cursor().execute('SELECT action,command_id,ts FROM command_audit ORDER BY id DESC LIMIT 10')))
PY
```

7) Cleanup runtime artifacts (dry-run first)

```powershell
python scripts/cleanup_tmp.py --archive --dry-run
# then to apply
python scripts/cleanup_tmp.py --archive --clean --yes
```

8) Run tests locally (venv)

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m pytest -q --basetemp .tmp/pytest
```

9) Notes & safety

- By default real execution is disabled. Set `ALLOW_COMMAND_EXECUTION=1` in `.tmp/telegram.env` to enable, and restrict `TELEGRAM_APPROVER_IDS` to trusted accounts.
- Dry-run executions emit both `command.executed.dryrun` and `command.executed` (payload includes `dry_run: true`).

---
Keep this file handy for operator copy-paste. Update `doc/HANDOFF.md` for longer procedures.
