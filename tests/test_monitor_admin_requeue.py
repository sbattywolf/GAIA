import json
import threading
import time
from http.server import HTTPServer

import requests
import pytest

import scripts.monitor_server as ms
import gaia.db as gdb


def _start_server():
    httpd = HTTPServer(('127.0.0.1', 0), ms.MonitorHandler)
    port = httpd.server_port
    th = threading.Thread(target=httpd.serve_forever, daemon=True)
    th.start()
    return httpd, port, th


def _write_failed_item(item):
    FAILED = ms.ROOT / '.tmp' / 'telegram_queue_failed.json'
    FAILED.parent.mkdir(parents=True, exist_ok=True)
    FAILED.write_text(json.dumps([item]), encoding='utf-8')


def test_admin_requeue_unauthorized(monkeypatch):
    # Ensure no token in environment
    monkeypatch.delenv('MONITOR_ADMIN_TOKEN', raising=False)

    _write_failed_item({'callback_query_id': 'cb-unauth'})

    httpd, port, th = _start_server()
    try:
        res = requests.post(f'http://127.0.0.1:{port}/admin/requeue', json={'index': 0}, timeout=5)
        assert res.status_code == 401
        assert res.json().get('error') == 'unauthorized'
        # audit trace for unauthorized attempt should be recorded
        traces = gdb.tail_traces(20)
        assert any(t.get('action') == 'telegram.requeue.admin' and t.get('status') == 'unauthorized' for t in traces)
    finally:
        httpd.shutdown()
        th.join(timeout=1)


def test_admin_requeue_authorized(monkeypatch):
    monkeypatch.setenv('MONITOR_ADMIN_TOKEN', 's3cr3t')

    item = {'callback_query_id': 'cb-auth'}
    _write_failed_item(item)

    # patch the requeue implementation to avoid side-effects; ensure it returns True
    def fake_requeue(it, front=False):
        return True

    monkeypatch.setattr('scripts.telegram_queue.requeue', fake_requeue)

    httpd, port, th = _start_server()
    try:
        headers = {'X-Admin-Token': 's3cr3t'}
        res = requests.post(f'http://127.0.0.1:{port}/admin/requeue', json={'index': 0}, headers=headers, timeout=5)
        assert res.status_code == 200
        assert res.json().get('requeued') is True

        # ensure an audit trace was written
        traces = gdb.tail_traces(20)
        found = None
        for t in traces:
            if t.get('action') == 'telegram.requeue.admin' and t.get('status') == 'ok':
                try:
                    det = json.loads(t.get('details') or '{}')
                except Exception:
                    det = {}
                if det.get('id') == item.get('callback_query_id'):
                    found = det
                    break
        assert found is not None, 'Expected audit trace for authorized requeue'
        assert 'principal' in found and found['principal'].endswith('...')
    finally:
        httpd.shutdown()
        th.join(timeout=1)
