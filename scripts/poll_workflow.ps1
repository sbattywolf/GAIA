Param(
    [string]$workflow = 'repro-windows-integration-flake.yml',
    [int]$intervalMin = 10
)

$destRoot = ".tmp/artifacts"
if (-not (Test-Path $destRoot)) { New-Item -ItemType Directory -Path $destRoot | Out-Null }
$stopFile = ".tmp/stop_poll"
Write-Output "Starting poller for workflow '$workflow' (interval: $intervalMin min). Create $stopFile to stop."
while (-not (Test-Path $stopFile)) {
    try {
        $runsJson = gh run list --workflow $workflow --limit 100 --json id,status,conclusion,createdAt 2>$null
        if ($runsJson) {
            $runs = $runsJson | ConvertFrom-Json
            foreach ($r in $runs) {
                if ($r.status -ne 'completed') { continue }
                $runId = $r.id
                $localDir = Join-Path $destRoot $runId
                if (-not (Test-Path $localDir)) {
                    Write-Output "[poller] Downloading artifacts for run ${runId}..."
                    try {
                        gh run download ${runId} --dir ${localDir} 2>&1 | Tee-Object -FilePath ".tmp/gh_download_${runId}.txt"
                        Write-Output "[poller] Download finished for run ${runId} -> ${localDir}"
                    } catch {
                        Write-Output "[poller] Failed to download run ${runId}: $_"
                    }
                }
            }
        } else {
            Write-Output "[poller] 'gh' returned no runs or command failed."
        }
    } catch {
        Write-Output "[poller] Error: $_"
    }
    Start-Sleep -Seconds ($intervalMin * 60)
}
Write-Output "Poller stopped because ${stopFile} was found."
