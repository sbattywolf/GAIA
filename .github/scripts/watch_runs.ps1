param(
    [Parameter(Mandatory=$true)] [string] $Repo,
    [Parameter(Mandatory=$true)] [string] $Branch,
    [int] $IntervalSeconds = 30
)

Write-Output "Starting background watcher for branch $Branch in repo $Repo"
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
        Write-Output 'Failed to list runs: ' + $_.Exception.Message
    }

    try {
        $fetchScript = Join-Path $PSScriptRoot 'fetch_failed_logs.ps1'
        if (Test-Path $fetchScript) {
            & $fetchScript -Repo $Repo -Branch $Branch
        } else {
            Write-Output "Fetch script not found: $fetchScript"
        }
    } catch {
        Write-Output 'fetch_failed_logs script failed: ' + $_.Exception.Message
    }

    try {
        $scanScript = Join-Path $PSScriptRoot 'scan_logs.ps1'
        if (Test-Path $scanScript) {
            & $scanScript
        } else {
            Write-Output "Scan script not found: $scanScript"
        }
    } catch {
        Write-Output 'scan_logs script failed: ' + $_.Exception.Message
    }

    Start-Sleep -Seconds $IntervalSeconds
}
