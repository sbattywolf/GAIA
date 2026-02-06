#!/usr/bin/env python3
"""
Load a .env file and run a command so scheduled services inherit required env vars.

Usage:
  python scripts/env_loader.py --env .private/.env -- python scripts/approval_listener_runner.py

Behavior:
- Parses simple KEY=VALUE lines (ignores comments and blank lines).
- Sets values into `os.environ` (overwrites existing keys).
- Executes the provided command in a child process.
"""
import os
import sys
import argparse
import subprocess


def load_env(path: str):
    if not os.path.exists(path):
        print(f'Env file not found: {path}', file=sys.stderr)
        return
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            os.environ[k] = v


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='.private/.env', help='Path to env file')
    parser.add_argument('cmd', nargs=argparse.REMAINDER, help='Command to run (prefix with --)')
    args = parser.parse_args()

    if not args.cmd:
        print('No command specified. Use -- to separate command. Example: -- python script.py', file=sys.stderr)
        return 2

    # Prefer an externally supplied path via PRIVATE_ENV_PATH to allow secrets
    # to live outside the repository (Option A).
    env_path = os.environ.get('PRIVATE_ENV_PATH') or args.env
    if env_path != args.env:
        print(f'Using external env path from PRIVATE_ENV_PATH: {env_path}', file=sys.stderr)
    load_env(env_path)

    # If cmd starts with '--', strip it
    cmd = args.cmd
    if cmd and cmd[0] == '--':
        cmd = cmd[1:]

    # Execute the command and forward exit code
    try:
        p = subprocess.run(cmd)
        return p.returncode
    except FileNotFoundError:
        print(f'Command not found: {cmd[0]}', file=sys.stderr)
        return 127
    except Exception as e:
        print(f'Error running command: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
