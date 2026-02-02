if ($PSVersionTable -eq $null) { Write-Host "Run this in PowerShell."; exit 1 }
Write-Host "GAIA end-of-session helper"

# Commit WIP
Write-Host "Committing WIP (if any)..."
git add -A
try { git commit -m "WIP: session checkpoint" } catch { Write-Host "Nothing to commit or git not configured." }

# Backup events and write session note
$ts = (Get-Date).ToString("yyyyMMddTHHmmss")
if (Test-Path .\events.ndjson) {
    $backup = ".\doc\media\events.$ts.ndjson"
    Copy-Item .\events.ndjson $backup -Force
    Write-Host "Events backed up to $backup"
}

# Append simple session note
$noteDir = ".\Gaia\doc"
if (-not (Test-Path $noteDir)) { New-Item -ItemType Directory -Path $noteDir -Force | Out-Null }
$noteFile = Join-Path $noteDir "session_notes.md"
Add-Content -Path $noteFile -Value ("## Session: $ts")
Add-Content -Path $noteFile -Value ("- Checkpoint: WIP commit created")
Add-Content -Path $noteFile -Value ""
Write-Host "Session note appended to $noteFile"

Write-Host "End-of-session routine complete. You can now safely close the machine." 
