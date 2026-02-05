Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$root = Resolve-Path ".." | Select-Object -ExpandProperty Path
Push-Location $root

function Write-PidFile($thePid){
    $pids = @{}
    if (Test-Path pids.json) { $pids = (Get-Content pids.json | ConvertFrom-Json) }
    $pids.automation_runner = $thePid
    $pids | ConvertTo-Json | Set-Content pids.json
}

$backoff = 1
while ($true) {
    Write-Output "Starting automation_runner.py"
    $proc = Start-Process -FilePath "python" -ArgumentList "scripts/automation_runner.py" -PassThru -WindowStyle Hidden
    Write-PidFile($proc.Id)
    $proc.WaitForExit()
    $exit = $proc.ExitCode
    Write-Output "automation_runner exited with code $exit"
    if ($exit -eq 0) { Write-Output 'Clean exit; restarting immediately'; $backoff = 1; continue }
    Write-Output "Restarting after $backoff seconds backoff"
    Start-Sleep -Seconds $backoff
    $backoff = [Math]::Min($backoff * 2, 300)
}

Pop-Location
