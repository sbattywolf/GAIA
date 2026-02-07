param(
  [string]$Repo = 'sbattywolf/GAIA',
  [string]$Branch = 'feat/implement-token-policy'
)

Write-Output "Listing runs for branch $Branch"
$runsJson = gh run list --repo $Repo --branch $Branch --limit 200 --json databaseId,status,conclusion,workflowName | Out-String
$runs = ConvertFrom-Json $runsJson
foreach ($r in $runs) {
  if ($r.conclusion -eq 'FAILURE') {
    Write-Output "Requesting rerun for run $($r.databaseId) - $($r.workflowName)"
    gh run rerun $($r.databaseId) --repo $Repo
  }
}
Write-Output 'Done.'
