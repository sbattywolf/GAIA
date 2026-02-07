import os


def pytest_sessionstart(session):
    """Ensure CI/test basetemp directories exist so pytest basetemp options don't fail.

    Some CI workflows pass `--basetemp .tmp/pytest` but do not ensure the parent
    `.tmp` directory exists. Creating these paths early avoids FileNotFoundError
    in non-interactive runners.
    """
    try:
        os.makedirs('.tmp/pytest', exist_ok=True)
    except Exception:
        # Best-effort: tests should still run even if the path cannot be created.
        pass
import subprocess
import sys
import socket
import time
import os
import pytest


def _find_free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _wait_port(port, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            s = socket.create_connection(('127.0.0.1', port), timeout=0.5)
            s.close()
            return True
        except Exception:
            time.sleep(0.1)
    return False


@pytest.fixture(scope='session')
def mock_telegram_server():
    """Start `scripts/mock_telegram_server.py` on an ephemeral port for tests.

    Yields the base URL (e.g. 'http://127.0.0.1:12345') to tests.
    """
    port = _find_free_port()
    proc = subprocess.Popen([sys.executable, os.path.join('scripts', 'mock_telegram_server.py'), '--port', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert _wait_port(port, timeout=5.0), 'mock server failed to open port'
        yield f'http://127.0.0.1:{port}'
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
