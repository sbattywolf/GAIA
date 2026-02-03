#!/usr/bin/env python3
"""Automated test: call monitor start/stop endpoints and poll PID status."""
import requests, time, sys
BASE='http://127.0.0.1:5000'

def post_start():
    r = requests.post(BASE + '/api/agents/start', timeout=60)
    print('start:', r.status_code, r.text[:1000])
    return r

def post_stop():
    r = requests.post(BASE + '/api/agents/stop', timeout=30)
    print('stop:', r.status_code, r.text[:1000])
    return r

def poll_status(timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(BASE + '/api/agents/pids_status', timeout=5)
            if r.status_code == 200:
                j = r.json()
                status = j.get('status') or {}
                live = sum(1 for v in status.values() if v.get('alive'))
                print('poll:', live, 'live')
                if live > 0:
                    return j
        except Exception as e:
            print('poll err', e)
        time.sleep(1)
    return None

if __name__ == '__main__':
    print('POST start')
    post_start()
    print('polling for live')
    s = poll_status(20)
    if not s:
        print('No live agents detected')
    else:
        print('Agents live; now stopping...')
        post_stop()
        time.sleep(2)
        final = requests.get(BASE + '/api/agents/pids_status', timeout=5).json()
        print('final:', final)
    sys.exit(0)
