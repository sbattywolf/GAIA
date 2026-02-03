<#
Rotate logs in .tmp/logs by keeping the newest N files per agent prefix.

Usage:
  ./scripts/rotate_logs.ps1 -LogDir .\.tmp\logs -Keep 7
#>
param(
  [string]$LogDir = '.\\.tmp\\logs',
  [int]$Keep = 7,
  [int]$ArchiveAfterDays = 7,
  [int]$ArchiveRetentionDays = 90,
  [switch]$DryRun,
  [switch]$Force
)

$repoRoot = (Get-Location).Path
$logDirFull = Join-Path $repoRoot $LogDir
if (-not (Test-Path $logDirFull)) {
  Write-Host "Log dir not found: $logDirFull"
  exit 1
}

function Keep-RecentLogs {
  param($name, $keep)
  $pattern = "$name*.log"
  $files = Get-ChildItem -Path $logDirFull -Filter $pattern -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
  if ($files -and $files.Count -gt $keep) {
    $candidates = $files[$keep..($files.Count - 1)]
    $cutoff = (Get-Date).AddDays(-$ArchiveAfterDays)
    $toArchive = $candidates | Where-Object { $_.LastWriteTime -lt $cutoff }
    $archiveDir = Join-Path $logDirFull 'archive'
    if (-not (Test-Path $archiveDir)) { New-Item -Path $archiveDir -ItemType Directory | Out-Null }
    foreach ($f in $toArchive) {
      try {
        # create archive name that includes original timestamp to avoid collisions
        $origTs = $f.LastWriteTime.ToString('yyyyMMdd_HHmmss')
        $zipName = Join-Path $archiveDir ("{0}.{1}.zip" -f $f.BaseName, $origTs)
        if ($DryRun) {
          Write-Host ("[dry-run] Would archive {0} -> {1}" -f $f.FullName, $zipName)
        } else {
          if (-not (Test-Path $zipName)) {
            Compress-Archive -Path $f.FullName -DestinationPath $zipName -Force
          }
          if ($Force) {
            Remove-Item $f.FullName -ErrorAction SilentlyContinue
            Write-Host "Archived and removed original $($f.FullName) -> $zipName"
          } else {
            Write-Host ("Archived {0} -> {1}; original file left in place (use -Force to remove originals)" -f $f.FullName, $zipName)
          }
        }
      } catch {
        Write-Host ("Failed to archive old log {0}: {1}" -f $f.FullName, $_)
      }
    }
  }
}

# discover distinct prefixes (before first dot or dash) to rotate for
 $all = Get-ChildItem -Path $logDirFull -File -ErrorAction SilentlyContinue
 $prefixes = $all | ForEach-Object { ($_.Name -split '[.\-]')[0] } | Sort-Object -Unique
foreach ($p in $prefixes) { Keep-RecentLogs -name $p -keep $Keep }

Write-Host "Rotation complete (kept $Keep per prefix)"

# Prune archived zip files older than ArchiveRetentionDays
$archiveDir = Join-Path $logDirFull 'archive'
if (Test-Path $archiveDir) {
  $cutoffArchive = (Get-Date).AddDays(-$ArchiveRetentionDays)
  $oldZips = Get-ChildItem -Path $archiveDir -Filter '*.zip' -File -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt $cutoffArchive }
  foreach ($z in $oldZips) {
    if ($DryRun) {
      Write-Host ("[dry-run] Would remove archive {0} (LastWrite: {1})" -f $z.FullName, $z.LastWriteTime)
    } else {
      if ($Force) {
        try { Remove-Item $z.FullName -ErrorAction SilentlyContinue; Write-Host "Removed archive {0}" -f $z.FullName } catch { Write-Host ("Failed to remove archive {0}: {1}" -f $z.FullName, $_) }
      } else {
        Write-Host ("Archive {0} is older than {1} days; use -Force to delete" -f $z.FullName, $ArchiveRetentionDays)
      }
    }
  }
}
