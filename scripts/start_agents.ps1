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
  [string]$WorkerId = 'test-worker',
  [int]$MaxJobs = 2,
  [int]$HealthPort = 9100,
  [int]$ReclaimInterval = 60,
  [string]$LogDir = '.\\.tmp\\logs',
  [int]$LogRetentionCount = 7,
  [string]$AgentId = '',
  [switch]$RunAsScheduledTask
)

$repoRoot = (Get-Location).Path
$tmpDir = Join-Path $repoRoot '.tmp'
if (-not (Test-Path $tmpDir)) { New-Item -Path $tmpDir -ItemType Directory | Out-Null }
$pidsFile = Join-Path $tmpDir 'agents_pids.json'

$logDirFull = Join-Path $repoRoot $LogDir
if (-not (Test-Path $logDirFull)) { New-Item -Path $logDirFull -ItemType Directory | Out-Null }

function Start-PythonModule {
  param($module, $argsStr, $name)
  $python = 'python'
  # Use env_loader to load .private/.env for scheduled services
  $launcher = Join-Path $repoRoot 'scripts\env_loader.py'
  # build ArgumentList as an array to avoid quoting issues
  $inner = @('-m', $module)
  if ($argsStr) {
    $inner += $argsStr -split ' '
  }
  # Final argument list: env_loader.py --env .private/.env -- python -m <module> <args...>
  $argArray = @($launcher, '--env', '.private\.env', '--', 'python') + $inner
  $ts = Get-Date -Format "yyyyMMdd_HHmmss"
  $outLog = Join-Path $logDirFull ("{0}.{1}.out.log" -f $name, $ts)
  $errLog = Join-Path $logDirFull ("{0}.{1}.err.log" -f $name, $ts)
  $argPreview = $argArray -join ' '
  Write-Host "Starting: $python $argPreview; stdout=$outLog stderr=$errLog"
  try {
    $proc = Start-Process -FilePath $python -ArgumentList $argArray -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
    return @{ pid = $proc.Id; out = $outLog; err = $errLog }
  } catch {
    Write-Host ("Failed to start {0}: {1}" -f $module, $_)
    return $null
  }
}

$pids = @{}

# Load agents.json mapping (if present) to resolve canonical ids, module and args
$agentsCfgPath = Join-Path $repoRoot 'agents.json'
$agentsCfg = @()
if (Test-Path $agentsCfgPath) {
  try {
    $raw = Get-Content $agentsCfgPath -Raw -ErrorAction Stop
    $agentsCfg = $raw | ConvertFrom-Json -ErrorAction Stop
  } catch {
    Write-Host "Failed to load agents.json: $_"
    $agentsCfg = @()
  }
}

function Find-AgentConfig {
  param($key)
  if (-not $key) { return $null }
  $lk = $key.ToString().ToLower()
  foreach ($a in $agentsCfg) {
    if ($a.id -and ($a.id.ToString().ToLower() -eq $lk)) { return $a }
    if ($a.name -and ($a.name.ToString().ToLower() -eq $lk)) { return $a }
    if ($a.aliases) {
      foreach ($al in $a.aliases) { if ($al.ToString().ToLower() -eq $lk) { return $a } }
    }
    if ($a.match) {
      foreach ($m in $a.match) { if ($m.ToString().ToLower() -eq $lk) { return $a } }
    }
  }
  return $null
}

# If there's an existing agents_pids.json, attempt to stop those PIDs for a clean restart
function Kill-ExistingAgents {
  param($pidsFile, $exclude = @())
  if (Test-Path $pidsFile) {
    try {
      $raw = Get-Content $pidsFile -Raw -ErrorAction Stop
      $json = $null
      try { $json = $raw | ConvertFrom-Json -ErrorAction Stop } catch { $json = $null }
      if ($json -and $json.pids) {
        foreach ($entry in $json.pids.PSObject.Properties) {
          $name = $entry.Name
          # skip excluded names (case-insensitive)
          $skip = $false
          if ($exclude -and $exclude.Count -gt 0) {
            foreach ($ex in $exclude) { if ($ex.ToString().ToLower() -eq $name.ToString().ToLower()) { $skip = $true; break } }
          }
          if ($skip) { Write-Host "Skipping stop of excluded agent $name"; continue }
          $val = $entry.Value
          if ($val.pid) {
            try {
              Write-Host "Stopping previous $name pid $($val.pid)"
              Stop-Process -Id $val.pid -ErrorAction SilentlyContinue -Force
            } catch {
              Write-Host "Could not stop pid $($val.pid): $_"
            }
          }
        }
      }
    } catch {
      Write-Host "Failed to read/stop existing agents: $_"
    }
    # if we excluded entries, don't remove the pid file (we preserved some entries)
    if (-not ($exclude -and $exclude.Count -gt 0)) {
      try { Remove-Item $pidsFile -ErrorAction SilentlyContinue } catch {}
    }
  }
}

