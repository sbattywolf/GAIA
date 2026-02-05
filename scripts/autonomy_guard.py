"""Autonomy guard helper.

Provides a small helper to check the single source-of-truth toggle
at `.tmp/autonomous_mode.json`. If not enabled, callers may abort
before performing side-effecting actions.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict


ROOT = Path(__file__).resolve().parent.parent


def read_autonomy_file() -> Dict[str, object]:
    p = ROOT / '.tmp' / 'autonomous_mode.json'
    if not p.exists():
        return {"autonomous": False}
    try:
        # accept files with a UTF-8 BOM (use utf-8-sig to strip it)
        return json.loads(p.read_text(encoding='utf-8-sig'))
    except Exception:
        return {"autonomous": False}


def is_autonomous_enabled() -> bool:
    """Return True when autonomy is explicitly enabled in .tmp/autonomous_mode.json.

    Defaults to False for safety.
    """
    cfg = read_autonomy_file()
    val = cfg.get('autonomous')
    if isinstance(val, bool):
        return val
    try:
        return str(val).lower() in ('1', 'true', 'yes', 'on')
    except Exception:
        return False


def require_autonomy_or_exit(action: str = 'action') -> None:
    """Exit the process with a message when autonomy is disabled.

    Intended for use at the start of runner entrypoints to avoid
    accidental external effects when autonomy is off.
    """
    if not is_autonomous_enabled():
        print(f'Autonomy disabled in .tmp/autonomous_mode.json — not performing {action}')
        raise SystemExit(0)
