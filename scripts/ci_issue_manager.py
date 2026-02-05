#!/usr/bin/env python3
"""
CI Issue Manager - Collect, classify, and manage CI-related issues.

This script:
1. Fetches failed workflow runs from GitHub Actions
2. Classifies failures by type and urgency
3. Identifies duplicate issues
4. Verifies if issues are fixed (by checking recent successful runs)
5. Closes fixed issues with verification
6. Creates new issues for unfixed failures

Usage:
  From CLI with gh:
    python3 scripts/ci_issue_manager.py --dry-run
  
  With JSON data from GitHub MCP (for environments without gh CLI):
    python3 scripts/ci_issue_manager.py --runs-file workflow_runs.json --issues-file issues.json --dry-run
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from collections import defaultdict
import re


class CIIssueManager:
    def __init__(self, repo: str = "sbattywolf/GAIA", dry_run: bool = False, use_gh: bool = True):
        self.repo = repo
        self.dry_run = dry_run
        self.use_gh = use_gh
        self.workflow_runs: List[Dict] = []
        self.open_issues: List[Dict] = []
        self.failed_runs: List[Dict] = []
        self.classification: Dict[str, List[Dict]] = defaultdict(list)
        
    def run_gh_command(self, cmd: List[str]) -> str:
        """Execute a gh CLI command and return output."""
        if not self.use_gh:
            raise RuntimeError("gh CLI not available in this environment")
            
        env = os.environ.copy()
        # Ensure GH_TOKEN is available from GITHUB_TOKEN if needed
        if 'GH_TOKEN' not in env and 'GITHUB_TOKEN' in env:
            env['GH_TOKEN'] = env['GITHUB_TOKEN']
            
        try:
            result = subprocess.run(
                ["gh"] + cmd,
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running gh command: {e.stderr}", file=sys.stderr)
            raise

    def load_workflow_runs_from_file(self, filepath: str):
        """Load workflow runs from a JSON file."""
        print(f"Loading workflow runs from {filepath}...")
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and 'workflow_runs' in data:
            self.workflow_runs = data['workflow_runs']
        elif isinstance(data, list):
            self.workflow_runs = data
        else:
            raise ValueError("Invalid workflow runs data format")
        
        print(f"Loaded {len(self.workflow_runs)} workflow runs")
        
        # Filter for failed runs
        self.failed_runs = [
            run for run in self.workflow_runs
            if run.get('conclusion') in ['failure', 'action_required']
        ]
        print(f"Found {len(self.failed_runs)} failed runs")

    def load_issues_from_file(self, filepath: str):
        """Load issues from a JSON file."""
        print(f"Loading issues from {filepath}...")
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and 'issues' in data:
            self.open_issues = data['issues']
        elif isinstance(data, list):
            self.open_issues = data
        else:
            raise ValueError("Invalid issues data format")
        
        print(f"Loaded {len(self.open_issues)} issues")

    def fetch_workflow_runs(self, limit: int = 100):
        """Fetch recent workflow runs."""
        print(f"Fetching {limit} recent workflow runs...")
        output = self.run_gh_command([
            "api",
            f"repos/{self.repo}/actions/runs",
            f"--paginate",
            "-q", ".workflow_runs[]",
            "-X", "GET"
        ])
        
        runs = []
        for line in output.strip().split('\n'):
            if line:
                try:
                    runs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        self.workflow_runs = runs[:limit]
        print(f"Fetched {len(self.workflow_runs)} workflow runs")
        
        # Filter for failed runs
        self.failed_runs = [
            run for run in self.workflow_runs
            if run.get('conclusion') in ['failure', 'action_required']
        ]
        print(f"Found {len(self.failed_runs)} failed runs")

    def fetch_open_issues(self):
        """Fetch open issues, especially CI-related ones."""
        print("Fetching open issues...")
        output = self.run_gh_command([
            "api",
            f"repos/{self.repo}/issues",
            "-X", "GET",
            "-f", "state=open",
            "-f", "per_page=100",
            "-q", ".[]"
        ])
        
        issues = []
        for line in output.strip().split('\n'):
            if line:
                try:
                    issues.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        self.open_issues = issues
        print(f"Fetched {len(self.open_issues)} open issues")

    def classify_failure(self, run: Dict) -> Dict[str, str]:
        """Classify a workflow run failure by type and urgency."""
        workflow_name = run.get('name', '')
        path = run.get('path', '')
        conclusion = run.get('conclusion', 'unknown')
        
        # Determine type
        failure_type = 'unknown'
        if 'secret' in workflow_name.lower() or 'secret' in path.lower():
            failure_type = 'security'
        elif 'test' in workflow_name.lower() or 'pytest' in workflow_name.lower():
            failure_type = 'test'
        elif 'ci' in workflow_name.lower() or 'ci' in path.lower():
            failure_type = 'ci'
        elif 'integration' in workflow_name.lower():
            failure_type = 'integration'
        elif 'build' in workflow_name.lower():
            failure_type = 'build'
        elif 'triage' in workflow_name.lower():
            failure_type = 'triage'
        
        # Determine urgency
        urgency = 'medium'
        if failure_type == 'security':
            urgency = 'critical'
        elif failure_type in ['ci', 'build']:
            urgency = 'high'
        elif failure_type in ['test', 'integration']:
            urgency = 'high'
        elif conclusion == 'action_required':
            urgency = 'high'
        
        return {
            'type': failure_type,
            'urgency': urgency,
            'workflow_name': workflow_name,
            'path': path
        }

    def classify_all_failures(self):
        """Classify all failed workflow runs."""
        print("Classifying failures...")
        for run in self.failed_runs:
            classification = self.classify_failure(run)
            run['classification'] = classification
            self.classification[classification['urgency']].append(run)
        
        print(f"Classification summary:")
        for urgency in ['critical', 'high', 'medium', 'low']:
            count = len(self.classification[urgency])
            if count > 0:
                print(f"  {urgency}: {count} failures")

    def is_failure_fixed(self, run: Dict) -> bool:
        """Check if a workflow failure has been fixed by finding recent successful runs."""
        workflow_id = run.get('workflow_id')
        head_branch = run.get('head_branch')
        created_at = run.get('created_at')
        
        if not all([workflow_id, head_branch, created_at]):
            return False
        
        # Look for successful runs of the same workflow on the same branch after this failure
        for recent_run in self.workflow_runs:
            if (recent_run.get('workflow_id') == workflow_id and
                recent_run.get('head_branch') == head_branch and
                recent_run.get('conclusion') == 'success' and
                recent_run.get('created_at') > created_at):
                return True
        
        return False

    def find_duplicate_issues(self, run: Dict) -> Optional[int]:
        """Find if an issue already exists for this workflow run."""
        run_id = run.get('id')
        workflow_name = run.get('name')
        
        # Look for issues with matching run ID or workflow name in title
        for issue in self.open_issues:
            title = issue.get('title', '')
            body = issue.get('body', '')
            
            # Check for explicit run ID
            if str(run_id) in title or str(run_id) in body:
                return issue['number']
            
            # Check for workflow name pattern
            if f"CI failure: run {run_id}" == title:
                return issue['number']
        
        return None

    def close_fixed_issue(self, issue_number: int, run: Dict):
        """Close an issue that has been verified as fixed."""
        print(f"Closing issue #{issue_number} (fixed)")
        
        comment = (
            f"✅ This issue has been verified as fixed.\n\n"
            f"A recent successful run of the same workflow confirms the fix:\n"
            f"- Workflow: {run['name']}\n"
            f"- Branch: {run['head_branch']}\n"
            f"- Fixed: {datetime.now().isoformat()}\n"
        )
        
        if not self.dry_run:
            # Add comment
            self.run_gh_command([
                "issue", "comment", str(issue_number),
                "--body", comment,
                "--repo", self.repo
            ])
            
            # Close issue
            self.run_gh_command([
                "issue", "close", str(issue_number),
                "--repo", self.repo,
                "--reason", "completed"
            ])
        else:
            print(f"[DRY RUN] Would close issue #{issue_number}")
            print(f"[DRY RUN] Comment: {comment}")

    def create_issue_for_failure(self, run: Dict) -> Optional[int]:
        """Create a new issue for an unfixed failure."""
        classification = run.get('classification', {})
        urgency = classification.get('urgency', 'medium')
        failure_type = classification.get('type', 'unknown')
        
        title = f"CI failure: {run['name']} (run {run['id']})"
        
        body = (
            f"### CI Failure Details\n\n"
            f"- **Workflow**: {run['name']}\n"
            f"- **Run ID**: {run['id']}\n"
            f"- **Branch**: {run['head_branch']}\n"
            f"- **Conclusion**: {run['conclusion']}\n"
            f"- **Created**: {run['created_at']}\n"
            f"- **Type**: {failure_type}\n"
            f"- **Urgency**: {urgency}\n\n"
            f"**Run URL**: {run['html_url']}\n\n"
            f"**Logs**: Check the workflow run for detailed logs.\n\n"
            f"---\n"
            f"*Auto-generated by CI Issue Manager*\n"
        )
        
        labels = ['ci', 'bug', urgency]
        if failure_type == 'security':
            labels.append('security')
        elif failure_type in ['test', 'integration']:
            labels.append('testing')
        
        if not self.dry_run:
            output = self.run_gh_command([
                "issue", "create",
                "--title", title,
                "--body", body,
                "--label", ",".join(labels),
                "--repo", self.repo
            ])
            
            # Extract issue number from output
            match = re.search(r'#(\d+)', output)
            if match:
                issue_number = int(match.group(1))
                print(f"Created issue #{issue_number} for run {run['id']}")
                return issue_number
        else:
            print(f"[DRY RUN] Would create issue:")
            print(f"  Title: {title}")
            print(f"  Labels: {', '.join(labels)}")
        
        return None

    def generate_report(self) -> Dict:
        """Generate a comprehensive report of CI issues."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_runs': len(self.workflow_runs),
                'failed_runs': len(self.failed_runs),
                'open_issues': len(self.open_issues),
            },
            'failures_by_urgency': {},
            'failures_by_type': defaultdict(int),
            'fixed_failures': [],
            'unfixed_failures': [],
            'duplicate_issues': [],
        }
        
        for urgency in ['critical', 'high', 'medium', 'low']:
            report['failures_by_urgency'][urgency] = len(self.classification[urgency])
        
        for run in self.failed_runs:
            classification = run.get('classification', {})
            failure_type = classification.get('type', 'unknown')
            report['failures_by_type'][failure_type] += 1
            
            is_fixed = self.is_failure_fixed(run)
            duplicate_issue = self.find_duplicate_issues(run)
            
            failure_info = {
                'run_id': run['id'],
                'workflow': run['name'],
                'branch': run['head_branch'],
                'urgency': classification.get('urgency'),
                'type': failure_type,
                'url': run['html_url'],
            }
            
            if is_fixed:
                failure_info['status'] = 'fixed'
                report['fixed_failures'].append(failure_info)
                
                if duplicate_issue:
                    report['duplicate_issues'].append({
                        'issue_number': duplicate_issue,
                        'run_id': run['id'],
                        'should_close': True
                    })
            else:
                failure_info['status'] = 'unfixed'
                report['unfixed_failures'].append(failure_info)
                
                if duplicate_issue:
                    failure_info['existing_issue'] = duplicate_issue
                    report['duplicate_issues'].append({
                        'issue_number': duplicate_issue,
                        'run_id': run['id'],
                        'should_close': False
                    })
        
        return report

    def save_report(self, report: Dict, filename: str = "ci_issues_report.json"):
        """Save report to a file."""
        filepath = f"/home/runner/work/GAIA/GAIA/{filename}"
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {filepath}")

    def process_all(self):
        """Main processing pipeline."""
        print("=" * 60)
        print("CI Issue Manager - Starting")
        print("=" * 60)
        
        # Verify we have data
        if not self.workflow_runs:
            print("ERROR: No workflow runs loaded!", file=sys.stderr)
            return
        if not self.open_issues:
            print("ERROR: No issues loaded!", file=sys.stderr)
            return
        
        # Classify failures
        self.classify_all_failures()
        
        # Generate report
        report = self.generate_report()
        
        # Process fixed issues
        print("\n" + "=" * 60)
        print("Processing Fixed Issues")
        print("=" * 60)
        fixed_count = 0
        for dup in report['duplicate_issues']:
            if dup['should_close']:
                run_id = dup['run_id']
                run = next((r for r in self.failed_runs if r['id'] == run_id), None)
                if run:
                    self.close_fixed_issue(dup['issue_number'], run)
                    fixed_count += 1
        print(f"Closed {fixed_count} fixed issues")
        
        # Create new issues for unfixed failures
        print("\n" + "=" * 60)
        print("Creating Issues for Unfixed Failures")
        print("=" * 60)
        created_count = 0
        for failure in report['unfixed_failures']:
            if 'existing_issue' not in failure:
                run_id = failure['run_id']
                run = next((r for r in self.failed_runs if r['id'] == run_id), None)
                if run and failure['urgency'] in ['critical', 'high']:
                    self.create_issue_for_failure(run)
                    created_count += 1
        print(f"Created {created_count} new issues")
        
        # Save report
        self.save_report(report)
        
        # Print summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Total workflow runs analyzed: {report['summary']['total_runs']}")
        print(f"Failed runs: {report['summary']['failed_runs']}")
        print(f"Open CI issues: {report['summary']['open_issues']}")
        print(f"\nFailures by urgency:")
        for urgency, count in report['failures_by_urgency'].items():
            if count > 0:
                print(f"  {urgency}: {count}")
        print(f"\nFixed failures identified: {len(report['fixed_failures'])}")
        print(f"Unfixed failures: {len(report['unfixed_failures'])}")
        print(f"Issues closed: {fixed_count}")
        print(f"New issues created: {created_count}")
        print("\n" + "=" * 60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="CI Issue Manager")
    parser.add_argument("--repo", default="sbattywolf/GAIA", help="Repository (owner/repo)")
    parser.add_argument("--dry-run", action="store_true", help="Don't make changes, just report")
    parser.add_argument("--limit", type=int, default=100, help="Number of workflow runs to fetch")
    parser.add_argument("--runs-file", help="Load workflow runs from JSON file instead of fetching")
    parser.add_argument("--issues-file", help="Load issues from JSON file instead of fetching")
    parser.add_argument("--use-gh", action="store_true", default=False, help="Use gh CLI (requires GH_TOKEN)")
    
    args = parser.parse_args()
    
    manager = CIIssueManager(repo=args.repo, dry_run=args.dry_run, use_gh=args.use_gh)
    
    # Load data from files or fetch via API
    if args.runs_file:
        manager.load_workflow_runs_from_file(args.runs_file)
    elif args.use_gh:
        manager.fetch_workflow_runs(limit=args.limit)
    else:
        print("Error: Either --runs-file or --use-gh must be specified", file=sys.stderr)
        sys.exit(1)
    
    if args.issues_file:
        manager.load_issues_from_file(args.issues_file)
    elif args.use_gh:
        manager.fetch_open_issues()
    else:
        print("Error: Either --issues-file or --use-gh must be specified", file=sys.stderr)
        sys.exit(1)
    
    manager.process_all()


if __name__ == "__main__":
    main()
