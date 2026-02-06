import urllib.request
import sys

url = 'http://127.0.0.1:8001/token'
try:
    with urllib.request.urlopen(url, timeout=10) as r:
        print(r.read().decode('utf-8'))
except Exception as e:
    # try to print response body if available
    fp = getattr(e, 'fp', None)
    if fp:
        try:
            print(fp.read().decode('utf-8'))
        except Exception:
            print('ERROR:', e)
    else:
        print('ERROR:', e)
    sys.exit(1)
