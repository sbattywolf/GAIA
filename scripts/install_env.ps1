<#
Bootstrap GAIA/Alby development environment (PowerShell)
Usage:
  .\scripts\install_env.ps1            # create venv, install requirements
  .\scripts\install_env.ps1 -Recreate  # recreate venv
#>
param(
    [switch]$Recreate
)

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $repoRoot
$venvPath = Join-Path $repoRoot "..\.venv" | Resolve-Path -ErrorAction SilentlyContinue
$venvPath = Join-Path $repoRoot "..\.venv"

if ($Recreate -and (Test-Path $venvPath)) {
    Write-Host "Removing existing venv at $venvPath"
    Remove-Item -Recurse -Force $venvPath
}

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating venv at $venvPath"
    python -m venv $venvPath
} else {
    Write-Host "Using existing venv at $venvPath"
}

$activate = Join-Path $venvPath 'Scripts\Activate.ps1'
if (Test-Path $activate) {
    Write-Host "Activating venv..."
    & $activate
} else {
    Write-Host "Activation script missing at $activate - you can activate manually:" -ForegroundColor Yellow
    Write-Host ". $venvPath\Scripts\Activate.ps1"
}

Write-Host "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip
$req = Join-Path $repoRoot '..\requirements.txt'
if (Test-Path $req) {
    pip install -r $req
} else {
    Write-Host "requirements.txt not found at $req" -ForegroundColor Yellow
}

Write-Host "Bootstrap complete."
Write-Host "To activate (PowerShell): . $venvPath\Scripts\Activate.ps1"
Write-Host "Quick smoke test: python -c 'import flask; import sys; print(\"flask\", flask.__version__)'"
