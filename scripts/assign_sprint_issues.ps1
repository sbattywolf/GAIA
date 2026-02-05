# Assign sprint issues 16-22 to the main collaborator
$Repo = 'sbattywolf/GAIA'
$assignee = 'sbattywolf'
$issues = 16..22
foreach ($i in $issues) {
    Write-Host "Assigning issue #$i to $assignee"
    gh issue edit $i --repo $Repo --add-assignee $assignee
}
# Comment on PR #15
gh pr comment 15 --repo $Repo --body "Assigned sprint issues to @$assignee for initial triage and breakdown."
