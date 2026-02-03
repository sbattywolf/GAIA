import json
import urllib.request

urls = [
    'http://127.0.0.1:5000/api/events?n=5',
    'http://127.0.0.1:5000/api/agents/status',
    'http://127.0.0.1:5000/api/agents/capabilities',
    'http://127.0.0.1:5000/api/agents/out_status'
]

for u in urls:
    print('\n==> ', u)
    try:
        with urllib.request.urlopen(u, timeout=5) as r:
            b = r.read().decode('utf-8')
            try:
                j = json.loads(b)
                print(json.dumps(j, indent=2))
            except Exception:
                print(b)
    except Exception as e:
        print('ERROR:', e)
