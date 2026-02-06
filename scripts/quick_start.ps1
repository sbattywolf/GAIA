<#
.SYNOPSIS
    GAIA Quick Start Script for Windows PowerShell

.DESCRIPTION
    Automated setup for local development with GitHub Copilot.
    Runs environment setup, loads context, and provides next steps.

.EXAMPLE
    .\scripts\quick_start.ps1
#>

Write-Host ""
Write-Host "================================" -ForegroundColor Blue
Write-Host "  GAIA Quick Start Setup" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Run automated setup
Write-Host ""
Write-Host "Running automated setup..." -ForegroundColor Blue
python scripts/setup_dev_env.py

# Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Setup completed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠ Setup completed with warnings. Review output above." -ForegroundColor Yellow
}

# Provide next steps
Write-Host ""
Write-Host "================================" -ForegroundColor Blue
Write-Host "  Next Steps" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""
Write-Host "1. Activate virtual environment:"
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host ""
Write-Host "2. Load project context:"
Write-Host "   python scripts/load_context.py" -ForegroundColor Green
Write-Host ""
Write-Host "3. Check environment health:"
Write-Host "   python scripts/health_check.py" -ForegroundColor Green
Write-Host ""
Write-Host "4. Start coding with Copilot:"
Write-Host "   See: doc/01_onboarding/copilot-local-setup.md" -ForegroundColor Green
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Cyan
Write-Host ""
