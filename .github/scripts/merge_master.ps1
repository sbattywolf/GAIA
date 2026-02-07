try {
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
} catch {
    Write-Error "Failed to determine current branch: $_"
    exit 1
}

Write-Output "Current branch: $branch"

Write-Output 'Fetching origin/master...'
git fetch origin master
if ($LASTEXITCODE -ne 0) {
    Write-Error 'git fetch failed'
    exit 1
}

Write-Output 'Checking out master and pulling latest (fast-forward only)...'
git checkout master
if ($LASTEXITCODE -ne 0) {
    Write-Error 'Failed to checkout master'
    exit 1
}

git pull --ff-only origin master
if ($LASTEXITCODE -ne 0) {
    Write-Output 'git pull --ff-only failed (continuing to attempt merge from remote master)'
}

Write-Output "Switching back to branch $branch"
git checkout $branch
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to checkout branch $branch"
    exit 1
}

Write-Output "Merging master into $branch"
git merge --no-edit master
$mergeExit = $LASTEXITCODE
if ($mergeExit -eq 0) {
    Write-Output 'Merge succeeded (no conflicts).'
} elseif ($mergeExit -eq 1) {
    Write-Output 'Merge completed with conflicts. Please resolve conflicts manually.'
} else {
    Write-Output "Merge returned exit code $mergeExit"
}

Write-Output 'Merge script completed.'
