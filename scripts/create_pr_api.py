#!/usr/bin/env python3
"""Create a pull request using GitHub REST API using token from .private/.env

This script will load `.private/.env` (if present) via `env_loader.load_env()`
and then call the GitHub API to create a PR from `feat/copilot-autowork` -> `main`.

It avoids printing secrets.
"""
import os
import sys
import json
from pathlib import Path

try:
    # attempt to import env_loader from scripts (repo root should be in sys.path)
    from scripts import env_loader
except Exception:
    # try to load by path as a fallback
    spec_path = Path(__file__).resolve().parent / 'env_loader.py'
    if spec_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('env_loader', str(spec_path))
        env_loader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(env_loader)

def main():
    # load local env file if present
    env_path = Path(__file__).resolve().parent.parent / '.private' / '.env'
    if env_path.exists():
        try:
            env_loader.load_env(str(env_path))
        except Exception:
            pass

    # Prefer automation-specific token variables used by repo tooling
    # Use `GAIA_GITHUB_TOKEN` when available, fall back to legacy names.
    try:
        from gaia.env_helpers import get_github_token
        token = get_github_token()
    except Exception:
        token = os.environ.get('AUTOMATION_GITHUB_TOKEN')
    if not token:
        print('No GitHub token found in environment (.private/.env or env vars). Aborting.', file=sys.stderr)
        return 2

    # Allow automation to override target repository via env (avoid relying on GITHUB_* vars)
    repo_override = os.environ.get('AUTOMATION_GITHUB_REPOSITORY') or os.environ.get('AUTOMATION_GITHUB_REPO')
    if repo_override and '/' in repo_override:
        owner, repo = repo_override.split('/', 1)
    else:
        owner = 'sbattywolf'
        repo = 'GAIA'
    head = 'feat/copilot-autowork'
    base = 'main'
    title = 'feat: copilot autowork — approvals & notifier'
    body = 'Adds approval extractor + tests, improves telegram queue retry/backoff, and fixes claim_cli import path.'

    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    payload = {'title': title, 'head': head, 'base': base, 'body': body}

    try:
        import requests
    except Exception:
        print('The `requests` library is required to run this script.', file=sys.stderr)
        return 3

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json'
    }

    r = requests.post(url, headers=headers, json=payload, timeout=15)
    if r.status_code in (200, 201):
        data = r.json()
        pr_url = data.get('html_url')
        print('PR created:', pr_url)
        return 0
    else:
        # print error summary without exposing token
        try:
            err = r.json()
        except Exception:
            err = {'status_code': r.status_code, 'text': r.text}
        print('Failed to create PR. Response:', json.dumps(err, indent=2) , file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
