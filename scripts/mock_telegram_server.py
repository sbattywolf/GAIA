#!/usr/bin/env python3
"""Simple mock Telegram Bot HTTP API server for local integration tests.

Usage:
  python scripts/mock_telegram_server.py --port 8081

Accepts POST requests to paths like /bot<token>/<method> and returns
JSON responses that mimic Telegram Bot API (getMe, sendMessage, etc.).
This server has no external deps and is suitable for CI/local runs.
"""
from http.server import BaseHTTPRequestHandler
import socketserver
import argparse
import json
import urllib.parse
import sys


class MockTelegramHandler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2 or not parts[0].startswith("bot"):
            self._send_json({"ok": False, "description": "invalid path"}, code=404)
            return

        token = parts[0][3:]
        method = parts[1]

        length_hdr = self.headers.get("Content-Length")
        te = self.headers.get("Transfer-Encoding", "").lower()
        body = b""
        if length_hdr:
            try:
                length = int(length_hdr)
                body = self.rfile.read(length) if length else b""
            except Exception:
                body = b""
        elif te == 'chunked':
            # read chunked transfer encoding
            chunks = []
            while True:
                line = self.rfile.readline()
                if not line:
                    break
                try:
                    size = int(line.strip().split(b';')[0], 16)
                except Exception:
                    break
                if size == 0:
                    # consume trailer and final CRLF
                    _ = self.rfile.readline()
                    break
                data = self.rfile.read(size)
                chunks.append(data)
                # consume CRLF after chunk
                _ = self.rfile.read(2)
            body = b"".join(chunks)
        else:
            # fallback: attempt to read available data (may be empty)
            try:
                self.connection.settimeout(0.01)
                body = self.rfile.read()
            except Exception:
                body = b""
        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        # Simple deterministic responses for common methods
        if method == "getMe":
            resp = {
                "ok": True,
                "result": {"id": 123456789, "is_bot": True, "first_name": "MockBot", "username": "mock_bot"},
            }
        elif method == "sendMessage":
            chat_id = payload.get("chat_id") or payload.get("chatId") or payload.get("chat", {}).get("id")
            text = payload.get("text", "")
            resp = {
                "ok": True,
                "result": {"message_id": 1, "chat": {"id": chat_id}, "text": text},
            }
        else:
            resp = {"ok": True, "result": {}}

        self._send_json(resp)

    def log_message(self, format, *args):
        # keep output minimal but visible
        sys.stdout.write("[mock_telegram] " + (format % args) + "\n")


def run_server(port):
    with socketserver.ThreadingTCPServer(("", port), MockTelegramHandler) as httpd:
        print(f"Mock Telegram server listening on http://127.0.0.1:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down mock telegram server")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", "-p", type=int, default=8081, help="Port to listen on")
    args = p.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
