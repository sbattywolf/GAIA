"""
Fetch latest events from the local monitor and append them to events.ndjson
Usage: python scripts/append_events.py [n]
"""
import sys
import urllib.request
import json

n = 50
if len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
    except Exception:
        pass
url = f"http://127.0.0.1:5000/api/events?n={n}"
try:
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
if not data:
    print('No events returned')
    sys.exit(0)

count = 0
with open('events.ndjson', 'a', encoding='utf-8') as f:
    for o in data:
        f.write(json.dumps(o, separators=(',',':')) + '\n')
        count += 1
print('Appended', count, 'events')
