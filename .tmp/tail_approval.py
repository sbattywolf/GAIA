import time, sys, os
path = os.path.join('.', '.tmp', 'logs', 'approval_listener.out.log')
os.makedirs(os.path.dirname(path), exist_ok=True)
open(path, 'a').close()
with open(path, 'r', encoding='utf-8') as f:
    f.seek(0, 2)
    start = time.time()
    print('--- start tail (300s) ---')
    sys.stdout.flush()
    while time.time() - start < 300:
        line = f.readline()
        if line:
            print(line.rstrip())
            sys.stdout.flush()
        else:
            time.sleep(0.25)
    print('--- end tail ---')
