<#
Rotate logs in .tmp/logs by keeping the newest N files per agent prefix.

Usage:
  ./scripts/rotate_logs.ps1 -LogDir .\.tmp\logs -Keep 7
#>
param(
  [string]$LogDir = '.\\.tmp\\logs',
  [int]$Keep = 7,
  [int]$ArchiveAfterDays = 7,
  [switch]$DryRun
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
        $zipName = Join-Path $archiveDir ("{0}.zip" -f $f.BaseName)
        if ($DryRun) {
          Write-Host ("[dry-run] Would archive {0} -> {1}" -f $f.FullName, $zipName)
        } else {
          if (-not (Test-Path $zipName)) {
            Compress-Archive -Path $f.FullName -DestinationPath $zipName -Force
          }
          Remove-Item $f.FullName -ErrorAction SilentlyContinue
          Write-Host "Archived $($f.FullName) -> $zipName"
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
