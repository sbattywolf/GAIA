#!/usr/bin/env python3
"""
Simple environment installer agent for GAIA.
- Dry-run (default): shows commands and writes a `install.dryrun` event to `events.ndjson`.
- Apply: creates a venv and runs `pip install -r requirements.txt` using the venv's python.

Usage:
  python agents/environment_installer.py [--apply] [--venv .venv] [--requirements requirements.txt]

Note: System-level installers (choco/winget) are printed as commands and NOT executed unless explicitly allowed.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import uuid

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')


def timestamp():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def append_event(evt):
    try:
        with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, default=str) + '\n')
    except Exception as e:
        print('WARN: failed to append event:', e)


def run_cmd(cmd, env=None, capture=False):
    print('RUN:', ' '.join(cmd) if isinstance(cmd, (list, tuple)) else cmd)
    if capture:
        return subprocess.check_output(cmd, env=env, shell=False)
    else:
        return subprocess.check_call(cmd, env=env, shell=False)


def create_venv(venv_path):
    import venv
    builder = venv.EnvBuilder(with_pip=True)
    print('Creating venv at', venv_path)
    builder.create(venv_path)


def venv_python(venv_path):
    if os.name == 'nt':
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        return os.path.join(venv_path, 'bin', 'python')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--apply', action='store_true', help='Actually perform installs (default is dry-run)')
    p.add_argument('--venv', default=os.path.join(ROOT, '.venv'), help='Path to virtualenv')
    p.add_argument('--requirements', default=os.path.join(ROOT, 'requirements.txt'), help='Path to requirements.txt')
    p.add_argument('--allow-system', action='store_true', help='Allow running system package manager commands (NOT recommended)')
    args = p.parse_args()

    plan = []
    plan.append({'step': 'create_venv', 'path': args.venv})
    plan.append({'step': 'pip_install', 'requirements': args.requirements})
    # Example system installs: (not executed unless --allow-system)
    plan.append({'step': 'choco', 'cmd': ['choco', 'install', 'git', 'python']})
    plan.append({'step': 'winget', 'cmd': ['winget', 'install', '--id', 'Git.Git']})

    event = {
        'type': 'install.start' if args.apply else 'install.dryrun',
        'source': os.path.basename(os.getcwd()),
        'target': os.path.basename(os.getcwd()),
        'timestamp': timestamp(),
        'trace_id': str(uuid.uuid4()),
        'payload': {
            'plan': plan,
            'apply': bool(args.apply),
        }
    }

    append_event(event)

    if not args.apply:
        print('\nDry-run mode: the installer would perform these steps:')
        for s in plan:
            if s['step'] == 'create_venv':
                print('- create venv at', s['path'])
            elif s['step'] == 'pip_install':
                print('- pip install -r', s['requirements'])
            else:
                print('- system command:', s['cmd'])
        print('\nTo apply: run with --apply')
        return 0

    # Apply mode
    try:
        # 1) create venv
        create_venv(args.venv)
        py = venv_python(args.venv)
        if not os.path.exists(py):
            print('ERROR: venv python not found at', py)
            return 2

        # 2) pip install -r requirements
        if os.path.exists(args.requirements):
            print('Installing pip requirements from', args.requirements)
            run_cmd([py, '-m', 'pip', 'install', '--upgrade', 'pip'])
            run_cmd([py, '-m', 'pip', 'install', '-r', args.requirements])
        else:
            print('WARN: requirements file not found at', args.requirements)

        # 3) system packages (only if allowed)
        if args.allow_system:
            print('Running system package manager commands (as allowed)')
            try:
                run_cmd(['choco', 'install', 'git', 'python'])
            except Exception as e:
                print('WARN: choco step failed or choco unavailable:', e)
        else:
            print('Skipping system package manager steps; use --allow-system to enable (not recommended)')

        evt = {
            'type': 'install.success',
            'source': os.path.basename(os.getcwd()),
            'target': os.path.basename(os.getcwd()),
            'timestamp': timestamp(),
            'trace_id': event['trace_id'],
            'payload': {
                'venv': args.venv,
                'requirements': args.requirements,
            }
        }
        append_event(evt)
        print('\nInstall completed successfully.')
        return 0
    except subprocess.CalledProcessError as e:
        print('ERROR: command failed:', e)
        evt = {
            'type': 'install.failure',
            'source': os.path.basename(os.getcwd()),
            'target': os.path.basename(os.getcwd()),
            'timestamp': timestamp(),
            'trace_id': event['trace_id'],
            'payload': {'error': str(e)}
        }
        append_event(evt)
        return 3
    except Exception as e:
        print('ERROR:', e)
        evt = {
            'type': 'install.failure',
            'source': os.path.basename(os.getcwd()),
            'target': os.path.basename(os.getcwd()),
            'timestamp': timestamp(),
            'trace_id': event['trace_id'],
            'payload': {'error': str(e)}
        }
        append_event(evt)
        return 4


if __name__ == '__main__':
    sys.exit(main())
