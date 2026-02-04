import subprocess
import sys
import time
import socket


def _wait_port(port, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=0.5)
            s.close()
            return True
        except Exception:
            time.sleep(0.1)
    return False


def test_send_message_against_mock_server():
    """Launch the mock Telegram server and call `send_message` from the real client.

    The test patches the client's `requests` calls by replacing the
    `https://api.telegram.org` hostname with the mock server address so the
    production client code runs unchanged.
    """
    # pick an available ephemeral port to avoid clashes when running full test suite
    import socket as _socket
    s = _socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    proc = subprocess.Popen([sys.executable, "scripts/mock_telegram_server.py", "--port", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert _wait_port(port, timeout=5.0), "mock server did not open port"

        # Import client and reload to avoid test-order monkeypatch interference,
        # then patch its requests to redirect to mock server
        import importlib
        import scripts.telegram_client as tc
        importlib.reload(tc)
        import requests as real_requests

        orig_post = real_requests.post
        orig_get = real_requests.get

        def patched_post(url, *args, **kwargs):
            url2 = url.replace("https://api.telegram.org", f"http://127.0.0.1:{port}")
            return orig_post(url2, *args, **kwargs)

        def patched_get(url, *args, **kwargs):
            url2 = url.replace("https://api.telegram.org", f"http://127.0.0.1:{port}")
            return orig_get(url2, *args, **kwargs)

        # Apply patches to the client's requests module object
        tc.requests.post = patched_post
        tc.requests.get = patched_get

        token = "MOCKTOKEN"
        resp = tc.send_message(token, chat_id=12345, text="integration test hello")

        assert resp.get("ok") is True
        assert resp.get("result", {}).get("text") == "integration test hello"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
