param(
    [string] $OutDir = '.tmp/archives',
    [string] $BundleName = 'GAIA-repo.bundle'
)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }
$bundlePath = Join-Path $OutDir $BundleName

Write-Output "Creating git bundle archive at $bundlePath"
git bundle create $bundlePath --all
if ($LASTEXITCODE -eq 0) {
    Write-Output "Bundle created: $bundlePath"
} else {
    Write-Output "Failed to create bundle (exit $LASTEXITCODE)"
}
