<#
Install workbook: checks for required CLIs and prints install suggestions.

This helper does NOT auto-install by default; it reports missing tools and suggests commands.
#>
if ($PSVersionTable -eq $null) { Write-Host "Run this in PowerShell."; exit 1 }

Write-Host "GAIA install workbook: checking common tools..."

$tools = @(
    @{ name = 'gh'; check = { Get-Command gh -ErrorAction SilentlyContinue } ; install = 'winget install --id GitHub.cli' },
    @{ name = 'bw'; check = { Get-Command bw -ErrorAction SilentlyContinue } ; install = 'winget install --id Bitwarden.BitwardenCLI' },
    @{ name = 'python'; check = { Get-Command python -ErrorAction SilentlyContinue } ; install = 'winget install --id Python.Python.3' }
)

$missing = @()
foreach ($t in $tools) {
    $found = & $t.check
    if ($null -eq $found) {
        Write-Host "MISSING: $($t.name)    -> suggested: $($t.install)"
        $missing += $t
    } else {
        Write-Host "OK: $($t.name)"
    }
}

if ($missing.Count -eq 0) { Write-Host "All core tools present."; exit 0 }

Write-Host "\nIf you want the script to attempt installation using winget, run with -Install switch."
if ($args -contains '-Install') {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        foreach ($t in $missing) {
            Write-Host "Attempting: $($t.install)"
            & winget install --silent --accept-package-agreements --accept-source-agreements $t.install
        }
    } else {
        Write-Host "winget not found; please install missing tools manually or enable winget." 
    }
}

Write-Host "Done."
