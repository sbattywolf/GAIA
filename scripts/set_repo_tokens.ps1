param(
    [string]$Repo = 'sbattywolf/GAIA'
)

function Set-RepoSecret {
    param(
        [string]$Name,
        [string]$Value
    )
    if ([string]::IsNullOrWhiteSpace($Value)) {
        Write-Host "Skipping $Name (no value provided)"
        return
    }
    Write-Host "Setting secret $Name for $Repo"
    gh secret set $Name --repo $Repo --body $Value
    if ($LASTEXITCODE -ne 0) { Write-Host "Failed to set $Name" -ForegroundColor Red }
}

# Read values from environment variables or prompt the user interactively
if ($env:AUTOMATION_GITHUB_TOKEN_VALUE) {
    Set-RepoSecret -Name 'AUTOMATION_GITHUB_TOKEN' -Value $env:AUTOMATION_GITHUB_TOKEN_VALUE
} else {
    $val = Read-Host -Prompt 'Enter value for AUTOMATION_GITHUB_TOKEN (leave blank to skip)'
    if ($val) { Set-RepoSecret -Name 'AUTOMATION_GITHUB_TOKEN' -Value $val }
}

if ($env:AUTOMATION_GITHUB_TOKEN_ORG_VALUE) {
    Set-RepoSecret -Name 'AUTOMATION_GITHUB_TOKEN_ORG' -Value $env:AUTOMATION_GITHUB_TOKEN_ORG_VALUE
} else {
    $val = Read-Host -Prompt 'Enter value for AUTOMATION_GITHUB_TOKEN_ORG (leave blank to skip)'
    if ($val) { Set-RepoSecret -Name 'AUTOMATION_GITHUB_TOKEN_ORG' -Value $val }
}

Write-Host 'Done.'
