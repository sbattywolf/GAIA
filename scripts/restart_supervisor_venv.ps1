$root = 'e:\Workspaces\Git\GAIA'
$ven_rel = @('.venv\Scripts\python.exe','venv\Scripts\python.exe','.env\Scripts\python.exe')
$ven_candidates = $ven_rel | ForEach-Object { Join-Path $root $_ }
$python = $ven_candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $python) {
    try { $python = (Get-Command python -ErrorAction Stop).Source } catch { $python = $null }
}
Write-Host "Using Python: $python"
Write-Host 'Stopping existing supervisor(s)'
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*monitor_supervisor.py*' }
if ($procs) {
    foreach ($p in $procs) {
        Write-Host "Killing PID $($p.ProcessId)"
        try { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue } catch {}
    }
} else { Write-Host 'No existing supervisor found' }
Start-Sleep -Seconds 1
if (-not $python) { Write-Host 'No python found to start supervisor'; exit 2 }
$proc = Start-Process -FilePath $python -ArgumentList "$root\scripts\monitor_supervisor.py","--host","127.0.0.1","--port","5000" -RedirectStandardOutput '.\.tmp\monitor_supervisor.log' -RedirectStandardError '.\.tmp\monitor_supervisor.err' -PassThru
Write-Host "Started supervisor pid=$($proc.Id)"
Start-Sleep -Seconds 2
Write-Host '=== supervisor log tail ==='
if (Test-Path '.\.tmp\monitor_supervisor.log') { Get-Content .\.tmp\monitor_supervisor.log -Tail 200 } else { Write-Host 'MISSING: .tmp/monitor_supervisor.log' }
Write-Host '=== supervisor.err tail ==='
if (Test-Path '.\.tmp\monitor_supervisor.err') { Get-Content .\.tmp\monitor_supervisor.err -Tail 200 } else { Write-Host 'MISSING: .tmp/monitor_supervisor.err' }
Write-Host '=== monitor_pid.txt ==='
if (Test-Path '.\.tmp\monitor_pid.txt') { Get-Content .\.tmp\monitor_pid.txt } else { Write-Host 'MISSING: .tmp/monitor_pid.txt' }
