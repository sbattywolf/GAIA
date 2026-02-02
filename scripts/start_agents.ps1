<#
Start common GAIA agents locally as background processes.

Usage:
  ./scripts/start_agents.ps1 [-WorkerId worker1] [-MaxJobs 2] [-HealthPort 9100] [-ReclaimInterval 60]

This will start:
- `python -m agents.worker` (background)
- `python -m agents.reclaimer` (background, loop)

PIDs are stored in `.tmp/agents_pids.json` so `scripts/stop_agents.ps1` can stop them.
#>
param(
  [string]$WorkerId = 'worker1',
  [int]$MaxJobs = 2,
  [int]$HealthPort = 9100,
  [int]$ReclaimInterval = 60,
  [string]$LogDir = '.\\.tmp\\logs',
  [int]$LogRetentionCount = 7,
  [switch]$RunAsScheduledTask
)

$repoRoot = (Get-Location).Path
$tmpDir = Join-Path $repoRoot '.tmp'
if (-not (Test-Path $tmpDir)) { New-Item -Path $tmpDir -ItemType Directory | Out-Null }
$pidsFile = Join-Path $tmpDir 'agents_pids.json'

$logDirFull = Join-Path $repoRoot $LogDir
if (-not (Test-Path $logDirFull)) { New-Item -Path $logDirFull -ItemType Directory | Out-Null }

function Start-PythonModule {
  param($module, $args, $name)
  $python = 'python'
  $argumentList = "-m $module $args"
  $ts = Get-Date -Format "yyyyMMdd_HHmmss"
  $outLog = Join-Path $logDirFull ("{0}.{1}.out.log" -f $name, $ts)
  $errLog = Join-Path $logDirFull ("{0}.{1}.err.log" -f $name, $ts)
  Write-Host "Starting: $python $argumentList; stdout=$outLog stderr=$errLog"
  try {
    $proc = Start-Process -FilePath $python -ArgumentList $argumentList -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
    return @{ pid = $proc.Id; out = $outLog; err = $errLog }
  } catch {
    Write-Host ("Failed to start {0}: {1}" -f $module, $_)
    return $null
  }
}

$pids = @{}

function Rotate-Logs {
  param($name, $keep = 7)
  $pattern = "$name*.log"
  $files = Get-ChildItem -Path $logDirFull -Filter $pattern -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
  if ($files -and $files.Count -gt $keep) {
    $toArchive = $files[$keep..($files.Count - 1)]
    $archiveDir = Join-Path $logDirFull 'archive'
    if (-not (Test-Path $archiveDir)) { New-Item -Path $archiveDir -ItemType Directory | Out-Null }
    foreach ($f in $toArchive) {
      try {
        $zipName = Join-Path $archiveDir ("{0}.zip" -f $f.BaseName)
        if (-not (Test-Path $zipName)) {
          Compress-Archive -Path $f.FullName -DestinationPath $zipName -Force
        }
        Remove-Item $f.FullName -ErrorAction SilentlyContinue
      } catch {
        Write-Host ("Failed to archive old log {0}: {1}" -f $f.FullName, $_)
      }
    }
  }
}

# rotate logs for known agents before starting new ones
$agentNames = @('worker','reclaimer','alby_online_dryrun')
foreach ($n in $agentNames) { Rotate-Logs -name $n -keep $LogRetentionCount }

# Start worker
$w = Start-PythonModule 'agents.worker' "--worker-id $WorkerId --max-jobs $MaxJobs --health-port $HealthPort" 'worker'
if ($w) { $pids['worker'] = $w }

# Start reclaimer loop
$r = Start-PythonModule 'agents.reclaimer' "--interval $ReclaimInterval --reclaim-max-attempts 3" 'reclaimer'
if ($r) { $pids['reclaimer'] = $r }

# Optionally start an online agent in dry-run mode placeholder
$a = Start-PythonModule 'agents.alby_online_agent' "create-issue --repo owner/repo --title \"dry-run\" --dry-run" 'alby_online_dryrun'
if ($a) { $pids['alby_online_dryrun'] = $a }

# If requested, create scheduled tasks for persistence (runs at logon)
$scheduled = @{}
if ($RunAsScheduledTask) {
  foreach ($entry in $pids.GetEnumerator()) {
    $name = "GAIA_$($entry.Key)"
    $schtaskCmd = "python -m agents.$($entry.Key)"
    $schtaskArgs = "/Create /SC ONLOGON /RL HIGHEST /F /TN $name /TR `"$schtaskCmd`""
    Write-Host "Creating scheduled task: $name -> $schtaskCmd"
    try {
      schtasks.exe $schtaskArgs | Out-Null
      $scheduled[$entry.Key] = $name
    } catch {
      Write-Host ("Failed to create scheduled task {0}: {1}" -f $name, $_)
    }
  }
}

# Save PIDs and scheduled task names
$out = @{ started = (Get-Date).ToString('o'); pids = $pids; scheduled = $scheduled }
$out | ConvertTo-Json -Depth 5 | Out-File -FilePath $pidsFile -Encoding utf8
Write-Host "Started agents. PIDs and metadata written to $pidsFile"
Write-Host "To stop: ./scripts/stop_agents.ps1"
