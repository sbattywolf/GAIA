$token = $env:AUTOMATION_GITHUB_TOKEN
if (-not $token) {
  Write-Host "NO_TOKEN"
  exit 1
}
$owner = 'sbattywolf'
$repo = 'GAIA'
$created = @()
foreach ($file in Get-ChildItem -Path 'doc/ISSUES' -Filter '*.md') {
  $p = $file.FullName
  $c = Get-Content $p -Raw
  $titleLine = ($c -split "`n" | Select-String -Pattern '^Title:\s*(.*)' | ForEach-Object { $_.Matches[0].Groups[1].Value })
  if ($titleLine) { $title = $titleLine.Trim() } else { $title = $file.BaseName }
  $payload = @{ title = $title; body = $c } | ConvertTo-Json -Depth 10
  try {
    $resp = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/issues" -Method Post -Headers @{ Authorization = "token $token"; 'User-Agent'='GAIA-Agent' } -Body $payload -ContentType 'application/json'
    Write-Host ("CREATED: {0}" -f $resp.html_url)
    $created += $resp.html_url
  } catch {
    Write-Host ("ERROR creating issue for {0}: {1}" -f $p, $_.Exception.Message)
  }
}
if ($created.Count -gt 0) {
  Write-Host "ALL_CREATED:"
  $created | ForEach-Object { Write-Host $_ }
} else {
  Write-Host "NO_ISSUES_CREATED"
}