# call Kill-ExistingAgents, excluding AgentId when provided (so we don't kill the existing instance)
if ($AgentId -and $AgentId.Trim() -ne '') {
  Kill-ExistingAgents -pidsFile $pidsFile -exclude @($AgentId)
} else {
  Kill-ExistingAgents -pidsFile $pidsFile
}

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

# Start agents according to resolved list (use AgentId if provided)
function Start-AgentByKey {
  param($key)
  $cfg = Find-AgentConfig -key $key
  if ($cfg -ne $null -and $cfg.module) {
    if ($cfg.id) { $nameKey = $cfg.id } else { $nameKey = $key }
    $args = $cfg.args
    if (-not $args) { $args = '' }
    Write-Host "Starting configured agent: $($cfg.module) $args (id=$nameKey)"
    $res = Start-PythonModule -module $cfg.module -argsStr $args -name $nameKey
    if ($res) { $pids[$nameKey] = $res }
    return
  }

  switch ($key) {
    'worker' {
      try {
        $name = 'worker'
        Write-Host "Starting real agent: agents.worker --worker-id $WorkerId --max-jobs $MaxJobs"
        $res = Start-PythonModule -module 'agents.worker' -argsStr ("--worker-id {0} --max-jobs {1}" -f $WorkerId, $MaxJobs) -name $name
        if ($res) { $pids[$name] = $res }
      } catch { Write-Host "Failed to start worker: $_" }
      break
    }
    'reclaimer' {
      try {
        $name = 'reclaimer'
        Write-Host "Starting real agent: agents.reclaimer --interval $ReclaimInterval"
        $res = Start-PythonModule -module 'agents.reclaimer' -argsStr ("--interval {0}" -f $ReclaimInterval) -name $name
        if ($res) { $pids[$name] = $res }
      } catch { Write-Host "Failed to start reclaimer: $_" }
      break
    }
    Default {
      try {
        $name = $key -replace '[^0-9A-Za-z_.-]','_'
        Write-Host "Attempting to start module by key: $key"
        $res = Start-PythonModule -module $key -argsStr '' -name $name
        if ($res) { $pids[$name] = $res }
      } catch { Write-Host ("Failed to start {0}: {1}" -f $key, $_) }
    }
  }
}

if ($AgentId -ne '') {
  $toStart = @($AgentId)
} else {
  $toStart = @('worker','reclaimer','alby_online_dryrun')
}

foreach ($k in $toStart) {
  # enforce single-instance for configured online agents
  $cfg = Find-AgentConfig -key $k
  $canonical = $k
  if ($cfg -and $cfg.id) { $canonical = $cfg.id }
  $isOnline = $false
  if ($cfg -and $cfg.id -and ($cfg.id.ToString().ToLower().Contains('-online-') -or $cfg.id.ToString().ToLower().Contains('-online'))) { $isOnline = $true }
  # check existing pid file for running instance
  $alreadyRunning = $false
  if (Test-Path $pidsFile) {
    try {
      $raw = Get-Content $pidsFile -Raw -ErrorAction Stop
      $pj = $raw | ConvertFrom-Json -ErrorAction Stop
      $pmap = $pj.pids
      if ($pmap) {
        foreach ($prop in $pmap.PSObject.Properties) {
          if ($prop.Name.ToString().ToLower() -eq $canonical.ToString().ToLower()) {
            $val = $prop.Value
            if ($val -and $val.pid) {
              try { $chk = Get-Process -Id $val.pid -ErrorAction SilentlyContinue; if ($chk) { $alreadyRunning = $true } } catch { }
            }
          }
        }
      }
    } catch { }
  }
  if ($isOnline -and $alreadyRunning) {
    Write-Host "Online agent '$canonical' already running; skipping start (single-instance enforced)"
    continue
  }

  Start-AgentByKey -key $k
  Start-Sleep -Seconds 1
  $checkKey = $k
  $cfg = Find-AgentConfig -key $k
  if ($cfg -and $cfg.id) { $checkKey = $cfg.id }
  if ($checkKey -and $pids.ContainsKey($checkKey)) {
    $check = Get-Process -Id $pids[$checkKey].pid -ErrorAction SilentlyContinue
    if (-not $check) {
      Write-Host "$k exited quickly; starting fallback agent_sleep for $k"
      $name = $checkKey
      $ts = Get-Date -Format "yyyyMMdd_HHmmss"
      $outLog = Join-Path $logDirFull ("{0}.fallback.{1}.out.log" -f $name, $ts)
      $errLog = Join-Path $logDirFull ("{0}.fallback.{1}.err.log" -f $name, $ts)
      $proc = Start-Process -FilePath 'python' -ArgumentList @('scripts\\agent_sleep.py','--name',$name,'--interval','30') -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
      if ($proc) { $pids[$name] = @{ pid = $proc.Id; out = $outLog; err = $errLog } }
    }
  }
}

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
