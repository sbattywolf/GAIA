"""Minimal mock Telegram HTTP API for local testing.

Usage:
  python -m agents.mock_telegram --port 8088 --out mock_telegram_events.ndjson

This server uses only the Python standard library so it can run in CI without
extra packages. It accepts POST /sendMessage with JSON {"chat_id":..., "text":...}
and appends NDJSON lines to the configured output file with fields: type, ts, payload.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import json
from datetime import datetime, timezone
from urllib.parse import urlparse
import os


class MockTelegramHandler(BaseHTTPRequestHandler):
    output_path = None

    def _read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except Exception:
            return None

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/sendMessage':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
            return

        payload = self._read_json() or {}
        event = {
            'type': 'telegram.mock.message',
            'ts': datetime.now(timezone.utc).isoformat(),
            'payload': payload,
        }
        try:
            os.makedirs(os.path.dirname(self.output_path) or '.', exist_ok=True)
            with open(self.output_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def log_message(self, format, *args):
        # quiet logging to stderr (keep minimal)
        return


def run(port: int, out: str, host: str = '127.0.0.1'):
    MockTelegramHandler.output_path = out
    server = HTTPServer((host, port), MockTelegramHandler)
    print(f"Mock Telegram server listening on http://{host}:{port} -> {out}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8088)
    parser.add_argument('--out', default='mock_telegram_events.ndjson')
    parser.add_argument('--host', default='127.0.0.1')
    args = parser.parse_args()
    run(args.port, args.out, args.host)


if __name__ == '__main__':
    main()
