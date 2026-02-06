#!/usr/bin/env python3
"""
GAIA Environment Health Check

Quick health check script to validate the development environment is properly configured.
Useful for troubleshooting and verifying setup before starting work.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class HealthCheck:
    """Environment health checker."""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warnings = 0
        self.results = []
    
    def check(self, name: str, func) -> bool:
        """Run a health check and record the result."""
        try:
            status, message = func()
            self.results.append((name, status, message))
            
            if status == "PASS":
                self.checks_passed += 1
                print(f"✓ {name}: {message}")
                return True
            elif status == "WARN":
                self.checks_warnings += 1
                print(f"⚠ {name}: {message}")
                return True
            else:
                self.checks_failed += 1
                print(f"✗ {name}: {message}")
                return False
        except Exception as e:
            self.checks_failed += 1
            print(f"✗ {name}: Error - {e}")
            return False
    
    def print_summary(self):
        """Print check summary."""
        print("\n" + "=" * 60)
        print("HEALTH CHECK SUMMARY")
        print("=" * 60)
        print(f"Passed:   {self.checks_passed}")
        print(f"Warnings: {self.checks_warnings}")
        print(f"Failed:   {self.checks_failed}")
        print("=" * 60 + "\n")


def check_python_version() -> Tuple[str, str]:
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        return "PASS", f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return "FAIL", f"Python {version.major}.{version.minor} (requires 3.10+)"


def check_venv() -> Tuple[str, str]:
    """Check if running in virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        return "PASS", f"Virtual environment active at {sys.prefix}"
    else:
        return "WARN", "Not running in virtual environment (recommended)"


def check_dependencies() -> Tuple[str, str]:
    """Check if key dependencies are installed."""
    try:
        import click
        import requests
        import flask
        return "PASS", "Key dependencies installed (click, requests, flask)"
    except ImportError as e:
        return "FAIL", f"Missing dependency: {e.name}"


def check_git() -> Tuple[str, str]:
    """Check Git installation and status."""
    try:
        result = subprocess.run(
            ['git', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        
        # Check if we're in a git repo
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return "PASS", f"{version} (in git repository)"
        else:
            return "WARN", f"{version} (not in git repository)"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "FAIL", "Git not found or not working"


def check_gh_cli() -> Tuple[str, str]:
    """Check GitHub CLI."""
    try:
        result = subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Check authentication
        auth_result = subprocess.run(
            ['gh', 'auth', 'status'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if auth_result.returncode == 0:
            return "PASS", "GitHub CLI installed and authenticated"
        else:
            return "WARN", "GitHub CLI installed but not authenticated"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "WARN", "GitHub CLI not installed (optional)"


def check_env_file() -> Tuple[str, str]:
    """Check .env file."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        # Check if it has content
        content = env_file.read_text()
        if content.strip():
            return "PASS", ".env file exists with configuration"
        else:
            return "WARN", ".env file exists but is empty"
    elif env_example.exists():
        return "WARN", ".env not found (use .env.example as template)"
    else:
        return "WARN", "No .env or .env.example found"


def check_directories() -> Tuple[str, str]:
    """Check essential directories."""
    required = ['.tmp', '.copilot']
    optional = ['agents', 'scripts', 'doc']
    
    missing_required = [d for d in required if not Path(d).exists()]
    missing_optional = [d for d in optional if not Path(d).exists()]
    
    if missing_required:
        return "FAIL", f"Missing required directories: {', '.join(missing_required)}"
    elif missing_optional:
        return "WARN", f"Missing optional directories: {', '.join(missing_optional)}"
    else:
        return "PASS", "All essential directories exist"


def check_session_state() -> Tuple[str, str]:
    """Check session state file."""
    state_file = Path('.copilot/session_state.json')
    
    if state_file.exists():
        try:
            import json
            with open(state_file, 'r') as f:
                state = json.load(f)
            status = state.get('status', 'UNKNOWN')
            return "PASS", f"Session state exists (status: {status})"
        except Exception as e:
            return "WARN", f"Session state exists but invalid: {e}"
    else:
        return "WARN", "No session state found (will be created on first run)"


def check_orchestrator() -> Tuple[str, str]:
    """Check orchestrator.py."""
    orchestrator = Path('orchestrator.py')
    
    if orchestrator.exists():
        return "PASS", "Orchestrator script found"
    else:
        return "FAIL", "orchestrator.py not found"


def check_agents() -> Tuple[str, str]:
    """Check agents directory."""
    agents_dir = Path('agents')
    
    if not agents_dir.exists():
        return "WARN", "agents/ directory not found"
    
    agents = list(agents_dir.glob('*.py'))
    agent_count = len([a for a in agents if a.name != '__init__.py'])
    
    if agent_count > 0:
        return "PASS", f"Found {agent_count} agent scripts"
    else:
        return "WARN", "agents/ directory exists but no agents found"


def check_copilot_config() -> Tuple[str, str]:
    """Check Copilot configuration."""
    copilot_instructions = Path('.github/copilot-instructions.md')
    
    if copilot_instructions.exists():
        size = copilot_instructions.stat().st_size
        return "PASS", f"Copilot instructions exist ({size} bytes)"
    else:
        return "WARN", "Copilot instructions not found"


def check_database() -> Tuple[str, str]:
    """Check if database exists."""
    db_file = Path('gaia.db')
    
    if db_file.exists():
        size = db_file.stat().st_size
        return "PASS", f"Database exists ({size} bytes)"
    else:
        return "WARN", "Database not found (will be created on first run)"


def check_events_log() -> Tuple[str, str]:
    """Check events.ndjson."""
    events_file = Path('events.ndjson')
    
    if events_file.exists():
        lines = len(events_file.read_text().strip().split('\n'))
        return "PASS", f"Events log exists ({lines} events)"
    else:
        return "WARN", "Events log not found (will be created by agents)"


def main():
    """Run all health checks."""
    print("\n" + "=" * 60)
    print("GAIA ENVIRONMENT HEALTH CHECK")
    print("=" * 60 + "\n")
    
    # Change to repo root
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    print(f"Checking environment at: {repo_root}\n")
    
    checker = HealthCheck()
    
    # Run all checks
    print("System Checks:")
    print("-" * 60)
    checker.check("Python Version", check_python_version)
    checker.check("Virtual Environment", check_venv)
    checker.check("Dependencies", check_dependencies)
    checker.check("Git", check_git)
    checker.check("GitHub CLI", check_gh_cli)
    
    print("\nProject Configuration:")
    print("-" * 60)
    checker.check("Environment File", check_env_file)
    checker.check("Directories", check_directories)
    checker.check("Session State", check_session_state)
    checker.check("Copilot Config", check_copilot_config)
    
    print("\nProject Components:")
    print("-" * 60)
    checker.check("Orchestrator", check_orchestrator)
    checker.check("Agents", check_agents)
    checker.check("Database", check_database)
    checker.check("Events Log", check_events_log)
    
    # Print summary
    checker.print_summary()
    
    # Recommendations
    if checker.checks_failed > 0:
        print("RECOMMENDATIONS:")
        print("- Run: python scripts/setup_dev_env.py")
        print("- Check failed items above and fix issues")
        print()
    elif checker.checks_warnings > 0:
        print("RECOMMENDATIONS:")
        print("- Review warnings above")
        print("- Run: python scripts/setup_dev_env.py (to fix missing items)")
        print()
    else:
        print("✓ Environment is healthy! You're ready to develop.")
        print()
    
    return 0 if checker.checks_failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
