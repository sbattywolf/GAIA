param(
    [string]$Repo = "sbattywolf/GAIA",
    [int]$PrNumber = 15
)

$issues = @(
    @{ title = 'Stabilize pre-prod E2E (8pt)'; body = 'Estimate: 8 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:high' },
    @{ title = 'Create GitHub Environments & secret separation (5pt)'; body = 'Estimate: 5 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:high' },
    @{ title = 'Coordinate secret rotation runbook (5pt)'; body = 'Estimate: 5 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:high' },
    @{ title = 'Audit & update key docs (5pt)'; body = 'Estimate: 5 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:medium' },
    @{ title = 'Implement rotation pilot runner (8pt)'; body = 'Estimate: 8 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:medium' },
    @{ title = 'Telegram notifications: stats & frequency (3pt)'; body = 'Estimate: 3 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:low' },
    @{ title = 'Cleanup archived docs (2pt)'; body = 'Estimate: 2 pts. See planner/sprint-1.md and PR #15'; labels = 'sprint/1,priority:low' }
)

$created = @()

foreach ($i in $issues) {
    $tmp = New-TemporaryFile
    try {
        Set-Content -Path $tmp -Value $i.body -Encoding UTF8
        $cmd = @('issue','create','--repo',$Repo,'--title',$i.title,'--body-file',$tmp,'--label',$i.labels)
        Write-Host "Running: gh $($cmd -join ' ' )"
        $out = gh @cmd 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to create issue: $out" -ForegroundColor Red
        } else {
            $created += $out.Trim()
            Write-Host "Created: $out" -ForegroundColor Green
        }
    } finally {
        Remove-Item $tmp -ErrorAction SilentlyContinue
    }
}

if ($created.Count -gt 0) {
    $body = "Linked sprint-1 issues:`n`n" + ($created -join "`n")
    Write-Host "Commenting on PR #$PrNumber with created issue links..."
    gh pr comment $PrNumber --repo $Repo --body $body
    Write-Host "Done."
} else {
    Write-Host "No issues were created. Aborting PR comment." -ForegroundColor Yellow
}
