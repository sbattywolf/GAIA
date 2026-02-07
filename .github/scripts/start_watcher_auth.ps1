param(
    [Parameter(Mandatory=$false)] [string] $Repo = 'sbattywolf/GAIA',
    [Parameter(Mandatory=$false)] [string] $Branch = 'fix/ci-test-fixes',
    [int] $IntervalSeconds = 30
)

function Ensure-GhAuth {
    if (-not $env:GITHUB_TOKEN -and -not $env:GH_TOKEN) {
        Write-Output 'GITHUB_TOKEN not found; you will be prompted to paste a token (input hidden).'
        $sec = Read-Host -AsSecureString 'Paste GitHub token (input hidden)'
        $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
        $tok = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
        $env:GITHUB_TOKEN = $tok
    }

    try {
        gh auth status 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'Authenticating gh using provided token...'
            $env:GITHUB_TOKEN | gh auth login --with-token
        } else {
            Write-Output 'gh already authenticated.'
        }
    } catch {
        Write-Output 'gh auth check failed, attempting login...'
        $env:GITHUB_TOKEN | gh auth login --with-token
    }
}

try {
    Ensure-GhAuth
    Write-Output "Launching watcher for $Repo@$Branch"
    & ./.github/scripts/watch_runs.ps1 -Repo $Repo -Branch $Branch -IntervalSeconds $IntervalSeconds
} catch {
    Write-Output 'Failed to start authenticated watcher: ' + $_.Exception.Message
}
