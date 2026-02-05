"""Checkpoint gating helper.

Provides a simple mechanism to require human approval before executing
high-impact steps. Checkpoint files live at the repository root and are
named `CHECKPOINT_<n>.md`. A checkpoint is considered approved when the
file contains the token `APPROVATO` (case-insensitive).
"""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def checkpoint_path(n: int) -> Path:
    return ROOT / f'CHECKPOINT_{n}.md'


def is_checkpoint_approved(n: int) -> bool:
    p = checkpoint_path(n)
    if not p.exists():
        return False
    try:
        txt = p.read_text(encoding='utf-8')
        return 'approvato' in txt.lower()
    except Exception:
        return False


def require_checkpoint(n: int, action: str = 'high-impact action') -> None:
    if not is_checkpoint_approved(n):
        print(f'Checkpoint {n} not approved; not performing {action}. Add APPROVATO to {checkpoint_path(n)} to proceed.')
        raise SystemExit(0)
