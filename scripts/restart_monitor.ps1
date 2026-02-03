param(
  [int]$Port = 5000,
  [int]$TimeoutSeconds = 20
)

$repoRoot = (Get-Location).Path
$tmpDir = Join-Path $repoRoot '.tmp'
if (-not (Test-Path $tmpDir)) { New-Item -Path $tmpDir -ItemType Directory | Out-Null }
$logDir = Join-Path $tmpDir 'logs'
if (-not (Test-Path $logDir)) { New-Item -Path $logDir -ItemType Directory | Out-Null }
$pidFile = Join-Path $tmpDir 'monitor_pid.txt'

function Kill-If-Running([int]$pid) {
  try {
    $p = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($p) {
      Write-Host "Stopping existing monitor pid $pid"
      Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
      Start-Sleep -Milliseconds 200
    }
  } catch {
    Write-Host ("Ignore stopping pid {0}: {1}" -f $pid, $_)
  }
}

if (Test-Path $pidFile) {
  try {
    $old = Get-Content $pidFile -Raw | ForEach-Object { $_.Trim() }
    if ($old -match '\d+') { Kill-If-Running ([int]$old) }
  } catch {
    Write-Host ("Failed reading existing pid file: {0}" -f $_)
  }
  Remove-Item $pidFile -ErrorAction SilentlyContinue
}

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$outLog = Join-Path $logDir ("monitor.{0}.out.log" -f $ts)
$errLog = Join-Path $logDir ("monitor.{0}.err.log" -f $ts)

Write-Host "Starting monitor with logs: stdout=$outLog stderr=$errLog"
try {
  $proc = Start-Process -FilePath 'python' -ArgumentList @('monitor/app.py') -WorkingDirectory $repoRoot -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
  if ($proc) {
    $proc.Id | Out-File -FilePath $pidFile -Encoding ascii
    Write-Host "Monitor started pid $($proc.Id)"
  } else {
    Write-Error "Failed to start monitor process"
    exit 1
  }
} catch {
  Write-Error ("Exception starting monitor: {0}" -f $_)
  exit 1
}

# wait until HTTP server responds
$url = "http://127.0.0.1:$Port/"
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $deadline) {
  try {
    $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) {
      Write-Host "Monitor HTTP responded: $($r.StatusCode)"
      exit 0
    }
  } catch {
    Start-Sleep -Milliseconds 250
  }
}
Write-Error "Monitor did not respond at $url within $TimeoutSeconds seconds. Check $outLog and $errLog"
exit 2
