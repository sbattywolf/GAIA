param(
  [string]$Repo = 'sbattywolf/GAIA'
)

Write-Output "Fetching remote branches (prune)..."
git fetch --prune origin

$refs = git for-each-ref --format='%(refname:short)' refs/remotes/origin
$branches = @()
foreach ($r in $refs) {
  $b = $r -replace '^origin/',''
  if ($b -and $b -ne 'HEAD' -and $b -ne 'master') { $branches += $b }
}

if (-not $branches) {
  Write-Output "No remote branches to delete."
  exit 0
}

foreach ($b in $branches) {
  Write-Output "\n---\nProcessing branch: $b"
  try {
    $prnums = gh pr list --repo $Repo --head $b --state open --jq '.[].number' 2>$null
  } catch {
    $prnums = $null
  }
  if ($prnums) {
    $prlist = $prnums -split "`n" | Where-Object { $_ }
    foreach ($p in $prlist) {
      Write-Output "Closing PR #$p for branch $b"
      gh pr close $p --repo $Repo --comment 'Closed by automation: cleaning stale branches' 2>$null
    }
  } else {
    Write-Output "No open PRs for branch $b"
  }

  Write-Output "Deleting remote branch origin/$b"
  gh api -X DELETE repos/$Repo/git/refs/heads/$b 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Output "gh api delete failed, trying git push --delete $b"
    git push origin --delete $b 2>$null
  }

  if (git show-ref --verify --quiet refs/heads/$b) {
    Write-Output "Deleting local branch $b"
    git branch -D $b 2>$null
  } else {
    Write-Output "No local branch $b"
  }
}

Write-Output "Cleanup complete."