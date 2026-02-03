import os
import json
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from scripts import claims
import gaia.db as gaia_db
from datetime import datetime

ADMIN_TOKEN = os.getenv("MONITOR_ADMIN_TOKEN")

def _read_body(environ):
    try:
        size = int(environ.get('CONTENT_LENGTH', 0) or 0)
    except Exception:
        size = 0
    body = environ['wsgi.input'].read(size) if size else b''
    if not body:
        return {}
    return json.loads(body.decode('utf-8'))

def _check_token(environ):
    if not ADMIN_TOKEN:
        return True, None
    headers = {k[5:].replace('_', '-').lower(): v for k, v in environ.items() if k.startswith('HTTP_')}
    token = headers.get('x-admin-token')
    if not token:
        qs = parse_qs(environ.get('QUERY_STRING', ''))
        token = qs.get('token', [None])[0]
    if token == ADMIN_TOKEN:
        return True, token
    return False, token

def json_resp(start_response, status_code, obj):
    body = json.dumps(obj).encode('utf-8')
    start_response(f"{status_code} OK", [('Content-Type', 'application/json')])
    return [body]

def app(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD')
    authorized, principal = _check_token(environ)

    if path == '/claims/claim' and method == 'POST':
        if not authorized:
            gaia_db.write_trace('claims.claim', status='unauthorized', details={'path': path})
            return json_resp(start_response, 401, {'ok': False, 'error': 'unauthorized'})
        body = _read_body(environ)
        story = body.get('story')
        todolist = body.get('todolist')
        owner = body.get('owner')
        agent_id = body.get('agent_id')
        fingerprint = body.get('fingerprint')
        ttl = body.get('ttl_seconds', 300)
        ok, res = claims.claim(story, todolist, owner, agent_id, fingerprint, ttl_seconds=ttl)
        gaia_db.write_trace('claims.claim', agent_id=agent_id, status='ok' if ok else 'conflict', details={'story': story, 'todolist': todolist, 'result': str(res), 'principal': principal})
        return json_resp(start_response, 200 if ok else 409, {'ok': ok, 'result': res})

    if path == '/claims/release' and method == 'POST':
        if not authorized:
            gaia_db.write_trace('claims.release', status='unauthorized', details={'path': path})
            return json_resp(start_response, 401, {'ok': False, 'error': 'unauthorized'})
        body = _read_body(environ)
        story = body.get('story')
        todolist = body.get('todolist')
        agent_id = body.get('agent_id')
        fingerprint = body.get('fingerprint')
        ok, res = claims.release(story, todolist, agent_id=agent_id, fingerprint=fingerprint)
        gaia_db.write_trace('claims.release', agent_id=agent_id, status='ok' if ok else 'failed', details={'story': story, 'todolist': todolist, 'result': str(res), 'principal': principal})
        return json_resp(start_response, 200 if ok else 400, {'ok': ok, 'result': res})

    if path == '/claims/inspect' and method in ('GET', 'POST'):
        # support GET query params or POST body
        if method == 'GET':
            qs = parse_qs(environ.get('QUERY_STRING', ''))
            story = qs.get('story', [None])[0]
            todolist = qs.get('todolist', [None])[0]
        else:
            body = _read_body(environ)
            story = body.get('story')
            todolist = body.get('todolist')
        info = claims.inspect_claim(story, todolist)
        gaia_db.write_trace('claims.inspect', status='ok', details={'story': story, 'todolist': todolist, 'principal': principal})
        return json_resp(start_response, 200, {'ok': True, 'claim': info})

    return json_resp(start_response, 404, {'ok': False, 'error': 'not_found'})

def serve(host='127.0.0.1', port=8088):
    print(f"Claims server listening on http://{host}:{port}")
    with make_server(host, port, app) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    serve()
