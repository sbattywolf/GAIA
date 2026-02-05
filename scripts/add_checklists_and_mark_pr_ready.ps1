Set-Location -LiteralPath 'E:\Workspaces\Git\GAIA'
$issues = 16..22
foreach ($i in $issues) {
    Write-Host "Updating issue #$i..."
    $body = gh issue view $i --repo sbattywolf/GAIA --json body --jq .body
    $tmp = New-TemporaryFile
    $checklist = "`n`n- [ ] Confirm scope and acceptance criteria`n- [ ] Break into sub-tasks`n- [ ] Add owner and final estimate"
    Set-Content -Path $tmp -Value ($body + $checklist) -Encoding UTF8
    gh issue edit $i --repo sbattywolf/GAIA --body-file $tmp
    Remove-Item $tmp -ErrorAction SilentlyContinue
}

# Mark PR #15 ready and comment
gh pr ready 15 --repo sbattywolf/GAIA
gh pr comment 15 --repo sbattywolf/GAIA --body "Added checklists to sprint issues and marked PR #15 ready for review."
Write-Host 'Done.'
