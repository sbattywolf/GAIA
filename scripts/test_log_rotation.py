"""Test script to exercise `approval_listener.log_debug` rotation.

Run: python scripts/test_log_rotation.py
"""
from scripts import approval_listener as al
import time
import os

# ensure .tmp exists
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logpath = os.path.join(root, '.tmp', 'approval_debug.log')
print('Log path:', logpath)
# set small rotate threshold for test
al.ROTATE_BYTES = 1024
# emit many debug lines
for i in range(300):
    al.log_debug('test_entry', {'i': i})
    if i % 50 == 0:
        print('wrote', i)
    # tiny sleep to avoid tight loop
    time.sleep(0.005)

# show files
for f in sorted(os.listdir(os.path.join(root, '.tmp'))):
    if f.startswith('approval_debug.log'):
        p = os.path.join(root, '.tmp', f)
        print(f, os.path.getsize(p))
print('done')
