import time
import urllib.request
import threading
import os
from scripts.mock_token_service import run_server


def http_get(url, token=None):
    req = urllib.request.Request(url)
    if token:
        req.add_header('Authorization', f'token {token}')
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()


def main():
    # Ensure token exists
    token = None
    p = os.path.join('.tmp', 'generated_token.txt')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            token = f.read().strip()
    else:
        token = 'local-test-token-123'
        # write so the service can pick it up if needed
        os.makedirs('.tmp', exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(token)

    ready = threading.Event()
    srv = run_server(token=token, port=8001, ready_event=ready)
    ready.wait(timeout=2)

    url = 'http://127.0.0.1:8001/verify'
    print('Testing correct token...')
    status, body = http_get(url, token=token)
    print('Status:', status, 'Body:', body)

    print('Testing wrong token...')
    status2, body2 = http_get(url, token='wrong-token')
    print('Status:', status2, 'Body:', body2)

    srv.shutdown()


if __name__ == '__main__':
    main()
