param(
    [string]$Repo = 'sbattywolf/GAIA',
    [int]$Interval = 30,
    [int]$Timeout = 1800
)

$start = Get-Date
$tmpDir = ".tmp/run_logs"
if (-not (Test-Path $tmpDir)) { New-Item -ItemType Directory -Path $tmpDir | Out-Null }

Write-Output "Watching GH Actions runs for repo $Repo (poll every $Interval s)"

while ((Get-Date) -lt $start.AddSeconds($Timeout)) {
    try {
        $out = gh run list --repo $Repo --workflow CI --limit 50 2>$null
    } catch {
        Write-Output "gh run list failed: $_"
        Start-Sleep -Seconds $Interval
        continue
    }
    $lines = $out -split "`n"
    foreach ($line in $lines) {
        if ($line -match '^\s*(\d+)\s+') {
            $runId = $matches[1]
            $fn = "$tmpDir/run-$runId.log"
            if (-not (Test-Path $fn)) {
                Write-Output "Fetching logs for run $runId"
                gh run view $runId --repo $Repo --log > $fn 2>$null
                Write-Output "Saved $fn"
            }
        }
    }
    Start-Sleep -Seconds $Interval
}
Write-Output "Watcher finished (timeout)"