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
    if ($_ -match '^[ \t]*#') { return }
    if ($_ -match '^[ \t]*$') { return }
    $pair = $_ -split '='
    if ($pair.Count -lt 2) { return }
    $key = $pair[0].Trim()
    $val = ($pair[1..($pair.Count-1)] -join '=').Trim()
    $env:$key = $val
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
