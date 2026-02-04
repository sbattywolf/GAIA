from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import os


class TokenHandler(BaseHTTPRequestHandler):
    expected_token = None

    def do_GET(self):
        # Health endpoint
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
            return

        if self.path != '/verify':
            self.send_response(404)
            self.end_headers()
            return

        auth = self.headers.get('Authorization','')
        # Accept 'token <t>' or 'Bearer <t>'
        parts = auth.split()
        token = parts[1] if len(parts) == 2 else ''

        if token and token == self.expected_token:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')

    def log_message(self, format, *args):
        # minimal logging
        return


def run_server(token=None, host='127.0.0.1', port=8000, ready_event: threading.Event = None):
    if token is None:
        token = os.environ.get('MOCK_TOKEN')
        # fallback to file
        try:
            with open(os.path.join(os.getcwd(), '.tmp', 'generated_token.txt'), 'r', encoding='utf-8') as f:
                token = f.read().strip() if not token else token
        except Exception:
            pass

    if not token:
        raise RuntimeError('No token provided (env MOCK_TOKEN or .tmp/generated_token.txt)')

    TokenHandler.expected_token = token
    srv = ThreadingHTTPServer((host, port), TokenHandler)

    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    if ready_event:
        ready_event.set()
    return srv


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--token')
    args = parser.parse_args()
    if args.token:
        os.environ['MOCK_TOKEN'] = args.token

    print('Starting mock token service on %s:%d' % (args.host, args.port))
    srv = run_server(host=args.host, port=args.port)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
