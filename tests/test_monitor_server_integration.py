import json
import socket
import threading
import time
from pathlib import Path


def test_monitor_pending_endpoint(tmp_path):
    import urllib.request

    # import the module under test
    import scripts.monitor_server as ms

    # point the server at a temp pending path
    ms.PENDING = tmp_path / '.tmp' / 'pending_commands.json'
    ms.PENDING.parent.mkdir(parents=True, exist_ok=True)

    # pick a free port
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()

    # start server in a daemon thread (serve() blocks)
    thr = threading.Thread(target=lambda: ms.serve('127.0.0.1', port), daemon=True)
    thr.start()
    # give server a moment to start
    time.sleep(0.15)

    # write a pending commands file
    pending = [{'id': 'p1', 'command': 'echo hi', 'from': {'first_name': 'tester'}, 'status': 'pending'}]
    ms.PENDING.write_text(json.dumps(pending), encoding='utf-8')

    url = f'http://127.0.0.1:{port}/pending'
    with urllib.request.urlopen(url, timeout=5) as r:
        assert r.status == 200
        data = json.loads(r.read().decode())
    assert 'pending' in data and isinstance(data['pending'], list)
    assert len(data['pending']) == 1
    assert data['pending'][0]['id'] == 'p1'
