$files = Get-ChildItem -Path .tmp -Filter 'run_db_*.log' -File -ErrorAction SilentlyContinue
if (-not $files) {
  Write-Output 'No log files found.'
  exit 0
}

$patterns = @(
  @{name='detect-secrets'; pat='detect-secrets'},
  @{name='detect-secrets-flag'; pat='unrecognized arguments: --json'},
  @{name='heredoc'; pat='here-document'},
  @{name='syntax-end'; pat='syntax error: unexpected end of file'},
  @{name='pytest-basetemp-missing'; pat='.tmp/pytest'},
  @{name='FileNotFoundError'; pat='FileNotFoundError'},
  @{name='No such file or directory'; pat='No such file or directory'},
  @{name='sqlite-actor'; pat='table audit has no column named actor'},
  @{name='OperationalError'; pat='sqlite3.OperationalError'},
  @{name='Traceback'; pat='Traceback (most recent call last)'},
  @{name='gh-error'; pat='##[error]'}
)

$reportPath = '.tmp/log_scan_report.txt'
"" | Out-File $reportPath -Encoding utf8
Add-Content $reportPath "Log scan report - $(Get-Date -Format o)"
Add-Content $reportPath "Scanned files: $($files.Count)"
Add-Content $reportPath ""

foreach ($p in $patterns) {
  $matches = Select-String -Path ($files | ForEach-Object { $_.FullName }) -Pattern $p.pat -SimpleMatch -ErrorAction SilentlyContinue
  $count = if ($matches) { $matches.Count } else { 0 }
  $filesWith = if ($matches) { ($matches | Select-Object -ExpandProperty Path -Unique) } else { @() }
  $sample = if ($matches) { ($matches | Select-Object -First 3 | ForEach-Object { $_.Path + ':' + $_.LineNumber + ' -> ' + ($_.Line.Trim()) }) } else { @() }

  Add-Content $reportPath "Pattern: $($p.name) ('$($p.pat)')"
  Add-Content $reportPath "  Matches: $count"
  if ($filesWith.Count -gt 0) {
    Add-Content $reportPath "  Files:"
    foreach ($f in $filesWith) { Add-Content $reportPath "    - $f" }
  } else {
    Add-Content $reportPath "  Files: (none)"
  }
  if ($sample.Count -gt 0) {
    Add-Content $reportPath "  Samples:"
    foreach ($s in $sample) { Add-Content $reportPath "    $s" }
  }
  Add-Content $reportPath ""
}

Add-Content $reportPath "Top error lines across all logs (unique):"
$top = Select-String -Path ($files | ForEach-Object { $_.FullName }) -Pattern 'ERROR|Exception|Traceback|unrecognized arguments|FileNotFoundError|OperationalError|here-document' -AllMatches -CaseSensitive:$false -ErrorAction SilentlyContinue |
  ForEach-Object { $_.Line.Trim() } | Sort-Object -Unique | Select-Object -First 50
foreach ($t in $top) { Add-Content $reportPath "  $t" }

Write-Output "Wrote report to $reportPath"
