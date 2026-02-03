# Supervisor & Deployment Notes (Windows-focused)

This document contains quick, copyable recipes to run `scripts/approval_listener.py` and `scripts/process_telegram_queue.py` as persistent services on a Windows development machine. It also includes simple health-check rules operators can use.

## Recommended approach (development)

- Use a scheduled background process or `Start-Process` to launch the Python scripts. Keep environment values in `.tmp/telegram.env` and load them before starting.

PowerShell example (start listener detached):

```powershell
#$envFile loading helper (populate process env from file)
#$envFile = Join-Path -Path $PWD -ChildPath '.tmp/telegram.env'
if (Test-Path $envFile) { Get-Content $envFile | ForEach-Object { if ($_ -match '^(?:\\s*#)?\\s*([^=]+)=(.*)$') { $k=$matches[1].Trim(); $v=$matches[2].Trim(); Set-Item -Path env:$k -Value $v } } }

# start approval listener as a background process
Start-Process -NoNewWindow -FilePath python -ArgumentList 'scripts/approval_listener.py','--poll','5','--continue-on-approve' -PassThru

# start retry worker
Start-Process -NoNewWindow -FilePath python -ArgumentList 'scripts/process_telegram_queue.py' -PassThru
```

## Supervisors & service wrappers

- For a more robust approach, use an external process manager such as NSSM (Non-Sucking Service Manager) to wrap Python scripts as Windows services. NSSM supports stdout/stderr capture and restart on failure.

NSSM quick steps:

1. Download NSSM and place `nssm.exe` on PATH.
2. Create a service: `nssm install gaia-approval "C:\\Path\\to\\python.exe" "C:\\path\\to\\repo\\scripts\\approval_listener.py --poll 5 --continue-on-approve"`
3. Configure stdout/stderr file paths and autostart options in the NSSM UI.

## Health checks and alerts

- Heartbeat: the listener writes `.tmp/telegram_health.json`. Alert if `running` is false or `last_seen` is older than a configurable threshold (e.g., 2x polling interval).
- Failed queue growth: monitor the size of `.tmp/telegram_queue_failed.json` and trigger an alert if it grows above a threshold (e.g., >5 items in 5 minutes).

Example check (PowerShell):

```powershell
# check heartbeat freshness
$h = Get-Content .tmp/telegram_health.json | ConvertFrom-Json
if (-not $h.running -or [datetime]::Parse($h.last_seen) -lt (Get-Date).AddMinutes(-10)) { Write-Error 'approval listener unhealthy' }

# check failed queue size
$f = Get-Content .tmp/telegram_queue_failed.json | ConvertFrom-Json
if ($f.Length -gt 5) { Write-Error 'failed queue growth detected' }
```

## Files & permissions

- Keep `.tmp/telegram.env` restricted (Windows ACL) so tokens are not world-readable.
- Rotate or archive `.tmp` files periodically; keep `events.ndjson` append-only and *never* rewrite it.

## Restart & rollback

- On misbehavior: stop the supervisor, move `.tmp` to an archive folder (timestamped), inspect `events.ndjson` and `gaia.db`, then restart services.

```powershell
Move-Item -Path .tmp -Destination .tmp.archive.$((Get-Date).ToString('yyyyMMddHHmmss'))
Start-Process -NoNewWindow -FilePath python -ArgumentList 'scripts/approval_listener.py','--poll','5','--continue-on-approve' -PassThru
```

## Systemd (Linux) example

If you run GAIA on Linux, a simple `systemd` unit for `approval_listener` could look like:

```ini
[Unit]
Description=GAIA Approval Listener
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/repo
ExecStart=/usr/bin/python3 scripts/approval_listener.py --poll 5 --continue-on-approve
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable with:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gaia-approval.service
```

## Notes

- These are development-focused recipes. For production, add logging, structured metrics, and integrate with your platform's alerting/observability stack.
