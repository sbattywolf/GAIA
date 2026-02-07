param(
  [string]$Repo = 'sbattywolf/GAIA',
  [string]$Branch = 'fix/add-audit-actor-migration',
  [int]$Interval = 30
)

Write-Output "Starting PR watcher for $Repo branch $Branch (interval ${Interval}s)"

while ($true) {
  try {
    $runsJson = gh run list --repo $Repo --branch $Branch --limit 30 --json databaseId,number,workflowName,status,conclusion,createdAt 2>$null
    if ($runsJson) {
      $runs = $runsJson | ConvertFrom-Json
      foreach ($r in $runs) {
        Write-Output ("ID=$($r.databaseId) workflow=$($r.workflowName) status=$($r.status) conclusion=$($r.conclusion) createdAt=$($r.createdAt)")
      }
    } else {
      Write-Output 'No runs yet.'
    }
  } catch {
    Write-Output "Failed to list runs: $($_.Exception.Message)"
  }

  try {
    & ./.github/scripts/fetch_failed_logs.ps1 -Repo $Repo -Branch $Branch
  } catch {
    Write-Output "fetch_failed_logs failed: $($_.Exception.Message)"
  }

  try {
    & ./.github/scripts/scan_logs.ps1
  } catch {
    Write-Output "scan_logs failed: $($_.Exception.Message)"
  }

  Start-Sleep -Seconds $Interval
}
