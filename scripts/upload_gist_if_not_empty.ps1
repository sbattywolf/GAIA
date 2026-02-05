Param(
  [Parameter(Mandatory=$true)][string]$FilePath,
  [string]$Description = "Auto-triage run log",
  [int]$MaxRetries = 3
)

if (-not (Test-Path $FilePath)) {
  Write-Output "File not found: $FilePath"
  exit 1
}

$size = (Get-Item $FilePath).Length
if ($size -eq 0) {
  Write-Output "Skipping upload: file is empty - $FilePath"
  "$((Get-Date).ToUniversalTime().ToString('u')) - $FilePath - skipped (empty)" | Out-File -FilePath ".\doc\sprints\analysis\created_gists.txt" -Append -Encoding utf8
  exit 0
}

$attempt = 0
while ($attempt -lt $MaxRetries) {
  $attempt++
  Write-Output ("Attempt {0}: creating gist for {1}" -f $attempt, $FilePath)
  $descText = "{0}: {1}" -f $Description, ([System.IO.Path]::GetFileName($FilePath))
  $out = gh gist create -d "$descText" "$FilePath" 2>&1
  $urlMatch = ($out | Select-String -Pattern "https://gist\.github\.com/\S+" -AllMatches).Matches.Value
  if ($urlMatch) {
    $url = $urlMatch -join ' '
    $line = "{0} - {1} - {2}" -f (Get-Date).ToUniversalTime().ToString('u'), (Resolve-Path $FilePath).Path, $url
    $line | Out-File -FilePath ".\doc\sprints\analysis\created_gists.txt" -Append -Encoding utf8
    Write-Output "Uploaded: $url"
    exit 0
  } else {
    Write-Output "Upload failed: $($out -join ' `n')"
    if ($attempt -lt $MaxRetries) { Start-Sleep -Seconds ([math]::Pow(2,$attempt)) }
  }
}

Write-Output "Failed to upload gist after $MaxRetries attempts for $FilePath"
"$((Get-Date).ToUniversalTime().ToString('u')) - $FilePath - upload_failed" | Out-File -FilePath ".\doc\sprints\analysis\created_gists.txt" -Append -Encoding utf8
exit 2
