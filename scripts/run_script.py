#!/usr/bin/env python3
"""Run an arbitrary script reliably using the correct interpreter.

Purpose: avoid accidentally sending shell commands into a Python REPL and
provide a consolidated way for the local agent to run scripts of different
languages. Logs runs to `.private/script_runner.log`.

Usage:
  python scripts/run_script.py /path/to/script [--args ...]

Behavior:
 - Chooses interpreter by extension: .py, .ps1, .sh, .bat/.cmd, .jar, .js
 - Uses project's venv python if present at `.venv\Scripts\python.exe` on Windows
 - Runs the command as a subprocess and returns the same exit code
"""
from __future__ import annotations
import sys
from pathlib import Path
import subprocess
import shlex
import logging

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / '.private' / 'script_runner.log'
LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, filename=str(LOG), filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')


def find_python() -> str:
    venv_py = ROOT / '.venv' / 'Scripts' / 'python.exe'
    if venv_py.exists():
        return str(venv_py)
    return sys.executable or 'python'


def build_command(script_path: Path, script_args: list[str]) -> list[str] | str:
    ext = script_path.suffix.lower()
    if ext == '.py':
        return [find_python(), str(script_path)] + script_args
    if ext == '.ps1':
        # Use PowerShell to run script file
        return ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script_path)] + script_args
    if ext in ('.bat', '.cmd'):
        return ['cmd', '/c', str(script_path)] + script_args
    if ext == '.sh':
        return ['bash', str(script_path)] + script_args
    if ext == '.jar':
        return ['java', '-jar', str(script_path)] + script_args
    if ext == '.js':
        return ['node', str(script_path)] + script_args
    # fallback: run via shell
    return ' '.join(shlex.quote(str(script_path)) + (' ' + ' '.join(shlex.quote(a) for a in script_args) if script_args else ''))


def run(script: str, args: list[str]) -> int:
    script_path = Path(script)
    if not script_path.exists():
        logging.error('Script not found: %s', script)
        print('Script not found:', script, file=sys.stderr)
        return 2

    cmd = build_command(script_path, args)
    logging.info('Running script %s with command %s', script_path, cmd)
    try:
        if isinstance(cmd, list):
            p = subprocess.run(cmd)
        else:
            p = subprocess.run(cmd, shell=True)
        logging.info('Script exit %s for %s', p.returncode, script_path)
        return p.returncode
    except FileNotFoundError as e:
        logging.exception('Interpreter not found: %s', e)
        print('Interpreter not found:', e, file=sys.stderr)
        return 3
    except Exception as e:
        logging.exception('Failed to run script: %s', e)
        print('Failed to run script:', e, file=sys.stderr)
        return 4


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print('Usage: run_script.py /path/to/script [args...]', file=sys.stderr)
        return 2
    script = argv[0]
    args = argv[1:]
    return run(script, args)


if __name__ == '__main__':
    raise SystemExit(main())
