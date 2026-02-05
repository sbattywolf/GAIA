param(
    [int]$Seconds = 300,
    [int]$EventsLines = 50,
    [int]$LogLines = 200
)

Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$root = Resolve-Path ".." | Select-Object -ExpandProperty Path
Push-Location $root

$end = (Get-Date).AddSeconds($Seconds)
$events = Join-Path $root 'events.ndjson'
$alog = Join-Path $root '.tmp\automation.log'
$out = Join-Path $root '.tmp\last_logs.txt'

function Tail-LastLines($path, $n){
    if (-not (Test-Path $path)) { return "<missing> $path" }
    $all = Get-Content -Raw -ErrorAction SilentlyContinue $path
    if (-not $all) { return "<empty> $path" }
    $lines = $all -split "\r?\n"
    return ($lines | Select-Object -Last $n) -join "`n"
}

# Poll until timeout to allow freshness; otherwise just dump last lines
while ((Get-Date) -lt $end) {
    $ev = Tail-LastLines $events $EventsLines
    $lg = Tail-LastLines $alog $LogLines
    "--- events (last $EventsLines lines) ---" | Out-File $out -Encoding utf8
    $ev | Out-File $out -Append -Encoding utf8
    "--- automation.log (last $LogLines lines) ---" | Out-File $out -Append -Encoding utf8
    $lg | Out-File $out -Append -Encoding utf8
    Start-Sleep -Seconds 5
    break
}

Write-Output "Wrote $out"
Pop-Location
