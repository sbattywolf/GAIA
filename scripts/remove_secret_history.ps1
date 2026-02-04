<#
.SYNOPSIS
  Safe helper to prepare and optionally execute a history rewrite to remove secrets.

.DESCRIPTION
  This script automates creating a bare mirror, running a non-destructive test of
  `git-filter-repo` using a provided `replace-text` file, and (optionally)
  applying the rewrite and pushing the cleaned refs to the remote. It will
  never push changes unless `-DoPush` and `-Approve` are provided together and
  `-RemoteUrl` is supplied.

.NOTES
  - Install `git-filter-repo` first: `python -m pip install git-filter-repo`
  - Do NOT put real tokens into `replace-text.txt` in shared places.
  - Always rotate leaked secrets immediately before or after the rewrite.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ReplaceTextFile,

    [string]$MirrorDir = "$(Resolve-Path -LiteralPath .)\GAIA-mirror.git",

    [switch]$DoPush,
    [string]$RemoteUrl = "",
    [switch]$Approve
)

function Assert-Command($cmd) {
    $null = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($?) { return $true }
    return $false
}

if (-not (Test-Path $ReplaceTextFile)) {
    Write-Error "Replace-text file not found: $ReplaceTextFile"
    exit 2
}

if (-not (Assert-Command git)) {
    Write-Error "git is not available on PATH. Install Git and retry."
    exit 3
}

# Check for git-filter-repo
try {
    & python -m git_filter_repo --version > $null 2>&1
    if ($LASTEXITCODE -ne 0) { throw 'missing' }
} catch {
    Write-Host "git-filter-repo not detected. Install it with:`n  python -m pip install git-filter-repo" -ForegroundColor Yellow
}

function Run-LocalDryRun {
    param($srcMirror, $replaceFile)
    $testMirror = "$srcMirror-dryrun"
    if (Test-Path $testMirror) { Remove-Item -Recurse -Force $testMirror }
    Write-Host "Copying mirror for dry-run: $srcMirror -> $testMirror"
    Copy-Item -Recurse -Force $srcMirror $testMirror

    Push-Location $testMirror
    try {
        Write-Host "Running git-filter-repo on dry-run mirror (this rewrites the copy)..."
        & python -m git_filter_repo --replace-text "$replaceFile" --force
        if ($LASTEXITCODE -ne 0) {
            Write-Error "git-filter-repo failed on dry-run mirror"
            return $false
        }

        Write-Host "Dry-run complete. Showing ref summary (first 30):"
        & git for-each-ref --format='%(refname:short) %(objectname:short)' | Select-Object -First 30
        return $true
    } finally {
        Pop-Location
    }
}

function Create-BareMirror {
    param($mirrorDir)
    if (Test-Path $mirrorDir) {
        Write-Host "Mirror directory exists: $mirrorDir (will reuse)"
    } else {
        Write-Host "Creating bare mirror at: $mirrorDir"
        & git clone --mirror . $mirrorDir
        if ($LASTEXITCODE -ne 0) { throw 'git clone --mirror failed' }
    }

    $backup = "$mirrorDir-backup-$(Get-Date -Format yyyyMMddTHHmmss).zip"
    Write-Host "Creating zip backup: $backup"
    Compress-Archive -Path $mirrorDir -DestinationPath $backup -Force
    return $mirrorDir
}

# Main flow
try {
    $absReplace = (Resolve-Path -LiteralPath $ReplaceTextFile).Path
} catch {
    Write-Error "Could not resolve replace-text file path"
    exit 4
}

Write-Host "Preparing bare mirror (no destructive action yet)..."
$createdMirror = Create-BareMirror -mirrorDir $MirrorDir

Write-Host "Performing non-destructive dry-run using a copy of the mirror..."
if (-not (Run-LocalDryRun -srcMirror $createdMirror -replaceFile $absReplace)) {
    Write-Error "Dry-run failed. Aborting."
    exit 5
}

Write-Host "Dry-run succeeded. Review the dry-run copy under: $createdMirror-dryrun"
Write-Host "IMPORTANT: No refs on 'origin' have been modified yet."

if ($DoPush) {
    if (-not $RemoteUrl) {
        Write-Error "To push cleaned refs you must provide `-RemoteUrl` and `-Approve`"
        exit 6
    }
    if (-not $Approve) {
        Write-Error "Push requested but not approved. Provide `-Approve` to allow destructive push."
        exit 7
    }

    Write-Host "Applying replace-text to the mirror and pushing to remote: $RemoteUrl"
    Push-Location $createdMirror
    try {
        & python -m git_filter_repo --replace-text "$absReplace" --force
        if ($LASTEXITCODE -ne 0) {
            Write-Error "git-filter-repo failed on mirror"
            exit 8
        }

        Write-Host "Filter applied on mirror. Now pushing with --mirror (force)."
        & git push --mirror $RemoteUrl
        if ($LASTEXITCODE -ne 0) {
            Write-Error "git push --mirror failed. You may need to temporarily disable push-protection."
            exit 9
        }
        Write-Host "Push complete. Re-run detect-secrets and CI checks on remote." -ForegroundColor Green
    } finally {
        Pop-Location
    }
} else {
    Write-Host "No push requested. To actually apply and push cleaned refs, re-run with: -DoPush -RemoteUrl <url> -Approve"
}

Write-Host "Script finished. If you want help generating `replace-text.txt` from `.secrets.scan`, ask me to produce a template (I will not include real tokens)."

exit 0
