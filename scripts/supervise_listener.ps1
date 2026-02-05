<#
Simple supervisor to start the approval listener and write PID.
Run this in PowerShell. It will start the listener and return; it does not loop.
For a restart-loop supervisor, wrap this script using a Windows Scheduled Task or service wrapper.
#>
$envFile = Join-Path -Path $PWD -ChildPath '.tmp/telegram.env'
if (Test-Path $envFile) {
  Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*([^#=]+)=(.*)$') { $k=$matches[1].Trim(); $v=$matches[2].Trim(); Set-Item -Path env:$k -Value $v }
  }
}

# start the listener and capture the process
# Use env_loader so listener reliably inherits envs from .tmp/telegram.env
$launcher = Join-Path $PWD 'scripts\env_loader.py'
$argList = @($launcher, '--env', '.tmp/telegram.env', '--', 'python', 'scripts\approval_listener.py', '--poll', '5', '--continue-on-approve')
$proc = Start-Process -FilePath python -ArgumentList $argList -PassThru
# write pid file
$pidFile = Join-Path -Path $PWD -ChildPath '.tmp/approval_listener.pid'
New-Item -ItemType Directory -Path (Split-Path $pidFile) -Force | Out-Null
Set-Content -Path $pidFile -Value $proc.Id -Encoding utf8
Write-Output "Started approval_listener.py pid=$($proc.Id)"

# Optionally wait a few seconds and show basic health
Start-Sleep -Seconds 1
$hf = Join-Path -Path $PWD -ChildPath '.tmp/telegram_health.json'
if (Test-Path $hf) { Write-Output "Health:"; Get-Content $hf -Raw }
