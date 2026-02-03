"""Lightweight monitor HTTP endpoint for GAIA.

Provides:
- GET /pending -> JSON array of pending commands (reads `.tmp/pending_commands.json`).

Designed to be minimal and dependency-free so the UI or a local monitor can query pending items.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import argparse
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from gaia import db as gaia_db

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / '.tmp' / 'pending_commands.json'
STATIC_ROOT = ROOT / 'monitor' / 'templates'


def safe_load_pending():
    try:
        if not PENDING.exists():
            return []
        return json.loads(PENDING.read_text(encoding='utf-8')) or []
    except Exception:
        return []


def load_admin_token():
    # prefer .tmp/telegram.env if present
    envp = ROOT / '.tmp' / 'telegram.env'
    token = os.environ.get('MONITOR_ADMIN_TOKEN')
    try:
        if envp.exists():
            for line in envp.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                k, v = line.split('=', 1)
                if k.strip() == 'MONITOR_ADMIN_TOKEN':
                    token = v.strip()
    except Exception:
        pass
    return token


class MonitorHandler(BaseHTTPRequestHandler):
    def _set_json_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _set_html_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Admin-Token')
        self.end_headers()

    def do_GET(self):
        # Serve pending JSON at /pending
        if self.path.startswith('/pending'):
            data = safe_load_pending()
            self._set_json_headers(200)
            try:
                self.wfile.write(json.dumps({'pending': data}, default=str).encode('utf-8'))
            except Exception:
                self.wfile.write(b'{"pending": []}')
            return

        # Serve static UI index
        if self.path == '/' or self.path == '/index.html':
            idx = STATIC_ROOT / 'index.html'
            if idx.exists():
                try:
                    content = idx.read_text(encoding='utf-8')
                    self._set_html_headers(200)
                    self.wfile.write(content.encode('utf-8'))
                    return
                except Exception:
                    pass
            self.send_response(500)
            self.end_headers()
            return

        # Serve static files under /static/ if present in templates
        if self.path.startswith('/static/'):
            rel = self.path.lstrip('/')
            target = STATIC_ROOT / rel.replace('static/', '')
            if target.exists() and target.is_file():
                try:
                    content = target.read_bytes()
                    # basic content type guessing
                    ct = 'application/octet-stream'
                    if str(target).endswith('.js'):
                        ct = 'application/javascript'
                    elif str(target).endswith('.css'):
                        ct = 'text/css'
                    elif str(target).endswith('.svg'):
                        ct = 'image/svg+xml'
                    self.send_response(200)
                    self.send_header('Content-Type', ct)
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception:
                    pass
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

    def _check_token(self):
        # Accept token via header 'X-Admin-Token' or query param 'token'
        token = load_admin_token()
        if not token:
            return None
        hdr = self.headers.get('X-Admin-Token')
        if hdr and hdr.strip() == token:
            return hdr.strip()
        # check query param
        qs = urlparse(self.path).query
        params = parse_qs(qs)
        if 'token' in params and params['token'] and params['token'][0] == token:
            return params['token'][0]
        return None

    def do_POST(self):
        # admin requeue endpoint
        if self.path.startswith('/admin/requeue'):
            tok = self._check_token()
            if not tok:
                try:
                    gaia_db.write_trace(action='telegram.requeue.admin', agent_id='monitor', status='unauthorized', details={'source': 'admin_ui', 'remote': self.client_address[0]})
                except Exception:
                    pass
                self._set_json_headers(401)
                self.wfile.write(json.dumps({'error': 'unauthorized'}).encode('utf-8'))
                return

            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length) if length else b''
            try:
                payload = json.loads(body.decode('utf-8') or '{}')
            except Exception:
                payload = {}
            # accept index or id
            idx = payload.get('index')
            cbid = payload.get('callback_id') or payload.get('id')
            from scripts import telegram_queue as tq
            if idx is not None:
                try:
                    idx = int(idx)
                except Exception:
                    self._set_json_headers(400)
                    self.wfile.write(json.dumps({'error': 'invalid index'}).encode('utf-8'))
                    return
                # load failed list and pop
                FAILED = ROOT / '.tmp' / 'telegram_queue_failed.json'
                try:
                    items = json.loads(FAILED.read_text(encoding='utf-8') or '[]') if FAILED.exists() else []
                except Exception:
                    items = []
                if idx < 0 or idx >= len(items):
                    self._set_json_headers(400)
                    self.wfile.write(json.dumps({'error': 'index out of range'}).encode('utf-8'))
                    return
                item = items.pop(idx)
                ok = tq.requeue(item, front=False)
                if ok:
                    try:
                        FAILED.write_text(json.dumps(items, indent=2), encoding='utf-8')
                    except Exception:
                        pass
                    try:
                        # audit admin requeue in gaia.db, include principal fingerprint
                        principal = (tok[:6] + '...') if tok else None
                        gaia_db.write_trace(action='telegram.requeue.admin', agent_id='monitor', status='ok', details={'source': 'admin_ui', 'index': idx, 'id': item.get('callback_query_id') or (item.get('update') or {}).get('update_id'), 'principal': principal, 'remote': self.client_address[0]})
                    except Exception:
                        pass
                    self._set_json_headers(200)
                    self.wfile.write(json.dumps({'requeued': True}).encode('utf-8'))
                    return
                else:
                    self._set_json_headers(500)
                    self.wfile.write(json.dumps({'error': 'requeue_failed'}).encode('utf-8'))
                    return
            if cbid:
                # find by callback id
                FAILED = ROOT / '.tmp' / 'telegram_queue_failed.json'
                try:
                    items = json.loads(FAILED.read_text(encoding='utf-8') or '[]') if FAILED.exists() else []
                except Exception:
                    items = []
                found = None
                for i, it in enumerate(items):
                    if (it.get('callback_query_id') == cbid) or ((it.get('update') or {}).get('update_id') == cbid):
                        found = i
                        break
                if found is None:
                    self._set_json_headers(404)
                    self.wfile.write(json.dumps({'error': 'not_found'}).encode('utf-8'))
                    return
                item = items.pop(found)
                ok = tq.requeue(item, front=False)
                if ok:
                    try:
                        FAILED.write_text(json.dumps(items, indent=2), encoding='utf-8')
                    except Exception:
                        pass
                    try:
                        principal = (tok[:6] + '...') if tok else None
                        gaia_db.write_trace(action='telegram.requeue.admin', agent_id='monitor', status='ok', details={'source': 'admin_ui', 'index': found, 'id': item.get('callback_query_id') or (item.get('update') or {}).get('update_id'), 'principal': principal, 'remote': self.client_address[0]})
                    except Exception:
                        pass
                    self._set_json_headers(200)
                    self.wfile.write(json.dumps({'requeued': True}).encode('utf-8'))
                    return
                self._set_json_headers(500)
                self.wfile.write(json.dumps({'error': 'requeue_failed'}).encode('utf-8'))
                return

        self._set_json_headers(404)
        self.wfile.write(json.dumps({'error': 'not_found'}).encode('utf-8'))


def serve(host: str = '127.0.0.1', port: int = 8080):
    addr = (host, port)
    httpd = HTTPServer(addr, MonitorHandler)
    print(f'Serving GAIA monitor on http://{host}:{port} (CTRL+C to stop)')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--host', default=os.environ.get('GAIA_MONITOR_HOST', '127.0.0.1'))
    p.add_argument('--port', type=int, default=int(os.environ.get('GAIA_MONITOR_PORT', '8080')))
    args = p.parse_args()
    serve(args.host, args.port)


if __name__ == '__main__':
    main()
