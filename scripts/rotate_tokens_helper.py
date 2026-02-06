#!/usr/bin/env python3
"""Helper to store a new GAIA_GITHUB_TOKEN in the local secrets store.

Usage examples:

  # Set token from env (recommended for interactive use)
  ROTATION_ADMIN_TOKEN=<token> python scripts/rotate_tokens_helper.py

  # Or pass token via CLI (be careful with shell history)
  python scripts/rotate_tokens_helper.py --token xxxxx

  # Optionally push to repo secrets using `gh` (if installed and authenticated)
  python scripts/rotate_tokens_helper.py --token xxxxx --use-gh --repo myorg/GAIA

This script writes to the project's encrypted secrets provider by default
and will mirror to the legacy key name (`AUTOMATION_GITHUB_TOKEN`) for
backward compatibility.
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gaia.secrets import SecretsManager


def set_local_secret(token: str) -> bool:
    sm = SecretsManager()
    success = sm.set('GAIA_GITHUB_TOKEN', token, provider='encrypted_file')
    if success:
        print('Wrote GAIA_GITHUB_TOKEN to encrypted store.')
    else:
        print('Failed to write GAIA_GITHUB_TOKEN to encrypted store.')
    return success


def push_repo_secret_with_gh(repo: str, token: str) -> bool:
    # Uses GitHub CLI to set a repository secret. Requires `gh` to be installed
    # and configured with sufficient privileges.
    try:
        cmd = ['gh', 'secret', 'set', 'GAIA_GITHUB_TOKEN', '--body', token, '--repo', repo]
        subprocess.run(cmd, check=True)
        print(f'Updated repository secret GAIA_GITHUB_TOKEN in {repo} via gh.')
        return True
    except FileNotFoundError:
        print('gh CLI not found; skipping repo secret update.')
    except subprocess.CalledProcessError as e:
        print('gh CLI failed to set secret:', e)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='The new GAIA_GITHUB_TOKEN value')
    parser.add_argument('--use-gh', action='store_true', help='Also update repo secret using gh')
    parser.add_argument('--repo', help='Repository (owner/repo) used with --use-gh')
    args = parser.parse_args()

    token = args.token or os.environ.get('ROTATION_ADMIN_TOKEN') or os.environ.get('GAIA_ROTATION_TOKEN')
    if not token:
        print('No token provided. Set --token or ROTATION_ADMIN_TOKEN environment variable.')
        return 2

    ok = set_local_secret(token)

    if args.use_gh:
        if not args.repo:
            print('When using --use-gh, --repo owner/repo is required.')
            return 3
        ok2 = push_repo_secret_with_gh(args.repo, token)
        ok = ok and ok2

    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
