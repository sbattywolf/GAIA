#!/usr/bin/env python3
"""Simple integration test: Start -> Probe -> Compare -> Restart -> Stop
Usage: python scripts/test_integration.py [agent-id]
"""
import requests, time, json, os, sys

BASE = os.environ.get('GAIA_MONITOR_URL', 'http://127.0.0.1:5000')

def load_first_agent():
    path = os.path.join(os.getcwd(), 'agents.json')
    if not os.path.exists(path):
        print('agents.json not found', path); return None
    data = json.load(open(path, 'r', encoding='utf-8'))
    if isinstance(data, dict):
        return next(iter(data.keys()))
    if isinstance(data, list) and data:
        a = data[0]
        return a.get('id') or a.get('name')
    return None

def post(path, payload=None):
    url = BASE.rstrip('/') + path
    try:
        r = requests.post(url, json=payload or {}, timeout=15)
        return r
    except Exception as e:
        print('POST error', url, e); return None

def get(path, params=None):
    url = BASE.rstrip('/') + path
    try:
        r = requests.get(url, params=params or {}, timeout=15)
        return r
    except Exception as e:
        print('GET error', url, e); return None

def main():
    aid = None
    if len(sys.argv) > 1:
        aid = sys.argv[1]
    else:
        aid = load_first_agent()
    if not aid:
        print('No agent id determined. Provide as first arg or ensure agents.json present.'); sys.exit(2)
    print('Using agent id:', aid)

    print('\n1) START')
    r = post('/api/agents/start', {'id': aid})
    print('start status:', getattr(r, 'status_code', None), getattr(r, 'text', None))
    time.sleep(2)

    print('\n2) PROBE')
    r = get('/api/agents/probe', {'id': aid})
    print('probe status:', getattr(r, 'status_code', None), getattr(r, 'text', None))

    print('\n3) COMPARE')
    r = get('/api/agents/compare', {'id': aid})
    print('compare status:', getattr(r, 'status_code', None))
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print('compare raw:', getattr(r, 'text', None))

    print('\n4) RESTART (stop -> start)')
    rs = post('/api/agents/stop', {'id': aid})
    print('stop status:', getattr(rs, 'status_code', None))
    time.sleep(1)
    rs = post('/api/agents/start', {'id': aid})
    print('start2 status:', getattr(rs, 'status_code', None))
    time.sleep(2)

    print('\n5) FINAL STOP')
    rf = post('/api/agents/stop', {'id': aid})
    print('final stop status:', getattr(rf, 'status_code', None), getattr(rf, 'text', None))

    print('\nIntegration test finished.')

if __name__ == '__main__':
    main()
