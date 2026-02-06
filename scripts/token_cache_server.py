#!/usr/bin/env python3
"""Small HTTP server to expose cached tokens to local agents.

Usage:
  python scripts/token_cache_server.py --app-id 123 --key-path .private/app.pem --installation-id 456

This starts a server on localhost:8001 by default with a single endpoint:
  GET /token  -> returns JSON {"token": "...", "expires_at": "..."}

Security: server binds to localhost only. Use firewall or SSH tunnels for remote access.
"""
from __future__ import annotations
import argparse
import json
import socketserver
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import sys
from pathlib import Path
import traceback
import os

# Ensure repo root is importable when running the script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gaia.token_cache as tc_mod


class TokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log every incoming request for diagnostics using safe logger
        try:
            safe_log(f"[{datetime.now(timezone.utc).isoformat()}] REQ {self.client_address[0]} {self.requestline}")
        except Exception:
            pass

        # Also print to stdout immediately for interactive debugging
        try:
            print('DEBUG REQ', self.client_address, repr(self.path), self.requestline)
            for k, v in self.headers.items():
                print('DEBUG HDR', k, ':', v)
            sys.stdout.flush()
        except Exception:
            pass

        if self.path == '/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'pong')
            try:
                safe_log(f"[{datetime.now(timezone.utc).isoformat()}] RESP 200 ping")
            except Exception:
                pass
            return

        if self.path.startswith('/token'):
            try:
                # In GAIA_TEST_MODE prefer the environment token to avoid
                # invoking helper subprocesses that may pull heavy deps.
                import os
                print('SERVER ENV GAIA_TEST_MODE=', os.environ.get('GAIA_TEST_MODE'))
                print('SERVER ENV GAIA_GITHUB_TOKEN present=', bool(os.environ.get('GAIA_GITHUB_TOKEN')))
                if os.environ.get('GAIA_TEST_MODE'):
                    tok = os.environ.get('GAIA_GITHUB_TOKEN') or os.environ.get('AUTOMATION_GITHUB_TOKEN')
                    if not tok:
                        raise RuntimeError('GAIA_TEST_MODE set but GAIA_GITHUB_TOKEN not provided')
                    token = tok
                    expires = None
                else:
                    # log before fetching to aid diagnosis
                    safe_log(f"[{datetime.now(timezone.utc).isoformat()}] INFO fetching_via_cache")
                    token = self.server.cache.get()
                    expires = self.server.cache._expires_at
                expires_s = expires.astimezone(timezone.utc).isoformat() if expires else None
                payload = {'token': token, 'expires_at': expires_s}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                body = json.dumps(payload).encode('utf-8')
                self.wfile.write(body)
                try:
                    safe_log(f"[{datetime.now(timezone.utc).isoformat()}] RESP 200 token_ok expires={expires_s}")
                except Exception:
                    pass
            except Exception as e:
                # Log full traceback to rotation/server.log for post-mortem
                try:
                    tb = traceback.format_exc()
                    safe_log(f"[{datetime.now(timezone.utc).isoformat()}] ERROR:")
                    for line in tb.splitlines():
                        safe_log(line)
                except Exception:
                    pass

                # Return traceback in response to help local debugging
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                try:
                    self.wfile.write(traceback.format_exc().encode('utf-8'))
                except Exception:
                    # fallback, minimal message
                    self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Keep output minimal
        return


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8001)
    parser.add_argument('--app-id', required=True)
    parser.add_argument('--key-path', required=True)
    parser.add_argument('--installation-id', required=True)
    args = parser.parse_args()

    # If GAIA_TEST_MODE is set in the environment, pass test_mode=True so the
    # TokenCache will prefer the `GAIA_GITHUB_TOKEN` env var instead of
    # invoking helper subprocesses. This keeps local dev/test flows fast.
    test_mode_flag = bool(os.environ.get('GAIA_TEST_MODE'))
    cache = tc_mod.TokenCache(args.app_id, args.key_path, args.installation_id, test_mode=test_mode_flag)

    server = ThreadedHTTPServer((args.host, args.port), TokenHandler)
    server.cache = cache

    # Write startup log so we can verify server is running before requests
    try:
        log_dir = Path(__file__).resolve().parents[1] / 'rotation'
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / 'server.log', 'a', encoding='utf-8') as lf:
            lf.write(f"[{datetime.now(timezone.utc).isoformat()}] START server http://{args.host}:{args.port}/token\n")
    except Exception:
        pass

    print(f'Serving token cache on http://{args.host}:{args.port}/token')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down')
        server.shutdown()
    except Exception:
        try:
            with open(log_dir / 'server.log', 'a', encoding='utf-8') as lf:
                lf.write(f"[{datetime.now(timezone.utc).isoformat()}] SERVER ERROR in serve_forever\n")
        except Exception:
            pass


if __name__ == '__main__':
    main()
