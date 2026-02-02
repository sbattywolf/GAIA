<#
Load local .env into the PowerShell session and apply PATH_APPEND.

Usage:
  . .\scripts\load_env.ps1
#>

if ($PSVersionTable -eq $null) { Write-Host "Run this in PowerShell."; exit 1 }

$envFile = Join-Path $PWD ".env"
if (-not (Test-Path $envFile)) {
    Write-Host ".env not found; copy .env.example to .env and populate it."; return
}

Write-Host "Loading .env from $envFile"
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -match '^[ \t]*#' -or $line -match '^[ \t]*$') { return }
    $idx = $line.IndexOf('=')
    if ($idx -lt 0) { return }
    $key = $line.Substring(0, $idx).Trim()
    $val = $line.Substring($idx + 1).Trim()
    if ($key) {
        Set-Item -Path ("Env:$key") -Value $val
    }
}

if ($env:PATH_APPEND) {
    Write-Host "Applying PATH_APPEND"
    $paths = $env:PATH_APPEND -split ';'
    foreach ($p in $paths) {
        if (-not [string]::IsNullOrWhiteSpace($p) -and (Test-Path $p)) {
            $env:PATH = $p + ';' + $env:PATH
        }
    }
}

Write-Host ".env loaded. Reminder: do not commit real secrets to git."
