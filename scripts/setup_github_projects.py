#!/usr/bin/env python3
"""Helper script to configure GitHub Projects integration for GAIA.

Usage:
    python scripts/setup_github_projects.py --help
    python scripts/setup_github_projects.py check
    python scripts/setup_github_projects.py configure --project-number 1
    python scripts/setup_github_projects.py test

This script helps you:
1. Check if GitHub Projects integration is configured
2. Verify your GitHub token and repository settings
3. Test the integration with a dry-run
4. Guide you through the setup process
"""

import argparse
import os
import sys
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_success(text):
    """Print success message."""
    print(f"✓ {text}")


def print_error(text):
    """Print error message."""
    print(f"✗ {text}")


def print_info(text):
    """Print info message."""
    print(f"ℹ {text}")


def check_github_cli():
    """Check if GitHub CLI is available."""
    try:
        result = subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_github_auth():
    """Check if GitHub CLI is authenticated."""
    try:
        result = subprocess.run(
            ['gh', 'auth', 'status'],
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, 'GH_TOKEN': os.environ.get('AUTOMATION_GITHUB_TOKEN', '')}
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_repo_info():
    """Get repository owner and name."""
    try:
        result = subprocess.run(
            ['gh', 'repo', 'view', '--json', 'owner,name'],
            capture_output=True,
            text=True,
            check=False,
            cwd=ROOT
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            owner = data.get('owner', {}).get('login', '')
            name = data.get('name', '')
            return owner, name
        return None, None
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None


def check_environment():
    """Check environment variables for GitHub integration."""
    print_header("Environment Check")
    
    issues = []
    warnings = []
    
    # Check for GitHub token
    token_vars = [
        'AUTOMATION_GITHUB_TOKEN_PAI',
        'AUTOMATION_GITHUB_TOKEN',
        'AUTOMATION_GITHUB_TOKEN_ORG',
        'GITHUB_TOKEN',
    ]
    token_found = None
    for var in token_vars:
        if os.environ.get(var):
            token_found = var
            print_success(f"GitHub token found: {var}")
            break
    
    if not token_found:
        issues.append("No GitHub token found in environment")
        print_error("Missing GitHub token (checked: " + ", ".join(token_vars) + ")")
    
    # Check for repository setting
    repo_vars = [
        'AUTOMATION_GITHUB_REPOSITORY',
        'AUTOMATION_GITHUB_REPO',
        'GITHUB_REPO',
        'GITHUB_REPOSITORY',
    ]
    repo_found = None
    for var in repo_vars:
        if os.environ.get(var):
            repo_found = var
            print_success(f"Repository setting found: {var}={os.environ.get(var)}")
            break
    
    if not repo_found:
        warnings.append("No repository setting found (optional for local use)")
        print_info("No repository setting (checked: " + ", ".join(repo_vars) + ")")
    
    # Check for project number (in GitHub Actions)
    project_num = os.environ.get('PROJECT_V2_NUMBER')
    if project_num:
        print_success(f"Project number configured: {project_num}")
    else:
        print_info("PROJECT_V2_NUMBER not set (required for auto-add to Projects)")
    
    return issues, warnings


def check_database():
    """Check if gaia.db exists and has backlog data."""
    print_header("Database Check")
    
    db_path = ROOT / 'gaia.db'
    if not db_path.exists():
        print_error(f"Database not found: {db_path}")
        print_info("Run: python agents/sync_backlog_to_db.py")
        return False
    
    print_success(f"Database found: {db_path}")
    
    # Try to read backlog table
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM backlog')
        count = cur.fetchone()[0]
        conn.close()
        
        if count > 0:
            print_success(f"Backlog table has {count} items")
            return True
        else:
            print_info("Backlog table is empty")
            return True
    except Exception as e:
        print_error(f"Error reading database: {e}")
        return False


def check_sync_agent():
    """Check if github_sessions_sync.py exists."""
    print_header("Sync Agent Check")
    
    agent_path = ROOT / 'agents' / 'github_sessions_sync.py'
    if not agent_path.exists():
        print_error(f"Sync agent not found: {agent_path}")
        return False
    
    print_success(f"Sync agent found: {agent_path}")
    return True


def check_workflow():
    """Check if sprint_onboard workflow exists."""
    print_header("Workflow Check")
    
    workflow_path = ROOT / '.github' / 'workflows' / 'sprint_onboard.yml'
    if not workflow_path.exists():
        print_error(f"Workflow not found: {workflow_path}")
        return False
    
    print_success(f"Workflow found: {workflow_path}")
    
    # Check if workflow contains PROJECT_V2_NUMBER
    content = workflow_path.read_text()
    if 'PROJECT_V2_NUMBER' in content:
        print_success("Workflow has GitHub Projects integration")
    else:
        print_info("Workflow does not reference PROJECT_V2_NUMBER")
    
    return True


def run_check():
    """Run all checks and report status."""
    print_header("GAIA GitHub Projects Integration Check")
    
    all_ok = True
    
    # Check GitHub CLI
    print_header("GitHub CLI Check")
    if check_github_cli():
        print_success("GitHub CLI (gh) is installed")
        
        if check_github_auth():
            print_success("GitHub CLI is authenticated")
        else:
            print_info("GitHub CLI not authenticated (optional)")
            print_info("Run: gh auth login")
    else:
        print_info("GitHub CLI (gh) not installed (optional)")
        print_info("Install from: https://cli.github.com/")
    
    # Check environment
    issues, warnings = check_environment()
    
    # Check database
    if not check_database():
        all_ok = False
    
    # Check sync agent
    if not check_sync_agent():
        all_ok = False
    
    # Check workflow
    if not check_workflow():
        all_ok = False
    
    # Final report
    print_header("Summary")
    
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print_error(issue)
        all_ok = False
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print_info(warning)
    
    if all_ok and not issues:
        print_success("All checks passed!")
        print("\nNext steps:")
        print("1. Configure PROJECT_V2_NUMBER secret in repository settings")
        print("2. Create a GitHub Project at: https://github.com/users/YOUR_USERNAME/projects")
        print("3. Test with: python scripts/setup_github_projects.py test")
        return 0
    else:
        print("\nSome checks failed. See errors above.")
        print("\nFor help, see: doc/GITHUB_PROJECTS_INTEGRATION.md")
        return 1


def run_configure(args):
    """Configure GitHub Projects integration."""
    print_header("Configure GitHub Projects Integration")
    
    if not args.project_number:
        print_error("Project number required. Use --project-number N")
        print_info("Find your project number in the URL: https://github.com/users/USER/projects/NUMBER")
        return 1
    
    print_info(f"Project number: {args.project_number}")
    print()
    print("To complete configuration, add this secret to your repository:")
    print()
    print("  1. Go to repository Settings → Secrets and variables → Actions")
    print("  2. Click 'New repository secret'")
    print("  3. Name: PROJECT_V2_NUMBER")
    print(f"  4. Value: {args.project_number}")
    print("  5. Click 'Add secret'")
    print()
    print("After adding the secret, issues labeled with 'sprint/*' will be")
    print("automatically added to your GitHub Project.")
    
    return 0


def run_test():
    """Test the sync agent in dry-run mode."""
    print_header("Test GitHub Sessions Sync")
    
    # Check if database exists
    db_path = ROOT / 'gaia.db'
    if not db_path.exists():
        print_error("Database not found. Run: python agents/sync_backlog_to_db.py")
        return 1
    
    # Run sync agent in dry-run mode
    agent_path = ROOT / 'agents' / 'github_sessions_sync.py'
    if not agent_path.exists():
        print_error("Sync agent not found")
        return 1
    
    print_info("Running sync agent in dry-run mode...")
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, str(agent_path), '--dry-run'],
            cwd=ROOT,
            check=False
        )
        
        if result.returncode == 0:
            print()
            print_success("Dry-run completed successfully")
            print()
            print("To sync for real, run:")
            print("  export AUTOMATION_GITHUB_TOKEN='your_token_here'")
            print("  export AUTOMATION_GITHUB_REPOSITORY='owner/repo'")
            print("  python agents/github_sessions_sync.py")
            return 0
        else:
            print()
            print_error("Dry-run failed")
            return 1
    except Exception as e:
        print_error(f"Error running sync agent: {e}")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Setup and configure GitHub Projects integration for GAIA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check current configuration
  python scripts/setup_github_projects.py check

  # Configure with project number
  python scripts/setup_github_projects.py configure --project-number 1

  # Test sync agent
  python scripts/setup_github_projects.py test

For more information, see: doc/GITHUB_PROJECTS_INTEGRATION.md
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Check command
    subparsers.add_parser('check', help='Check if GitHub Projects integration is configured')
    
    # Configure command
    configure_parser = subparsers.add_parser('configure', help='Configure GitHub Projects integration')
    configure_parser.add_argument(
        '--project-number',
        type=int,
        help='GitHub Project number (from URL)'
    )
    
    # Test command
    subparsers.add_parser('test', help='Test the sync agent in dry-run mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'check':
        return run_check()
    elif args.command == 'configure':
        return run_configure(args)
    elif args.command == 'test':
        return run_test()
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
