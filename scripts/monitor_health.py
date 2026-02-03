#!/usr/bin/env python3
"""
Simple monitor health check.
Exit 0 if monitor responds (200) to `/api/agents/status` or `/`, else exit 2.
"""
import sys
import urllib.request
import json

urls = [
    'http://127.0.0.1:5000/api/agents/status',
    'http://127.0.0.1:5000/'
]

for u in urls:
    try:
        with urllib.request.urlopen(u, timeout=5) as r:
            code = r.getcode()
            body = r.read()
            if code == 200:
                # try parse JSON for diagnostics
                try:
                    j = json.loads(body)
                    print('OK', u, json.dumps(j))
                except Exception:
                    print('OK', u, f'status={code}')
                sys.exit(0)
            else:
                print('ERROR', u, 'status', code)
    except Exception as e:
        print('ERR', u, e)

print('Monitor not healthy')
sys.exit(2)
