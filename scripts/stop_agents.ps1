<#
Stop agents started by `start_agents.ps1`.

Usage:
  ./scripts/stop_agents.ps1
#>
param(
  [string]$AgentId = ''
)

 $repoRoot = (Get-Location).Path
 $tmpDir = Join-Path $repoRoot '.tmp'
 $pidsFile = Join-Path $tmpDir 'agents_pids.json'
if (-not (Test-Path $pidsFile)) {
    Write-Host "No PID file found at $pidsFile"
    exit 0
}
 $json = Get-Content $pidsFile -Raw | ConvertFrom-Json

 # Build a map of recorded pids
 $pmap = @{}
 if ($json.pids) {
    foreach ($prop in $json.pids.PSObject.Properties) {
        $pmap[$prop.Name] = $prop.Value
    }
}

 # Determine which keys to stop
 $toStop = @()
 if ($AgentId -and $AgentId.Trim() -ne '') {
    # prefer exact match, else contains
    if ($pmap.ContainsKey($AgentId)) { $toStop += $AgentId }
    else {
      foreach ($k in $pmap.Keys) { if ($k.ToString().ToLower().Contains($AgentId.ToLower())) { $toStop += $k } }
    }
    if (-not $toStop -or $toStop.Count -eq 0) {
      Write-Host "No matching agent entries found for AgentId='$AgentId' in $pidsFile"
      exit 0
    }
} else {
    $toStop = $pmap.Keys
}

 # Stop running processes recorded under .pids (selected)
 foreach ($name in $toStop) {
    $val = $pmap[$name]
    $procId = $null
    if ($val -and $val.pid) { $procId = $val.pid }
    if ($procId) {
        try {
            Write-Host "Stopping $name (PID $procId)"
            Stop-Process -Id $procId -Force -ErrorAction Stop
        } catch {
            Write-Host ("Failed to stop PID {0}: {1}" -f $procId, $_)
        }
    }
    # remove from map
    $pmap.Remove($name) | Out-Null
}

 # Remove scheduled tasks if any were created
 if ($json.scheduled) {
    foreach ($prop in $json.scheduled.PSObject.Properties) {
        $taskName = $prop.Value
        try {
            Write-Host "Deleting scheduled task $taskName"
            schtasks.exe /Delete /TN $taskName /F | Out-Null
        } catch {
            Write-Host ("Failed to delete scheduled task {0}: {1}" -f $taskName, $_)
        }
    }
}

 # write back remaining pids or remove file
 if ($pmap.Count -eq 0) {
    try { Remove-Item $pidsFile -ErrorAction SilentlyContinue } catch {}
    Write-Host "Stopped agents and removed PID file"
} else {
    $out = @{ started = $json.started; pids = $pmap }
    $out | ConvertTo-Json -Depth 5 | Out-File -FilePath $pidsFile -Encoding utf8
    Write-Host "Stopped requested agents; remaining PIDs updated in $pidsFile"
}
