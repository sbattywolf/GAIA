# Auto triage and prioritize open issues
# Generates doc/sprints/analysis/prioritized-issues.ndjson and .csv
# Updates issue labels, assignees and milestone (Sprint 1) where appropriate.

$issuesFile = "doc/sprints/analysis/backlog-issues.ndjson"
$outNdjson = "doc/sprints/analysis/prioritized-issues.ndjson"
$outCsv = "doc/sprints/analysis/prioritized-issues.csv"
$milestone = "Sprint 1"
$defaultAssignee = "sbattywolf"

if (-not (Test-Path $issuesFile)) {
    Write-Error "Issues file not found: $issuesFile"
    exit 1
}

Remove-Item -Force -ErrorAction SilentlyContinue $outNdjson, $outCsv

"number,title,priority,est_hours,suggested_assignee,sprint_suggestion" | Out-File $outCsv -Encoding utf8

Get-Content $issuesFile | ForEach-Object {
    $issue = $_ | ConvertFrom-Json
    $num = $issue.number
    $title = $issue.title
    $body = $issue.body -join " "
    $labels = @($issue.labels | ForEach-Object { $_.name })

    # Determine priority
    $priority = $null
    if ($labels -contains 'critical') { $priority = 'critical' }
    elseif ($labels -contains 'high') { $priority = 'high' }
    elseif ($labels -contains 'medium') { $priority = 'medium' }
    elseif ($labels -contains 'low') { $priority = 'low' }
    else {
        $txt = ($title + ' ' + $body).ToLower()
        if ($txt -match 'token|secret|leak|purge|filter-repo') { $priority = 'critical' }
        elseif ($txt -match 'ci|workflow|pytest|basetemp|importable') { $priority = 'high' }
        elseif ($txt -match 'e2e|integration|mock') { $priority = 'high' }
        elseif ($txt -match 'test|flak') { $priority = 'high' }
        else { $priority = 'medium' }
    }

    switch ($priority) {
        'critical' { $est = 24 }
        'high' { $est = 16 }
        'medium' { $est = 8 }
        'low' { $est = 4 }
        default { $est = 8 }
    }

    $suggested = ''
    if ($priority -in @('critical','high')) { $suggested = $defaultAssignee }
    $sprint = if ($priority -in @('critical','high')) { 'Sprint 1' } else { 'backlog' }

    # Prepare label additions
    $addLabels = @()
    if (-not ($labels -contains $priority)) { $addLabels += $priority }
    # ensure epic tags (ci/testing/security/integration) preserved - don't remove existing labels

    # Update GitHub issue: add labels and assignee and milestone for critical/high
    $cmd = @()
    foreach ($l in $addLabels) { $cmd += "--add-label $l" }
    if ($suggested) { $cmd += "--add-assignee $suggested" }
    if ($sprint -eq 'Sprint 1') { $cmd += "--milestone '$milestone'" }

    if ($cmd.Count -gt 0) {
        $cmdLine = "gh issue edit $num " + ($cmd -join ' ')
        Write-Output ("Updating issue {0}: {1}" -f $num, $cmdLine)
        iex $cmdLine
    }

    # Write outputs
    $outObj = [PSCustomObject]@{
        number = $num
        title = $title
        priority = $priority
        est_hours = $est
        suggested_assignee = $suggested
        sprint_suggestion = $sprint
        labels = ($labels -join ';')
    }
    $json = $outObj | ConvertTo-Json -Compress
    $json | Out-File -FilePath $outNdjson -Append -Encoding utf8

    "{0},{1},{2},{3},{4},{5}" -f $num,('"' + ($title -replace '"','""') + '"'),$priority,$est,$suggested,$sprint | Out-File -FilePath $outCsv -Append -Encoding utf8
}

Write-Output "Wrote $outNdjson and $outCsv"
