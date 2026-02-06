"""Environment helpers for canonical token names and fallbacks.

Provide a single place to prefer `GAIA_GITHUB_TOKEN` while falling back to
legacy `AUTOMATION_GITHUB_TOKEN` for backward compatibility.
"""
from __future__ import annotations
import os
from typing import Optional


def get_github_token() -> Optional[str]:
    """Return the preferred GitHub token from env or None.

    Preference order:
    1. `GAIA_GITHUB_TOKEN`
    2. `AUTOMATION_GITHUB_TOKEN`
    3. `GITHUB_TOKEN` / `GH_TOKEN`
    """
    for name in ('GAIA_GITHUB_TOKEN', 'AUTOMATION_GITHUB_TOKEN', 'GITHUB_TOKEN', 'GH_TOKEN'):
        val = os.environ.get(name)
        if val:
            return val
    return None


def token_env_names() -> tuple[str, ...]:
    """Return env var names checked by `get_github_token()` (for diagnostics)."""
    return ('GAIA_GITHUB_TOKEN', 'AUTOMATION_GITHUB_TOKEN', 'GITHUB_TOKEN', 'GH_TOKEN')
