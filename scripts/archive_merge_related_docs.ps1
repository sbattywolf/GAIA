Param()

# Safe archival script: move merge/draft-related docs into doc/archive/ with timestamped names
Set-StrictMode -Version Latest
if (-not (Test-Path -Path doc\archive)) {
    New-Item -ItemType Directory -Path doc\archive | Out-Null
}

$timestamp = (Get-Date).ToString("yyyyMMddHHmm")
$patterns = @("*.draft*","*stoy_auto.draft.json","STR_Telegram.draft")

foreach ($p in $patterns) {
    Get-ChildItem -Path doc -Filter $p -File -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        $src = $_.FullName
        $dest = Join-Path -Path (Join-Path -Path "doc" -ChildPath "archive") -ChildPath ($_.Name + ".archived." + $timestamp)
        Write-Host "Archiving $src -> $dest"
        Copy-Item -Path $src -Destination $dest -Force
    }
}

Write-Host "Archival complete. Review files in doc/archive/. To remove originals, run with --delete-originals flag after review." 
