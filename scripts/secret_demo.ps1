<#
Demo: retrieve a secret (e.g. GH_TOKEN) via scripts/secret_helper.py and export it into the session.

Usage:
  .\scripts\secret_demo.ps1 GH_TOKEN
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Key
)

Write-Host "Attempting to retrieve secret: $Key"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { Write-Warning "Python not found on PATH. Install Python to use secret_helper.py"; return }

$scriptPath = Join-Path $PSScriptRoot 'secret_helper.py'
if (-not (Test-Path $scriptPath)) {
    Write-Warning "secret_helper.py not found at $scriptPath"
    return
}

try {
    $value = & python $scriptPath $Key 2>$null
} catch {
    Write-Warning "Error running secret_helper.py: $_"
    return
}

if ([string]::IsNullOrEmpty($value)) {
    Write-Warning "No value found for $Key"
    return
}

# Export to session environment and print masked value
Set-Item -Path ("Env:$Key") -Value $value
$masked = if ($value.Length -gt 6) { $value.Substring(0,3) + '...' + $value.Substring($value.Length -3) } else { '***' }
Write-Host "Retrieved and exported $Key (masked): $masked"
