#!/usr/bin/env python3
"""CLI to safely approve a CHECKPOINT_<n>.md by adding APPROVATO.

Usage:
  python scripts/approve_checkpoint.py --checkpoint 1 --signer "Carlo" --message "OK" [--yes]

Behavior:
 - Shows the checkpoint file, requires interactive confirmation by typing APPROVATO
   unless `--yes` is passed.
 - Appends an approval line with signer and timestamp.
 - Emits a `checkpoint.approved` event to `events.ndjson` and writes an audit row.
"""
from __future__ import annotations

import argparse
import sys
import os
import json
from datetime import datetime
from pathlib import Path
import getpass


ROOT = Path(__file__).resolve().parent.parent
EVENTS_FILE = ROOT / 'events.ndjson'


def checkpoint_path(n: int) -> Path:
    return ROOT / f'CHECKPOINT_{n}.md'


def ensure_checkpoint_file(p: Path) -> None:
    if not p.exists():
        p.write_text(f"CHECKPOINT {p.stem}\n\nAdd APPROVATO to this file to approve.\n", encoding='utf-8')


def append_approval(p: Path, signer: str, message: str) -> None:
    ts = datetime.utcnow().isoformat() + 'Z'
    line = f"\nAPPROVATO by {signer} at {ts}\nMessage: {message}\n"
    with open(p, 'a', encoding='utf-8') as f:
        f.write(line)


def emit_event(n: int, signer: str, message: str) -> None:
    ev = {
        'type': 'checkpoint.approved',
        'source': 'approve_checkpoint',
        'checkpoint': n,
        'signer': signer,
        'message': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    try:
        with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(ev, ensure_ascii=False) + '\n')
    except Exception:
        pass
    # best-effort audit write
    try:
        import orchestrator
        orchestrator.write_audit('approve_checkpoint', 'checkpoint.approved', json.dumps(ev, ensure_ascii=False))
    except Exception:
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--checkpoint', type=int, default=1)
    p.add_argument('--signer', type=str, default=None)
    p.add_argument('--message', type=str, default='')
    p.add_argument('--yes', action='store_true', help='Non-interactive: approve without typing token')
    args = p.parse_args()

    cp = checkpoint_path(args.checkpoint)
    ensure_checkpoint_file(cp)

    print(f"Checkpoint file: {cp}")
    print('--- current content ---')
    print(cp.read_text(encoding='utf-8'))
    print('-----------------------')

    signer = args.signer or os.environ.get('USER') or os.environ.get('USERNAME') or getpass.getuser()

    # Non-interactive CI safety: require --yes when stdin is not a TTY
    if not args.yes and not sys.stdin.isatty():
        print('Non-interactive environment detected: pass --yes to approve non-interactively or run locally.')
        raise SystemExit(2)

    if not args.yes:
        confirm = input("Type APPROVATO to confirm approval (case-sensitive): ")
        if confirm.strip() != 'APPROVATO':
            print('Approval aborted (token mismatch).')
            raise SystemExit(1)

    append_approval(cp, signer, args.message or '')
    emit_event(args.checkpoint, signer, args.message or '')
    print(f'Checkpoint {args.checkpoint} approved by {signer}')


if __name__ == '__main__':
    main()
