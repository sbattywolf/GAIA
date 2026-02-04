<#
.SYNOPSIS
Create a GitHub environment named 'production' and set environment-scoped
secrets TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID using the `gh` CLI.

USAGE
  PowerShell -File .\scripts\gh_setup_env.ps1
  PowerShell -File .\scripts\gh_setup_env.ps1 -Repo "owner/repo"

Notes
- Requires `gh` CLI installed and authenticated (gh auth login).
- You can pre-export environment variables TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
  to avoid interactive prompts.
#>

param(
    [string]$Repo,
    [string]$Reviewers
)

function Fail([string]$msg) {
    Write-Error $msg
    exit 1
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Fail "gh CLI not found. Install from https://cli.github.com/ and run 'gh auth login'."
}

if (-not $Repo) {
    try {
        $Repo = gh repo view --json nameWithOwner -q .nameWithOwner 2>$null
    } catch {
        Fail "Failed to detect repo. Pass owner/repo as -Repo parameter."
    }
}

Write-Host "Using repo: $Repo"

# Create environment (no-op if it already exists)
Write-Host "Creating environment 'production' (if not present)..."
try {
    gh api --method POST "/repos/$Repo/environments" -f name=production 2>$null
    Write-Host "Environment 'production' created."
} catch {
    Write-Host "Environment creation returned non-OK or already exists (continuing)."
}

function Read-SecretValue([string]$name) {
    $envItem = Get-Item -Path "Env:$name" -ErrorAction SilentlyContinue
    if ($envItem -and $envItem.Value) {
        return $envItem.Value
    }
    $secure = Read-Host -Prompt "Enter $name (input hidden)" -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
    return $plain
}

$botVal = Read-SecretValue -name "TELEGRAM_BOT_TOKEN"
$chatVal = Read-SecretValue -name "TELEGRAM_CHAT_ID"

if ([string]::IsNullOrWhiteSpace($botVal) -or [string]::IsNullOrWhiteSpace($chatVal)) {
    Fail "Both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required. You may set them as environment variables before running this script."
}

Write-Host "Setting environment-scoped secrets in GitHub (production)..."
# Pipe the secret value to gh secret set --env
$botVal | gh secret set TELEGRAM_BOT_TOKEN --env production --repo $Repo > $null
$chatVal | gh secret set TELEGRAM_CHAT_ID --env production --repo $Repo > $null

Write-Host "Secrets set for environment 'production'."
Write-Host "Next recommended steps:"
Write-Host "- In the GitHub repo UI: Settings → Environments → production → configure protection rules (add required reviewers and a wait timer)."
Write-Host "- You can open the repo page with: gh repo view --web"
Write-Host "Done. After adding required reviewers you can run the protected workflow 'real-send.yml' manually from Actions."

# If REVIEWERS were provided (env var REVIEWERS or -Reviewers param), attempt to set protection required_reviewers
$reviewersVal = $null
if ($Reviewers) { $reviewersVal = $Reviewers }
elseif ($env:REVIEWERS) { $reviewersVal = $env:REVIEWERS }

if ($reviewersVal) {
    Write-Host "Attempting to set required reviewers for environment 'production': $reviewersVal"
    $arr = $reviewersVal -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }
    $items = @()
    foreach ($u in $arr) {
        $items += @{ type = 'User'; login = $u }
    }
    $body = @{ reviewers = $items; dismiss_stale_reviews = $false; require_code_owner_reviews = $false } | ConvertTo-Json -Depth 4
    try {
        gh api --method PUT "/repos/$Repo/environments/production/protection/required_reviewers" -f "$body" -H "Accept: application/vnd.github+json" 2>$null
        Write-Host "Protection rules updated successfully."
    } catch {
        Write-Host "Failed to set protection rules. Ensure you have repository admin rights and try again."
    }
}
