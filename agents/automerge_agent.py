#!/usr/bin/env python3
"""Simple opt-in automerge agent for prototype mode.

Requirements: `gh` CLI available on PATH and authenticated for a user with repo permissions.

Usage:
  python agents/automerge_agent.py [--dry-run]

Behavior:
- Lists open PRs labeled `automerge`.
- For each PR, checks combined status for the PR head SHA.
- If combined status is 'success', attempts to `gh pr merge --squash` the PR.
- Honors `--dry-run` to only print actions.

This is intentionally simple and CLI-driven to avoid embedding secrets.
"""
import argparse
import json
import subprocess
import sys
import re


def run(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)


def get_repo():
    try:
        url = run(['git', 'remote', 'get-url', 'origin']).strip()
    except Exception:
        print('Unable to determine git remote origin URL; set AUTOMATION_GITHUB_REPOSITORY env or run from a git repo.', file=sys.stderr)
        return None
    # parse owner/repo from URL formats
    m = re.search(r'[:/]([^/]+/[^/]+?)(?:\.git)?$', url)
    if not m:
        return None
    return m.group(1)


def list_automerge_prs():
    out = run(['gh', 'pr', 'list', '--state', 'open', '--label', 'automerge', '--json', 'number,headRefName,headRefOid,author'])
    return json.loads(out)


def get_combined_status(repo, sha):
    # GET /repos/{owner}/{repo}/commits/{ref}/status
    out = run(['gh', 'api', f'/repos/{repo}/commits/{sha}/status'])
    data = json.loads(out)
    return data.get('state')


def merge_pr(num, dry_run=False):
    if dry_run:
        print(f'[DRY-RUN] Would merge PR #{num} (squash)')
        return True
    try:
        print(f'Merging PR #{num}...')
        out = run(['gh', 'pr', 'merge', str(num), '--squash', '--delete-branch', '--confirm'])
        print(out)
        return True
    except subprocess.CalledProcessError as e:
        print(f'Failed to merge PR #{num}:', e.output, file=sys.stderr)
        return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    repo = get_repo() or (run(['gh', 'repo', 'view', '--json', 'nameWithOwner']).strip())
    if isinstance(repo, str) and repo.startswith('{'):
        repo = json.loads(repo).get('nameWithOwner')
    if not repo:
        print('Could not determine repository owner/name; exiting.', file=sys.stderr)
        sys.exit(1)

    prs = list_automerge_prs()
    if not prs:
        print('No open PRs labeled automerge found.')
        return

    for pr in prs:
        num = pr.get('number')
        sha = pr.get('headRefOid')
        author = (pr.get('author') or {}).get('login')
        print(f'PR #{num} (head {sha}) author={author}')
        try:
            state = get_combined_status(repo, sha)
        except subprocess.CalledProcessError as e:
            print(f'Failed to fetch status for {sha}:', e.output, file=sys.stderr)
            continue
        print(f'Combined status: {state}')
        if state and state.lower() == 'success':
            merge_pr(num, dry_run=args.dry_run)
        else:
            print(f'Skipping PR #{num}: combined status is {state}')


if __name__ == '__main__':
    main()
