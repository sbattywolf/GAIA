Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)
# repo root
Push-Location ..
$root = Get-Location
$tmp = Join-Path $root '.tmp'
if (-not (Test-Path $tmp)) { New-Item -Path $tmp -ItemType Directory | Out-Null }
$envFile = Join-Path $tmp 'telegram.env'
if (-not (Test-Path $envFile)) {
  Write-Output "Missing env file: $envFile"; Pop-Location; exit 1
}
# load simple KEY=VALUE pairs
Get-Content $envFile | ForEach-Object {
  $_ = $_.Trim()
  if ($_ -like '#*' -or $_ -eq '') { return }
  $parts = $_ -split '=', 2
  if ($parts.Count -ge 2) { $n = $parts[0].Trim(); $v = $parts[1].Trim(); Set-Item -Path env:\$n -Value $v }
}
# ensure PYTHONPATH includes repo root so `from gaia import ...` works
$env:PYTHONPATH = $root.Path
# logs
$logDir = Join-Path $tmp 'logs'
if (-not (Test-Path $logDir)) { New-Item -Path $logDir -ItemType Directory | Out-Null }
$out = Join-Path $logDir 'approval_listener.out.log'
$err = Join-Path $logDir 'approval_listener.err.log'
# start detached: run long-lived (1 day) with 5-minute poll to reduce polling frequency
# Use env_loader so the process inherits the env file reliably
$launcher = Join-Path $root 'scripts\env_loader.py'
$argList = @($launcher, '--env', $envFile, '--', 'python', 'scripts\approval_listener.py', '--timeout', '86400', '--poll', '300')
Start-Process -FilePath python -ArgumentList $argList -RedirectStandardOutput $out -RedirectStandardError $err -WindowStyle Hidden
Write-Output "Approval listener started (logs -> $out , $err)"
Pop-Location
