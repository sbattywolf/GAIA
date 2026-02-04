<#
Set repository GitHub Actions secrets for Telegram summary.

Usage examples:
  # prompt for values interactively
  .\scripts\set_repo_secrets.ps1 -Repo 'OWNER/REPO'

  # pass values directly (careful with shell history)
  .\scripts\set_repo_secrets.ps1 -Repo 'OWNER/REPO' -BotToken 'TOKEN' -ChatId '123456'

This script requires the GitHub CLI (`gh`) to be installed and authenticated.
#>

[CmdletBinding()]
Param(
    [Parameter(Mandatory=$true)] [string] $Repo,
    [Parameter(Mandatory=$false)] [string] $BotToken,
    [Parameter(Mandatory=$false)] [string] $ChatId
)

function Prompt-SecureStringToPlain([string]$prompt) {
    $s = Read-Host -Prompt $prompt -AsSecureString
    $ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)
    try { [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI 'gh' not found. Install and authenticate (gh auth login) before running."
    exit 2
}

if (-not $BotToken) {
    if ($env:TELEGRAM_BOT_TOKEN) { $BotToken = $env:TELEGRAM_BOT_TOKEN }
    else { $BotToken = Prompt-SecureStringToPlain 'Enter TELEGRAM_BOT_TOKEN (hidden):' }
}

if (-not $ChatId) {
    if ($env:TELEGRAM_CHAT_ID) { $ChatId = $env:TELEGRAM_CHAT_ID }
    else { $ChatId = Read-Host 'Enter TELEGRAM_CHAT_ID (plain):' }
}

try {
    gh secret set TELEGRAM_BOT_TOKEN --repo $Repo --body $BotToken
    gh secret set TELEGRAM_CHAT_ID --repo $Repo --body $ChatId
    Write-Output "Secrets set for $Repo"
} catch {
    Write-Error "Failed to set secrets: $_"
    exit 1
} finally {
    # clear sensitive variables
    $BotToken = $null
}
