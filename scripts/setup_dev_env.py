#!/usr/bin/env python3
"""
GAIA Development Environment Setup Script

Automates the complete setup of the GAIA development environment including:
- Python virtual environment
- Dependencies installation
- GitHub CLI verification
- Secrets configuration
- Directory structure creation
- Health checks
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Tuple, List

# ANSI color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}\n")


def print_success(message: str):
    """Print a success message."""
    print(f"{GREEN}✓ {message}{RESET}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{YELLOW}⚠ {message}{RESET}")


def print_error(message: str):
    """Print an error message."""
    print(f"{RED}✗ {message}{RESET}")


def print_info(message: str):
    """Print an info message."""
    print(f"{BLUE}ℹ {message}{RESET}")


def run_command(cmd: List[str], check: bool = True, capture: bool = True) -> Tuple[int, str]:
    """
    Run a shell command and return exit code and output.
    
    Args:
        cmd: Command and arguments as list
        check: Whether to raise on non-zero exit
        capture: Whether to capture output
        
    Returns:
        Tuple of (exit_code, output)
    """
    try:
        if capture:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=check
            )
            return result.returncode, result.stdout.strip()
        else:
            result = subprocess.run(cmd, check=check)
            return result.returncode, ""
    except subprocess.CalledProcessError as e:
        return e.returncode, str(e)
    except FileNotFoundError:
        return 127, f"Command not found: {cmd[0]}"


def check_python_version() -> bool:
    """Check if Python version is 3.10+."""
    print_section("Checking Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version_str} detected (meets requirement: 3.10+)")
        return True
    else:
        print_error(f"Python {version_str} detected (requires 3.10+)")
        return False


def check_git() -> bool:
    """Check if Git is installed."""
    print_section("Checking Git Installation")
    code, output = run_command(['git', '--version'], check=False)
    
    if code == 0:
        print_success(f"Git installed: {output}")
        return True
    else:
        print_error("Git is not installed or not in PATH")
        print_info("Install from: https://git-scm.com/")
        return False


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed."""
    print_section("Checking GitHub CLI")
    code, output = run_command(['gh', '--version'], check=False)
    
    if code == 0:
        print_success(f"GitHub CLI installed: {output.split()[0]}")
        
        # Check authentication
        code, auth_status = run_command(['gh', 'auth', 'status'], check=False)
        if code == 0:
            print_success("GitHub CLI is authenticated")
        else:
            print_warning("GitHub CLI is not authenticated")
            print_info("Run: gh auth login")
        return True
    else:
        print_warning("GitHub CLI (gh) is not installed")
        print_info("Install from: https://cli.github.com/")
        print_info("Optional but recommended for agent workflows")
        return False


def setup_venv() -> bool:
    """Create and setup Python virtual environment."""
    print_section("Setting Up Virtual Environment")
    
    venv_path = Path('.venv')
    
    if venv_path.exists():
        print_info("Virtual environment already exists at .venv")
        return True
    
    print_info("Creating virtual environment...")
    code, output = run_command([sys.executable, '-m', 'venv', '.venv'], check=False)
    
    if code == 0:
        print_success("Virtual environment created successfully")
        return True
    else:
        print_error(f"Failed to create virtual environment: {output}")
        return False


def get_pip_executable() -> str:
    """Get the path to pip in the virtual environment."""
    if platform.system() == 'Windows':
        return str(Path('.venv') / 'Scripts' / 'pip.exe')
    else:
        return str(Path('.venv') / 'bin' / 'pip')


def install_dependencies() -> bool:
    """Install Python dependencies."""
    print_section("Installing Dependencies")
    
    pip_exe = get_pip_executable()
    
    if not Path(pip_exe).exists():
        print_error("Virtual environment pip not found. Run with venv activated?")
        return False
    
    # Upgrade pip first
    print_info("Upgrading pip...")
    code, _ = run_command([pip_exe, 'install', '--upgrade', 'pip'], check=False, capture=False)
    
    if code != 0:
        print_warning("Failed to upgrade pip, continuing anyway...")
    
    # Install main requirements
    if Path('requirements.txt').exists():
        print_info("Installing requirements.txt...")
        code, _ = run_command([pip_exe, 'install', '-r', 'requirements.txt'], check=False, capture=False)
        
        if code == 0:
            print_success("Main requirements installed")
        else:
            print_error("Failed to install main requirements")
            return False
    else:
        print_warning("requirements.txt not found")
    
    # Install dev requirements if they exist
    if Path('requirements-dev.txt').exists():
        print_info("Installing requirements-dev.txt...")
        code, _ = run_command([pip_exe, 'install', '-r', 'requirements-dev.txt'], check=False, capture=False)
        
        if code == 0:
            print_success("Dev requirements installed")
        else:
            print_warning("Failed to install dev requirements")
    
    return True


