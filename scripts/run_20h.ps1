Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$root = Resolve-Path ".." | Select-Object -ExpandProperty Path
Push-Location $root

Write-Output "Launching supervisor for a 20-hour run"
# Start supervisor in a new PowerShell process and record PID
$proc = Start-Process -FilePath pwsh -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File scripts/supervisor.ps1" -PassThru
$runPid = $proc.Id
Write-Output "Supervisor PID: $runPid"
if (Test-Path pids.json) { $p = Get-Content pids.json | ConvertFrom-Json } else { $p = @{} }
$p.run_20h = @{ pid = $runPid; started = (Get-Date).ToString('o') }
$p | ConvertTo-Json | Set-Content pids.json

# Sleep for 20 hours (72,000 seconds)
Write-Output "Supervisor will run for 20 hours (72000s)"
Start-Sleep -Seconds 72000

Write-Output "20-hour window elapsed — attempting graceful stop"
try {
    Stop-Process -Id $runPid -Force -ErrorAction SilentlyContinue
} catch {
    Write-Output "Supervisor process may have already exited"
}
Write-Output "Run complete"
Pop-Location
