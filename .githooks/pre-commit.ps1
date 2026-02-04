Param()
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
if (-not $python) { Write-Error 'Python not found in PATH'; exit 1 }
$root = (git rev-parse --show-toplevel) -replace '\\','\\'
& $python "$root\scripts\check_staged_secrets.py"
