"""Run a command with environment loaded from `.tmp/telegram.env`.

This avoids shell/REPL quoting issues by using a small Python wrapper.

Usage examples:
  # run the tg_command_manager list command
  python scripts/run_with_env.py python scripts/tg_command_manager.py list

  # execute a command with args
  python scripts/run_with_env.py python scripts/tg_command_manager.py execute <id> --execute

The script loads key=value lines from `.tmp/telegram.env` into the process
environment before executing the provided subprocess. It prints stdout/stderr
and returns the subprocess exit code.
"""
from __future__ import annotations
import os
import re
import sys
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / '.tmp' / 'telegram.env'


def load_env(path: Path):
    if not path.exists():
        return {}
    env = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    os.environ.update(env)
    return env


def main(argv: list[str]):
    if not argv:
        print('Usage: python scripts/run_with_env.py <command> [args...]')
        return 2
    loaded = load_env(ENV_PATH)
    if loaded:
        print('Loaded env from', ENV_PATH)
    else:
        print('No env file at', ENV_PATH)

    cmd = argv
    print('Running:', ' '.join(cmd))
    try:
        proc = subprocess.run(cmd, check=False)
        return proc.returncode
    except KeyboardInterrupt:
        print('Interrupted')
        return 130
    except Exception as e:
        print('Error running command:', e)
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
