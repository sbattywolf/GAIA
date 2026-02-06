"""Central token cache for GitHub App installation tokens.

Provides a lightweight in-process cache that fetches installation tokens
via `scripts/github_app_token.py` and caches them until expiry. Designed to
be used by the controller to serve tokens to local agents via a small HTTP
endpoint (see `scripts/token_cache_server.py`).

This module keeps dependencies minimal by invoking the helper script
as a subprocess and reading JSON output.
"""
from __future__ import annotations
import json
import subprocess
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
import os
import json
from datetime import datetime, timezone
try:
    from orchestrator import write_audit
except Exception:
    # fallback if orchestrator not importable via module path
    from ..orchestrator import write_audit  # type: ignore


class TokenFetchError(RuntimeError):
    pass


class TokenCache:
    def __init__(self, app_id: str, key_path: str, installation_id: str, helper_python: str = 'python', test_mode: bool = False):
        self.app_id = app_id
        self.key_path = str(Path(key_path))
        self.installation_id = installation_id
        self.helper_python = helper_python
        # test_mode when True will use GAIA_GITHUB_TOKEN env var instead of
        # invoking the helper subprocess. Default is False to preserve test
        # expectations where tests instantiate TokenCache and expect the
        # helper to be called (they patch subprocess.run).
        self.test_mode = bool(test_mode)

        self._lock = threading.Lock()
        self._token: Optional[str] = None
        self._expires_at: Optional[datetime] = None

    def _fetch_via_helper(self) -> None:
        # Test-mode: avoid invoking helper and SecretsManager (which may need
        # heavy deps). Prefer env var `GAIA_TEST_MODE` -> use `GAIA_GITHUB_TOKEN`.
        # Only use the environment token when explicitly constructed in
        # test mode; this avoids respecting a globally exported GAIA_TEST_MODE
        # in consumer environments (such as developer shells) which would
        # interfere with unit tests that patch subprocess.run.
        if self.test_mode:
            tok = os.environ.get('GAIA_GITHUB_TOKEN') or os.environ.get('AUTOMATION_GITHUB_TOKEN')
            if not tok:
                raise TokenFetchError('GAIA_TEST_MODE enabled for TokenCache but no GAIA_GITHUB_TOKEN found in env')
            token = tok
            expires_at = None
        else:
            cmd = [self.helper_python, 'scripts/github_app_token.py',
                   '--app-id', str(self.app_id), '--key-path', self.key_path,
                   '--installation-id', str(self.installation_id)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                raise TokenFetchError(proc.stderr or proc.stdout or 'unknown error')
            try:
                data = json.loads(proc.stdout)
                token = data.get('token')
                expires_at = data.get('expires_at')
            except Exception:
                # fallback: sometimes helper prints plain token
                token = proc.stdout.strip()
                expires_at = None

        if not token:
            raise TokenFetchError('no token in helper output')

        self._token = token
        if expires_at:
            # parse ISO 8601
            self._expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        else:
            # default to 50 minutes from now
            self._expires_at = datetime.now(timezone.utc) + timedelta(minutes=50)

        # Audit: write to DB and append to events.ndjson
        try:
            details = json.dumps({'action': 'token_fetch', 'installation_id': self.installation_id, 'expires_at': self._expires_at.isoformat()})
            write_audit('token-cache', 'fetch', details)
        except Exception:
            pass
        try:
            # append to events.ndjson in repo root if possible
            root = os.getcwd()
            ev = {'type': 'token.fetch', 'source': 'token-cache', 'installation_id': self.installation_id, 'expires_at': self._expires_at.isoformat(), 'timestamp': datetime.now(timezone.utc).isoformat() + 'Z'}
            with open(os.path.join(root, 'events.ndjson'), 'a', encoding='utf-8') as f:
                f.write(json.dumps(ev, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def get(self) -> str:
        with self._lock:
            now = datetime.now(timezone.utc)
            if self._token and self._expires_at and now < (self._expires_at - timedelta(minutes=5)):
                return self._token

            # fetch new token
            self._fetch_via_helper()
            return self._token

    def force_refresh(self) -> str:
        with self._lock:
            self._fetch_via_helper()
            return self._token
