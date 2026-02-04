<#
Install WSL2 (Ubuntu) and show Podman install steps.

Run this script from an elevated PowerShell prompt (Run as Administrator).
It will enable WSL and request a reboot if required, then instruct you
how to install Podman inside the installed Linux distro.

Do NOT include any secrets in repo files. Keep tokens in GitHub Secrets.
#>

# Check for admin
If (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
    ).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Error "This script must be run as Administrator. Right-click PowerShell -> Run as Administrator."
    exit 1
}

Write-Host "Starting WSL install (this may enable features and request a reboot)..."

try {
    # Use the simple installer where available
    wsl --install -d Ubuntu
    $rc = $LASTEXITCODE
    if ($rc -ne 0) {
        Write-Warning "'wsl --install' returned exit code $rc. Attempting manual feature enable..."
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
        Write-Host "Features enabled. Please reboot and then run 'wsl --set-default-version 2' and install a distro from the Microsoft Store (Ubuntu recommended)."
    } else {
        Write-Host "WSL install requested. If prompted, reboot and finish distro setup from the Start menu (Ubuntu)."
    }
}
catch {
    Write-Error "WSL install failed: $_"
    exit 2
}

Write-Host "----- NEXT STEPS (run inside your WSL Ubuntu shell) -----"
Write-Host "(Open Ubuntu from Start menu after first-run setup completes)"
Write-Host "Run the following inside the WSL shell to install Podman and test a container:"
Write-Host "sudo apt update && sudo apt install -y podman buildah"
Write-Host "# Optional: enable Docker CLI compatibility"
Write-Host "sudo apt install -y podman-docker"
Write-Host "# Test Podman"
Write-Host "podman --version"
Write-Host "podman run --rm hello-world"

Write-Host "If you prefer not to use WSL or cannot run as admin, consider installing Git for Windows (Git Bash) or MSYS2 for Unix tools, or use Podman Desktop (GUI)."