def setup_secrets() -> bool:
    """Setup secrets configuration."""
    print_section("Secrets Configuration")
    
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print_success(".env file already exists")
        return True
    
    if env_example.exists():
        print_info("Creating .env from .env.example...")
        try:
            env_file.write_text(env_example.read_text())
            print_success(".env file created")
            print_warning("Remember to add your tokens to .env")
            print_info("Or use: python scripts/secrets_cli.py set GITHUB_TOKEN your_token")
            return True
        except Exception as e:
            print_error(f"Failed to create .env: {e}")
            return False
    else:
        print_warning(".env.example not found")
        print_info("You may need to configure secrets manually")
        return True


def create_directories() -> bool:
    """Create necessary directory structure."""
    print_section("Creating Directory Structure")
    
    dirs_to_create = [
        '.tmp',
        '.backup',
        'out',
        'logs',
        Path('doc') / '01_onboarding',
        Path('doc') / '02_technical',
        Path('doc') / '03_procedural',
        Path('doc') / '04_reference',
        Path('doc') / '05_backlog',
    ]
    
    for dir_path in dirs_to_create:
        dir_path = Path(dir_path)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"Created: {dir_path}")
            except Exception as e:
                print_warning(f"Failed to create {dir_path}: {e}")
        else:
            print_info(f"Already exists: {dir_path}")
    
    return True


def check_gitignore() -> bool:
    """Verify .gitignore has necessary entries."""
    print_section("Checking .gitignore")
    
    gitignore = Path('.gitignore')
    
    if not gitignore.exists():
        print_warning(".gitignore not found")
        return False
    
    content = gitignore.read_text()
    required_entries = ['.env', '.venv', '__pycache__', '*.pyc', '.tmp']
    
    missing = [entry for entry in required_entries if entry not in content]
    
    if missing:
        print_warning(f"Missing entries in .gitignore: {', '.join(missing)}")
        print_info("Consider adding them to prevent accidental commits")
    else:
        print_success("All essential entries found in .gitignore")
    
    return True


def print_next_steps():
    """Print next steps for the user."""
    print_section("Setup Complete! Next Steps")
    
    print_info("1. Activate the virtual environment:")
    if platform.system() == 'Windows':
        print(f"   {BOLD}.venv\\Scripts\\Activate.ps1{RESET} (PowerShell)")
        print(f"   {BOLD}.venv\\Scripts\\activate.bat{RESET} (CMD)")
    else:
        print(f"   {BOLD}source .venv/bin/activate{RESET}")
    
    print_info("\n2. Configure secrets (if needed):")
    print(f"   {BOLD}python scripts/secrets_cli.py set GITHUB_TOKEN your_token{RESET}")
    
    print_info("\n3. Start a development session:")
    if platform.system() == 'Windows':
        print(f"   {BOLD}.\\scripts\\start_session.ps1{RESET}")
    else:
        print(f"   {BOLD}./scripts/start_session.sh{RESET}")
    
    print_info("\n4. Run an example agent:")
    print(f"   {BOLD}python agents/backlog_agent.py --title 'Test' --body 'Created by GAIA'{RESET}")
    
    print_info("\n5. Load context and backlog:")
    print(f"   {BOLD}python scripts/load_context.py{RESET}")
    
    print_info("\n6. For Copilot users:")
    print(f"   See {BOLD}doc/01_onboarding/copilot-local-setup.md{RESET}")
    
    print(f"\n{GREEN}{BOLD}Happy coding with GAIA! 🚀{RESET}\n")


def main():
    """Main setup routine."""
    print(f"\n{BOLD}{BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║         GAIA Development Environment Setup            ║")
    print("║                                                        ║")
    print("║  Automated setup for local development with Copilot   ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(RESET)
    
    # Change to repo root
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    
    print_info(f"Working directory: {repo_root}\n")
    
    # Run all checks and setup steps
    checks = [
        ("Python Version", check_python_version),
        ("Git", check_git),
        ("GitHub CLI", check_gh_cli),
        ("Virtual Environment", setup_venv),
        ("Dependencies", install_dependencies),
        ("Secrets", setup_secrets),
        ("Directories", create_directories),
        ("Git Ignore", check_gitignore),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error during {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_section("Setup Summary")
    
    for name, result in results:
        if result:
            print_success(f"{name}: OK")
        else:
            print_warning(f"{name}: NEEDS ATTENTION")
    
    # Next steps
    print_next_steps()
    
    # Return success if critical checks passed
    critical_checks = ["Python Version", "Virtual Environment", "Dependencies"]
    critical_passed = all(
        result for name, result in results 
        if name in critical_checks
    )
    
    return 0 if critical_passed else 1


if __name__ == '__main__':
    sys.exit(main())
