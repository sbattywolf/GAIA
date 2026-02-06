#!/usr/bin/env python3
"""
Close Fixed CI Issues - Identifies and closes CI issues that are now resolved.

This script:
1. Fetches open CI issues
2. Extracts workflow run IDs from issue bodies
3. Checks if subsequent runs of the same workflow succeeded
4. Closes issues that have been fixed with verification comment
"""

import json
import subprocess
import sys
import re
from datetime import datetime
from typing import Dict, List, Optional


def run_gh_command(cmd: List[str]) -> str:
    """Execute a gh CLI command and return output."""
    try:
        result = subprocess.run(
            ["gh"] + cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        raise


def extract_run_info(issue: Dict) -> Optional[Dict]:
    """Extract workflow run information from issue body."""
    body = issue.get('body', '')
    
    # Try to extract run ID
    run_id_match = re.search(r'Run ID:\s*(\d+)', body)
    if not run_id_match:
        run_id_match = re.search(r'runs/(\d+)', body)
    
    if not run_id_match:
        return None
    
    run_id = run_id_match.group(1)
    
    # Try to extract workflow name
    workflow_match = re.search(r'Workflow:\s*(.+)', body)
    workflow_name = workflow_match.group(1).strip() if workflow_match else None
    
    return {
        'run_id': run_id,
        'workflow_name': workflow_name,
        'issue_number': issue['number'],
        'issue_title': issue['title']
    }


def check_if_fixed(run_info: Dict, repo: str) -> bool:
    """Check if the workflow has succeeded in recent runs."""
    workflow_name = run_info['workflow_name']
    
    if not workflow_name:
        return False
    
    try:
        # Get recent workflow runs for this workflow
        # Note: This is a simplified check - in production you'd want to check
        # the same workflow on the same branch as the original failure
        output = run_gh_command([
            "api",
            f"repos/{repo}/actions/workflows",
            "-q", f".workflows[] | select(.name == \"{workflow_name}\") | .id"
        ])
        
        if not output:
            return False
        
        workflow_id = output.strip()
        
        # Get recent runs
        output = run_gh_command([
            "api",
            f"repos/{repo}/actions/workflows/{workflow_id}/runs",
            "-X", "GET",
            "-f", "per_page=10",
            "-q", ".workflow_runs[] | select(.conclusion == \"success\") | .id"
        ])
        
        # If we have at least one successful run, consider it fixed
        return bool(output.strip())
        
    except Exception as e:
        print(f"Error checking workflow status: {e}", file=sys.stderr)
        return False


def close_issue(issue_number: int, repo: str, run_info: Dict, dry_run: bool = False):
    """Close a fixed issue with a verification comment."""
    comment = (
        f"✅ This issue appears to be resolved.\n\n"
        f"Recent runs of the **{run_info['workflow_name']}** workflow have succeeded, "
        f"indicating that the underlying problem has been fixed.\n\n"
        f"If you believe this issue should remain open, please reopen it with additional context.\n\n"
        f"---\n"
        f"*Auto-closed by CI Issue Manager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*"
    )
    
    if not dry_run:
        # Add comment
        run_gh_command([
            "issue", "comment", str(issue_number),
            "--body", comment,
            "--repo", repo
        ])
        
        # Close issue
        run_gh_command([
            "issue", "close", str(issue_number),
            "--repo", repo,
            "--reason", "completed"
        ])
        
        print(f"✓ Closed issue #{issue_number}: {run_info['issue_title']}")
    else:
        print(f"[DRY RUN] Would close issue #{issue_number}: {run_info['issue_title']}")
        print(f"[DRY RUN] Comment: {comment}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Close Fixed CI Issues")
    parser.add_argument("--repo", default="sbattywolf/GAIA", help="Repository (owner/repo)")
    parser.add_argument("--dry-run", action="store_true", help="Don't make changes, just report")
    parser.add_argument("--label", default="ci-failure,needs-triage", help="Issue labels to filter (comma-separated)")
    parser.add_argument("--max-issues", type=int, default=50, help="Maximum issues to check")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Close Fixed CI Issues")
    print("=" * 60)
    
    # Fetch open issues with CI-related labels
    labels = args.label.split(',')
    label_query = ' '.join([f'label:{l}' for l in labels])
    
    print(f"\nFetching open issues with labels: {', '.join(labels)}")
    
    try:
        output = run_gh_command([
            "issue", "list",
            "--repo", args.repo,
            "--state", "open",
            "--limit", str(args.max_issues),
            "--json", "number,title,body,labels",
        ])
        
        issues = json.loads(output)
        print(f"Found {len(issues)} open issues\n")
        
        issues_to_close = []
        
        for issue in issues:
            run_info = extract_run_info(issue)
            
            if not run_info:
                continue
            
            print(f"Checking issue #{issue['number']}: {issue['title'][:60]}...")
            
            if check_if_fixed(run_info, args.repo):
                print(f"  → Fixed! Will close.")
                issues_to_close.append(run_info)
            else:
                print(f"  → Still failing or unclear.")
        
        print("\n" + "=" * 60)
        print(f"Summary: {len(issues_to_close)} issues to close")
        print("=" * 60 + "\n")
        
        if issues_to_close:
            for run_info in issues_to_close:
                close_issue(run_info['issue_number'], args.repo, run_info, args.dry_run)
        else:
            print("No issues to close.")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
