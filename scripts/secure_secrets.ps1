<#
Secure local secrets by uploading them to GitHub Actions Secrets and blanking local files.

Usage (interactive):
  .\scripts\secure_secrets.ps1

Usage (non-interactive):
  .\scripts\secure_secrets.ps1 -YesToAll

Prerequisites:
- GitHub CLI (`gh`) installed and authenticated (`gh auth login`).
- `git` available to discover remote repo.

What it does:
- Reads `.private/.env` for known keys (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GITHUB_TOKEN).
- If `gh` is available and authenticated, uploads non-empty values to repository secrets.
- Makes a secure backup of `.private/.env` to `.private/.env.backup.TIMESTAMP`, then blanks the original file or removes it.
- Runs `detect-secrets` scan if available and prints instructions for rotating leaked PATs (cannot revoke PATs automatically).

IMPORTANT: This script does NOT revoke or rotate personal tokens; you must rotate revoked tokens via the GitHub web UI.
#>

param(
    [switch]$YesToAll
)

Set-StrictMode -Version Latest

$root = (Resolve-Path "$(Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '..')").Path
$envFile = Join-Path $root '.private/.env'
if (-not (Test-Path $envFile)) {
    Write-Host "No .private/.env file found at $envFile. Nothing to do."; exit 0
}

Write-Host "Reading local secrets from $envFile"
$lines = Get-Content $envFile -ErrorAction Stop
$kv = @{}
foreach ($line in $lines) {
    $l = $line.Trim()
    if (-not $l -or $l.StartsWith('#')) { continue }
    if ($l -match '^(.*?)=(.*)$') {
        $k = $matches[1].Trim()
        $v = $matches[2].Trim()
        $kv[$k] = $v
    }
}

$keysToHandle = @('TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID','AUTOMATION_GITHUB_TOKEN')

function Get-GitHubRepoSlug {
    # Parse remote.origin.url
    try {
        $url = git config --get remote.origin.url 2>$null
        if (-not $url) { return $null }
        $url = $url.Trim()
        if ($url -match '[:/]([^/]+/[^/]+)(?:\.git)?$') { return $matches[1] }
    } catch { }
    return $null
}

$repo = Get-GitHubRepoSlug
if (-not $repo) { Write-Warning "Could not determine repo slug from git remote; gh commands will require -R owner/repo parameter." }

function GhAvailable {
    try { gh --version >$null 2>&1; return $true } catch { return $false }
}

if (-not (GhAvailable)) {
    Write-Warning "GitHub CLI 'gh' not found. Install and authenticate (gh auth login) to enable automated upload of secrets."
}

foreach ($k in $keysToHandle) {
    if (-not $kv.ContainsKey($k) -or [string]::IsNullOrWhiteSpace($kv[$k])) { continue }
    $val = $kv[$k]
    Write-Host "Found local value for $k"
    if (-not $YesToAll) {
        $ok = Read-Host "Upload $k to GitHub Actions Secrets for repo [$repo]? (y/N)"
        if ($ok -notin @('y','Y','yes','Yes')) { Write-Host "Skipping $k"; continue }
    }

    if (GhAvailable) {
        try {
            if ($repo) {
                $proc = Start-Process -FilePath gh -ArgumentList @('secret','set',$k,'-R',$repo) -NoNewWindow -PassThru -RedirectStandardInput 'PIPE'
                $proc.StandardInput.WriteLine($val)
                $proc.StandardInput.Close()
                $proc.WaitForExit()
                if ($proc.ExitCode -eq 0) { Write-Host "Uploaded $k to $repo (Actions secret)" } else { Write-Warning "gh secret set exit code $($proc.ExitCode)" }
            } else {
                # fallback: attempt without -R (uses current repo if gh is configured)
                $proc = Start-Process -FilePath gh -ArgumentList @('secret','set',$k) -NoNewWindow -PassThru -RedirectStandardInput 'PIPE'
                $proc.StandardInput.WriteLine($val)
                $proc.StandardInput.Close()
                $proc.WaitForExit()
                if ($proc.ExitCode -eq 0) { Write-Host "Uploaded $k to repository Actions secrets" } else { Write-Warning "gh secret set exit code $($proc.ExitCode)" }
            }
        } catch {
            Write-Warning "Failed to upload $k via gh: $_"
        }
    } else {
        Write-Warning "gh CLI not available; please add $k to repository Secrets manually."
    }
}

# Backup and blank local file
$timestamp = (Get-Date).ToString('yyyyMMddTHHmmss')
$backup = Join-Path (Split-Path $envFile -Parent) (".env.backup.$timestamp")
Copy-Item -Path $envFile -Destination $backup -Force
Write-Host "Backed up original file to $backup"

# Create an empty .private/.env with minimal safety
[System.IO.File]::WriteAllText($envFile, "# Local secrets removed on $(Get-Date -Format o)`n")
try { icacls $envFile /inheritance:r | Out-Null; icacls $envFile /grant:r "$($env:USERNAME):(R,W)" | Out-Null } catch { }
Write-Host "Blanked $envFile (original retained at $backup)."

# Run detect-secrets if available
try {
    detect-secrets --version >$null 2>&1
    Write-Host "Running detect-secrets scan (quick)..."
    & detect-secrets scan > "$root/.secrets.auto.scan" 2>$null
    Write-Host "Wrote scan output to $root/.secrets.auto.scan"
} catch {
    Write-Host "detect-secrets not installed or not in PATH; skipping scan."
}

Write-Host "Done. Review $backup to recover values if needed. Rotate any leaked tokens (see doc/SECRETS_ROTATION.md)."
