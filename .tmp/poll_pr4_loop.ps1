$max = 10
for ($i = 0; $i -lt $max; $i++) {
    Write-Output ("--- poll {0} ({1}) ---" -f $i, (Get-Date -Format o))
    gh run list --repo sbattywolf/GAIA --branch chore/online-agent-smoke-ci --limit 10
    Start-Sleep -Seconds 60
}
