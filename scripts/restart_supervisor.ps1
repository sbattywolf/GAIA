Write-Host 'Stopping existing supervisor(s)'
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*monitor_supervisor.py*' }
if ($procs) {
  foreach ($p in $procs) {
    Write-Host "Killing PID $($p.ProcessId)"
    try { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue } catch {}
  }
} else {
  Write-Host 'No existing supervisor found'
}
Start-Sleep -Seconds 1
$python = (Get-Command python).Source
$proc = Start-Process -FilePath $python -ArgumentList 'e:\Workspaces\Git\GAIA\scripts\monitor_supervisor.py','--host','127.0.0.1','--port','5000' -RedirectStandardOutput '.\.tmp\monitor_supervisor.log' -RedirectStandardError '.\.tmp\monitor_supervisor.err' -PassThru
Write-Host "Started supervisor pid=$($proc.Id)"
Start-Sleep -Seconds 1
Write-Host '=== supervisor log tail ==='
if (Test-Path '.\.tmp\monitor_supervisor.log') { Get-Content .\.tmp\monitor_supervisor.log -Tail 50 } else { Write-Host 'MISSING: .tmp/monitor_supervisor.log' }
Write-Host '=== monitor_pid.txt ==='
if (Test-Path '.\.tmp\monitor_pid.txt') { Get-Content .\.tmp\monitor_pid.txt } else { Write-Host 'MISSING: .tmp/monitor_pid.txt' }
