param(
  [int]$Pr = 156,
  [string]$Repo = 'sbattywolf/GAIA',
  [int]$TimeoutSeconds = 600
)

$start = Get-Date
while ((Get-Date) -lt $start.AddSeconds($TimeoutSeconds)) {
  $res = gh pr view $Pr --repo $Repo --json number,state,mergeable,mergeStateStatus,statusCheckRollup | ConvertFrom-Json
  $notCompleted = $res.statusCheckRollup | Where-Object { $_.status -ne 'COMPLETED' }
  $fails = $res.statusCheckRollup | Where-Object { $_.status -eq 'COMPLETED' -and ($_.conclusion -ne 'SUCCESS') }
  Write-Output "PR $($res.number) state=$($res.state) mergeable=$($res.mergeable) status=$($res.mergeStateStatus) checks_not_completed=$($notCompleted.Count) failures=$($fails.Count)"
  if (($notCompleted.Count -eq 0) -and ($fails.Count -eq 0)) {
    Write-Output 'All checks passed — merging'
    gh pr merge $Pr --repo $Repo --merge --delete-branch --confirm
    break
  }
  Start-Sleep -Seconds 15
}
Write-Output 'Polling finished.'
