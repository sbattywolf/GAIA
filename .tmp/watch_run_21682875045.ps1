$runId = 21682875045
while ($true) {
    $info = gh run view $runId --repo sbattywolf/GAIA 2>&1
    if ($info -match 'Status:\s+completed') {
        Write-Output "Run completed; fetching logs..."
        gh run view $runId --repo sbattywolf/GAIA --log
        break
    }
    Write-Output ("{0} - still running" -f (Get-Date -Format o))
    Start-Sleep -Seconds 15
}
