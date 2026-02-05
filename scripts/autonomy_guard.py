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

# allowlist cache
_ALLOWLIST: Dict[str, object] | None = None


def _allowlist_path() -> Path:
    cfg = ROOT / 'config' / 'agent_mode_allowlist.json'
    return cfg


def load_allowlist() -> Dict[str, object]:
    """Load allowlist from `config/agent_mode_allowlist.json`.

    Returns a dict with keys `allowed_commands` (list) and `allowed_paths` (list).
    Falls back to an empty allowlist when file missing or invalid.
    """
    global _ALLOWLIST
    if _ALLOWLIST is not None:
        return _ALLOWLIST
    p = _allowlist_path()
    if not p.exists():
        _ALLOWLIST = {"allowed_commands": [], "allowed_paths": []}
        return _ALLOWLIST
    try:
        data = json.loads(p.read_text(encoding='utf-8-sig'))
        if not isinstance(data, dict):
            data = {}
    except Exception:
        data = {}
    ac = data.get('allowed_commands') or []
    ap = data.get('allowed_paths') or []
    _ALLOWLIST = {"allowed_commands": [str(x) for x in ac], "allowed_paths": [str(x) for x in ap]}
    return _ALLOWLIST


def is_command_allowed(command: str) -> bool:
    """Return True when `command` is present in the allowlist or allowlist is empty.

    Empty allowlist implies conservative (no-op) behavior: require env `ALLOW_COMMAND_EXECUTION`.
    """
    try:
        al = load_allowlist()
        cmds = al.get('allowed_commands', [])
        if not cmds:
            # no explicit allowlist configured — respect explicit env guard
            return os.environ.get('ALLOW_COMMAND_EXECUTION') == '1'
        return command in cmds
    except Exception:
        return os.environ.get('ALLOW_COMMAND_EXECUTION') == '1'


def is_path_allowed(path: str) -> bool:
    try:
        al = load_allowlist()
        paths = al.get('allowed_paths', [])
        if not paths:
            return False
        p = Path(path).resolve()
        for base in paths:
            try:
                basep = (ROOT / base).resolve()
            except Exception:
                basep = Path(base).resolve()
            try:
                if str(p).startswith(str(basep)):
                    return True
            except Exception:
                continue
        return False
    except Exception:
        return False


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
