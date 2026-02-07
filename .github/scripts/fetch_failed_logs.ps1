param(
  [string]$Repo = 'sbattywolf/GAIA',
  [string]$Branch = 'feat/implement-token-policy'
)

if (-not (Test-Path '.tmp')) { New-Item -ItemType Directory -Path '.tmp' | Out-Null }

Write-Output "Listing runs for branch $Branch"
$runsJson = gh run list --repo $Repo --branch $Branch --limit 200 --json databaseId,number,workflowName,status,conclusion,createdAt | Out-String
try {
  $runs = ConvertFrom-Json $runsJson
} catch {
  Write-Error "Failed to parse gh run list JSON: $_"
  exit 1
}

$failed = @()
if ($null -eq $runs) {
  Write-Output 'No runs returned.'
  exit 0
}
if ($runs -is [System.Array]) {
  $failed = $runs | Where-Object { $_.status -eq 'completed' -and $_.conclusion -ne 'success' }
} else {
  if ($runs.status -eq 'completed' -and $runs.conclusion -ne 'success') { $failed = @($runs) }
}

if ($failed.Count -eq 0) { Write-Output 'No completed failed runs found.'; exit 0 }

foreach ($r in $failed) {
  $out = ".tmp/run_db_$($r.databaseId).log"
  $err = ".tmp/run_db_$($r.databaseId).err"
  Write-Output "Saving run $($r.databaseId) $($r.workflowName) $($r.conclusion) -> $out"
  gh run view $($r.databaseId) --repo $Repo --log > $out 2> $err
}

Write-Output 'Completed fetching logs.'
