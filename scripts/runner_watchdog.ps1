<#
Runner watchdog: ensures `gise_autonomous_runner.py` is running and starts it if missing.
Usage: Run this once in a background PowerShell session or schedule it via Task Scheduler.
#>
Set-StrictMode -Version Latest
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = "python"
$scriptRel = "scripts/gise_autonomous_runner.py"
$args = @('--tenmin-hours','20','--thirtymin-hours','30','--duration-hours','20')

function Get-RunnerProcesses {
    try {
        Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object { $_.CommandLine -and $_.CommandLine -match 'gise_autonomous_runner.py' }
    } catch {
        @()
    }
}

if ((Get-RunnerProcesses).Count -eq 0) {
    Start-Process -NoNewWindow -FilePath $py -ArgumentList $args -WorkingDirectory $root -PassThru | Out-Null
    Write-Output "Runner started"
} else {
    Write-Output "Runner already running"
}
