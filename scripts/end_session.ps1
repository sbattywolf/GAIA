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
Write-Host "Running end-of-session maintenance: prune closed todos..."

# Run prune script to keep last 7 closed todos and archive older ones
try {
    if ($env:PROTOTYPE_USE_LOCAL_EVENTS -eq '1') {
        Write-Host "Skipping prune (PROTOTYPE_USE_LOCAL_EVENTS=1)"
    } else {
        $py = "python"
        $script = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "prune_closed_todos.py"
        if (Test-Path $script) {
            & $py $script --ndjson "Gaia/doc/todo-archive.ndjson" --keep 7 --older-out "Gaia/doc/todo-archive-older.ndjson"
            Write-Host "Prune script executed."
        } else {
            Write-Host "Prune script not found: $script"
        }
    }
} catch {
    Write-Host "Prune script failed: $_"
}

Write-Host "End-of-session routine complete. You can now safely close the machine." 
