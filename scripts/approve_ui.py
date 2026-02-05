#!/usr/bin/env python3
"""Interactive approval UI for CHECKPOINT files.

Provides a small terminal menu to list checkpoints, view files, run a notifier dry-run,
approve checkpoints (interactive or non-interactive), and enable autonomy.

Safety: approvals use `scripts/approve_checkpoint.py`. Enabling autonomy requires
an explicit confirmation and (optionally) a present APPROVATO in the checkpoint file.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent


def list_checkpoints() -> List[Path]:
    return sorted(ROOT.glob('CHECKPOINT_*.md'))


def print_menu() -> None:
    print('\nApproval UI')
    print('1) List checkpoints')
    print('2) View checkpoint')
    print('3) Approve (interactive)')
    print('4) Approve (non-interactive --yes)')
    print('5) Run notifier one-shot DryRun')
    print('6) Enable autonomy (create .tmp/autonomous_mode.json)')
    print('7) Quit')


def view_checkpoint(n: int) -> None:
    p = ROOT / f'CHECKPOINT_{n}.md'
    if not p.exists():
        print('Missing', p)
        return
    print('\n---', p, '---')
    print(p.read_text(encoding='utf-8'))
    print('--- end ---')


def run_approve(n: int, signer: str | None = None, yes: bool = False) -> int:
    signer = signer or os.environ.get('USER') or os.environ.get('USERNAME') or 'approver'
    cmd = [sys.executable, str(ROOT / 'scripts' / 'approve_checkpoint.py'), '--checkpoint', str(n), '--signer', signer]
    if yes:
        cmd.append('--yes')
    print('Running:', ' '.join(cmd))
    return subprocess.call(cmd)


def run_dryrun_notifier() -> int:
    cmd = [sys.executable, str(ROOT / 'scripts' / 'telegram_realtime.py'), '--interval', '0']
    print('Running DryRun notifier:', ' '.join(cmd))
    return subprocess.call(cmd)


def enable_autonomy(require_approved: bool = True) -> None:
    cp = input('Which checkpoint number gated this enablement? (enter number) ') or '1'
    try:
        n = int(cp)
    except Exception:
        print('Invalid number')
        return
    p = ROOT / f'CHECKPOINT_{n}.md'
    if require_approved:
        if not p.exists() or 'APPROVATO' not in p.read_text(encoding='utf-8'):
            print('Checkpoint not approved - aborting. Use option 3/4 to approve first.')
            return
    confirm = input('Type ENABLE to create .tmp/autonomous_mode.json and enable autonomy: ')
    if confirm.strip() != 'ENABLE':
        print('Aborted')
        return
    tmp = ROOT / '.tmp'
    tmp.mkdir(exist_ok=True)
    am = tmp / 'autonomous_mode.json'
    am.write_text(json.dumps({'autonomous': True}, ensure_ascii=False), encoding='utf-8')
    print('Wrote', am)


def main() -> None:
    # If not running in a TTY, the interactive UI cannot proceed.
    if not sys.stdin.isatty():
        print('Approval UI requires a TTY. Use non-interactive scripts (e.g. --yes) in CI or run locally.')
        return

    while True:
        print_menu()
        choice = input('\nSelect an option: ').strip()
        if choice == '1':
            cps = list_checkpoints()
            if not cps:
                print('No checkpoints found')
            for p in cps:
                print('-', p.name)
        elif choice == '2':
            n = input('Checkpoint number: ').strip()
            try:
                view_checkpoint(int(n))
            except Exception:
                print('Invalid number')
        elif choice == '3':
            n = input('Checkpoint number to approve: ').strip()
            signer = input('Signer name (leave blank to use environment): ').strip() or None
            try:
                run_approve(int(n), signer=signer, yes=False)
            except Exception as e:
                print('Approve failed:', e)
        elif choice == '4':
            n = input('Checkpoint number to approve (non-interactive): ').strip()
            signer = input('Signer name (leave blank to use environment): ').strip() or None
            try:
                run_approve(int(n), signer=signer, yes=True)
            except Exception as e:
                print('Approve failed:', e)
        elif choice == '5':
            run_dryrun_notifier()
        elif choice == '6':
            enable_autonomy(require_approved=True)
        elif choice == '7' or choice.lower() in ('q', 'quit', 'exit'):
            print('Bye')
            return
        else:
            print('Unknown choice')


if __name__ == '__main__':
    main()
