#!/usr/bin/env python3
"""Minimal token server for quick local debugging.

Usage:
  python scripts/simple_token_server.py

Endpoints:
  GET /ping  -> 200 'pong'
  GET /token -> JSON {"token": "...", "expires_at": null}

This server reads `GAIA_TEST_MODE` and `GAIA_GITHUB_TOKEN` from the environment.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Print request info for debugging
            print('REQ', self.client_address, 'PATH', repr(self.path))
            for k, v in self.headers.items():
                print('HDR', k, ':', v)
            self.wfile.flush()

            if self.path == '/ping':
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'pong')
                return

            if self.path == '/token':
                if os.environ.get('GAIA_TEST_MODE'):
                    tok = os.environ.get('GAIA_GITHUB_TOKEN') or os.environ.get('AUTOMATION_GITHUB_TOKEN')
                    if not tok:
                        self.send_response(500)
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'GAIA_TEST_MODE set but GAIA_GITHUB_TOKEN not provided')
                        return
                    payload = {'token': tok, 'expires_at': None}
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(payload).encode('utf-8'))
                    return

                # Not in test mode: respond with minimal error to avoid heavy deps
                self.send_response(501)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Not implemented: real token fetch disabled in simple server')
                return

            self.send_response(404)
            self.end_headers()
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print('HANDLER ERROR', tb)
            try:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(tb.encode('utf-8'))
            except Exception:
                pass


def main():
    host = '127.0.0.1'
    port = 8001
    print(f'Serving simple token server on http://{host}:{port}')
    server = HTTPServer((host, port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down')
        server.shutdown()


if __name__ == '__main__':
    main()
