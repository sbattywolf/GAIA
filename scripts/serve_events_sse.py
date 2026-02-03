#!/usr/bin/env python3
"""Simple SSE server to stream events.ndjson and serve a tiny UI.

Usage: python scripts/serve_events_sse.py --host 0.0.0.0 --port 8001
Open http://localhost:8001/ in a browser.
"""
import argparse
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import os

ROOT = os.getcwd()
EVENTS = os.path.join(ROOT, 'events.ndjson')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/' or p.endswith('index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(os.path.dirname(__file__), 'monitor_index.html'), 'rb') as f:
                self.wfile.write(f.read())
            return
        if p == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            try:
                # tail the file
                if not os.path.exists(EVENTS):
                    open(EVENTS, 'a').close()
                with open(EVENTS, 'r', encoding='utf-8') as fh:
                    fh.seek(0, os.SEEK_END)
                    while True:
                        line = fh.readline()
                        if not line:
                            time.sleep(0.5)
                            continue
                        data = line.strip()
                        if not data:
                            continue
                        msg = f"data: {data}\n\n"
                        try:
                            self.wfile.write(msg.encode('utf-8'))
                            self.wfile.flush()
                        except BrokenPipeError:
                            break
            except Exception:
                pass
            return
        self.send_response(404)
        self.end_headers()


def run(host, port):
    httpd = HTTPServer((host, port), Handler)
    print(f"Serving monitor on http://{host}:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=8001)
    args = p.parse_args()
    run(args.host, args.port)
