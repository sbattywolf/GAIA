#!/usr/bin/env python3
"""
GAIA Dashboard Setup Verification Script

This script checks if your laptop is ready to run the GAIA dashboard.
It verifies Python version, required files, and provides helpful feedback.
"""

import sys
import os
from pathlib import Path
import platform

# ANSI color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    print(f"{BLUE}{BOLD}  {text}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 70}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"  {GREEN}✓{RESET} {text}")

def print_warning(text):
    """Print warning message."""
    print(f"  {YELLOW}⚠{RESET} {text}")

def print_error(text):
    """Print error message."""
    print(f"  {RED}✗{RESET} {text}")

def print_info(text):
    """Print info message."""
    print(f"  {BLUE}ℹ{RESET} {text}")

def check_python_version():
    """Check if Python version is adequate."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python version: {version_str}")
    print_info(f"Python executable: {sys.executable}")
    
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version_str} is compatible (requires 3.10+)")
        return True
    else:
        print_error(f"Python {version_str} is too old (requires 3.10+)")
        print_info("Download Python from: https://www.python.org/downloads/")
        return False

def check_system_info():
    """Display system information."""
    print_header("System Information")
    
    print_info(f"Operating System: {platform.system()}")
    print_info(f"OS Version: {platform.version()}")
    print_info(f"Architecture: {platform.machine()}")
    print_info(f"Hostname: {platform.node()}")
    
    return True

def check_repository_structure():
    """Check if we're in the right directory."""
    print_header("Checking Repository Structure")
    
    # Get repository root
    try:
        root = Path(__file__).resolve().parents[1]
    except:
        root = Path.cwd()
    
    print_info(f"Repository root: {root}")
    
    # Check for key files and directories
    checks = {
        'scripts/dashboard_server.py': 'Dashboard server script',
        'scripts/project_dashboard.html': 'Dashboard HTML file',
        'scripts/project_summary.py': 'CLI summary tool',
        'doc': 'Documentation directory',
        'agents.json': 'Agents configuration file',
    }
    
    all_good = True
    for path, description in checks.items():
        full_path = root / path
        if full_path.exists():
            print_success(f"{description}: Found at {path}")
        else:
            print_error(f"{description}: Missing at {path}")
            all_good = False
    
    return all_good

def check_data_files():
    """Check if data files exist."""
    print_header("Checking Data Files")
    
    root = Path(__file__).resolve().parents[1]
    
    # Check for data files
    data_files = {
        'doc/todo-archive.ndjson': ('Tasks data', True),
        'agents.json': ('Agents configuration', True),
        '.tmp/pending_commands.json': ('Pending commands', False),
    }
    
    all_required = True
    for path, (description, required) in data_files.items():
        full_path = root / path
        if full_path.exists():
            size = full_path.stat().st_size
            print_success(f"{description}: Found ({size} bytes) at {path}")
        else:
            if required:
                print_error(f"{description}: Missing at {path} (REQUIRED)")
                all_required = False
            else:
                print_warning(f"{description}: Missing at {path} (optional)")
    
    return all_required

def check_port_availability():
    """Check if default port is available."""
    print_header("Checking Port Availability")
    
    import socket
    
    default_port = 8080
    alternative_ports = [8888, 9000, 3000]
    
    def is_port_available(port):
        """Check if a port is available."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0
        except:
            return False
    
    if is_port_available(default_port):
        print_success(f"Port {default_port} is available")
        return True
    else:
        print_warning(f"Port {default_port} is already in use")
        print_info("You can use a different port with --port flag:")
        
        # Find an available alternative
        for port in alternative_ports:
            if is_port_available(port):
                print_info(f"  python scripts/dashboard_server.py --port {port}")
                return True
        
        print_warning("All common ports are in use. Try a custom port like 8090")
        return True

def provide_next_steps():
    """Show what to do next."""
    print_header("Next Steps")
    
    print(f"{BOLD}To start the dashboard:{RESET}")
    print()
    print("  1. Open a terminal in the repository directory")
    print("  2. Run: python scripts/dashboard_server.py --port 8080")
    print("  3. Open your browser to: http://localhost:8080/dashboard")
    print()
    print(f"{BOLD}Alternative - CLI Tool:{RESET}")
    print()
    print("  Run: python scripts/project_summary.py")
    print()
    print(f"{BOLD}For more help:{RESET}")
    print()
    print("  • LAPTOP_SETUP.md - Detailed laptop setup guide")
    print("  • scripts/QUICKSTART.md - 60-second quick start")
    print("  • doc/DASHBOARD_README.md - Complete documentation")
    print()

def main():
    """Main verification function."""
    print()
    print(f"{BOLD}{BLUE}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{BLUE}║  GAIA Dashboard - Setup Verification                              ║{RESET}")
    print(f"{BOLD}{BLUE}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
    
    checks = [
        ("Python Version", check_python_version),
        ("System Info", check_system_info),
        ("Repository Structure", check_repository_structure),
        ("Data Files", check_data_files),
        ("Port Availability", check_port_availability),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
    
    print()
    if all_passed:
        print(f"{GREEN}{BOLD}✓ All checks passed! You're ready to run the dashboard.{RESET}")
    else:
        print(f"{YELLOW}{BOLD}⚠ Some checks failed. Review the issues above.{RESET}")
    
    provide_next_steps()
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Verification cancelled.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)
