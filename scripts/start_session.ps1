<#
Start GAIA session helper (PowerShell).
Loads .env, activates .venv if present, and tails events.ndjson.
#>

if ($PSVersionTable -eq $null) { Write-Host "Run this in PowerShell."; return }

Write-Host "Starting GAIA session..."

try {
    # Activate venv if present
    if (Test-Path .venv\Scripts\Activate.ps1) {
        Write-Host "Activating .venv..."
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host ".venv not found; create one with: python -m venv .venv"
    }

    # Load .env into session if loader exists
    $loadEnvPath = Join-Path $PWD 'scripts\load_env.ps1'
    if (Test-Path $loadEnvPath) {
        Write-Host "Loading .env via scripts/load_env.ps1..."
        try { . $loadEnvPath } catch { Write-Warning "Failed to load .env: $_" }
    } else { Write-Host "No scripts/load_env.ps1 found; skipping .env load." }

    # Ensure doc folders exist
    if (-not (Test-Path .\Gaia\doc)) { New-Item -ItemType Directory -Path .\Gaia\doc -Force | Out-Null }

    Write-Host "Tailing events (if present): GAIA/events.ndjson"
    if (Test-Path .\events.ndjson) {
        Write-Host "Tailing events (Ctrl+C to stop)"
        Get-Content .\events.ndjson -Wait -Tail 50
    } else {
        Write-Host "No events.ndjson found yet. Run an agent or create the file to begin."
    }
} catch {
    Write-Warning "start_session.ps1 encountered an error: $_"
}
# Start GAIA session helper (Windows PowerShell variant)
try {
    if ($PSVersionTable -eq $null) { Write-Host "Run this in PowerShell."; return }

    Write-Host "Starting GAIA session..."

    # Activate venv if present
    if (Test-Path .venv\Scripts\Activate.ps1) {
        Write-Host "Activating .venv..."
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host ".venv not found; create one with: python -m venv .venv"
    }

    # Load .env into session if loader exists
    $loadEnvPath = Join-Path $PWD 'scripts\load_env.ps1'
    if (Test-Path $loadEnvPath) {
        Write-Host "Loading .env via scripts/load_env.ps1..."
        try {
            . $loadEnvPath
        } catch {
            Write-Warning "Failed to load .env: $_"
        }
    } else {
        Write-Host "No scripts/load_env.ps1 found; skipping .env load."
    }

    # Ensure doc folders exist
    if (-not (Test-Path .\Gaia\doc)) { New-Item -ItemType Directory -Path .\Gaia\doc -Force | Out-Null }

    Write-Host "Tailing events (if present): GAIA/events.ndjson"
    if (Test-Path .\events.ndjson) {
        Write-Host "Tailing events (Ctrl+C to stop)"
        Get-Content .\events.ndjson -Wait -Tail 50
    } else {
        Write-Host "No events.ndjson found yet. Run an agent or create the file to begin."
    }
} catch {
    Write-Warning "start_session.ps1 encountered an error: $_"
}
REM Start GAIA session helper (Windows PowerShell variant)
if ($PSVersionTable -eq $null) { Write-Host "Run this in PowerShell."; exit 1 }

Write-Host "Starting GAIA session..."

# Activate venv if present
if (Test-Path .venv\Scripts\Activate.ps1) {
    Write-Host "Activating .venv..."
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host ".venv not found; create one with: python -m venv .venv"
}

# Ensure doc folders exist
if (-not (Test-Path .\Gaia\doc)) { New-Item -ItemType Directory -Path .\Gaia\doc -Force | Out-Null }

Write-Host "Tailing events (if present): GAIA/events.ndjson"
if (Test-Path .\events.ndjson) {
    Write-Host "Tailing events (Ctrl+C to stop)"
    Get-Content .\events.ndjson -Wait -Tail 50
} else {
    Write-Host "No events.ndjson found yet. Run an agent or create the file to begin."
}
