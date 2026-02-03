# Stop any listener on port 5000, start monitor detached, run start_agents.ps1
try {
    $conn = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($conn) {
        $pid = $conn.OwningProcess
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "Stopped pid $pid"
    } else {
        Write-Host "No listener on port 5000"
    }
} catch {
    Write-Host "Get-NetTCPConnection failed, falling back to netstat"
    $line = netstat -ano | findstr ":5000" | Select-Object -First 1
    if ($line) {
        $parts = $line -split '\\s+'
        $last = $parts[-1]
        if ($last) {
            Stop-Process -Id $last -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped pid $last"
        }
    } else {
        Write-Host "No listener found"
    }
}

Start-Sleep -Milliseconds 500

# locate python
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Host "python not found"; exit 1 }

# start monitor detached
Start-Process -FilePath $py -ArgumentList 'monitor/app.py' -WorkingDirectory (Get-Location)
Write-Host "Launched monitor"

Start-Sleep -Seconds 1

# run start_agents.ps1
& .\scripts\start_agents.ps1

Write-Host "start_agents completed"
