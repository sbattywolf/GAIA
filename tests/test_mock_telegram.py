import threading
import time
import json
import urllib.request
import tempfile
from http.server import HTTPServer

from agents.mock_telegram import MockTelegramHandler


def start_server_in_thread(tmpfile_path):
    MockTelegramHandler.output_path = tmpfile_path
    server = HTTPServer(('127.0.0.1', 0), MockTelegramHandler)
    port = server.server_address[1]

    def _serve():
        try:
            server.serve_forever()
        except Exception:
            pass

    t = threading.Thread(target=_serve, daemon=True)
    t.start()
    return server, port, t


def test_send_message_and_record(tmp_path):
    out = tmp_path / 'events.ndjson'
    server, port, t = start_server_in_thread(str(out))
    time.sleep(0.1)

    url = f'http://127.0.0.1:{port}/sendMessage'
    payload = json.dumps({'chat_id': 1234, 'text': 'hello'}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST', headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read().decode('utf-8')
        assert resp.status == 200

    # allow handler to flush
    time.sleep(0.05)
    server.shutdown()

    data = out.read_text(encoding='utf-8').strip().splitlines()
    assert len(data) == 1
    obj = json.loads(data[0])
    assert obj['type'] == 'telegram.mock.message'
    assert obj['payload']['chat_id'] == 1234
    assert obj['payload']['text'] == 'hello'
