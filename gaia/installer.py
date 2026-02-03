"""Installer shim that reuses `agents/environment_installer.py`."""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
AGENTS_ENV_INSTALLER = os.path.join(ROOT, 'agents', 'environment_installer.py')


def run_apply(apply=False, venv_path='.venv', requirements='requirements.txt', allow_system=False):
    cmd = [sys.executable, AGENTS_ENV_INSTALLER]
    if apply:
        cmd.append('--apply')
    cmd += ['--venv', venv_path, '--requirements', requirements]
    if allow_system:
        cmd.append('--allow-system')
    print('Invoking installer:', ' '.join(cmd))
    return subprocess.call(cmd)
