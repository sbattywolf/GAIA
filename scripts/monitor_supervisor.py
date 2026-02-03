#!/usr/bin/env python3
"""Supervisor for monitor/app.py

Starts monitor/app.py as a child process, writes the child's PID to
.tmp/monitor_pid.txt, redirects stdout/stderr to .tmp/monitor.log and
.tmp/monitor.err, and restarts the child if it exits.
"""
import subprocess
import sys
import time
import os
from datetime import datetime
import urllib.request
import urllib.error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TMP_DIR = os.path.join(ROOT, '.tmp')
os.makedirs(TMP_DIR, exist_ok=True)
LOG_PATH = os.path.join(TMP_DIR, 'monitor.log')
ERR_PATH = os.path.join(TMP_DIR, 'monitor.err')
PID_PATH = os.path.join(TMP_DIR, 'monitor_pid.txt')

def write_pid(pid: int):
    try:
        with open(PID_PATH, 'w') as f:
            f.write(str(pid))
    except Exception:
        pass

def remove_pid():
    try:
        if os.path.exists(PID_PATH):
            os.remove(PID_PATH)
    except Exception:
        pass

def start_child(host='127.0.0.1', port=5000):
    python = sys.executable
    cmd = [python, '-u', os.path.join(ROOT, 'monitor', 'app.py'), '--host', host, '--port', str(port)]
    logf = open(LOG_PATH, 'ab')
    errf = open(ERR_PATH, 'ab')
    proc = subprocess.Popen(cmd, stdout=logf, stderr=errf)
    write_pid(proc.pid)
    return proc, logf, errf

def supervisor_loop(host='127.0.0.1', port=5000, restart_delay=1):
    print(f'[{datetime.utcnow().isoformat()}Z] Supervisor starting monitor on {host}:{port}')
    try:
        while True:
            proc, logf, errf = start_child(host, port)
            print(f'[{datetime.utcnow().isoformat()}Z] Started child pid={proc.pid}')
            # wait for child to become healthy (poll monitor health endpoint)
            check_url = f'http://{host}:{port}/api/agents/status'
            healthy = False
            start_time = time.time()
            health_timeout = 10
            while time.time() - start_time < health_timeout:
                # if the process exited prematurely, break and restart
                if proc.poll() is not None:
                    break
                try:
                    with urllib.request.urlopen(check_url, timeout=2) as r:
                        if r.getcode() == 200:
                            healthy = True
                            break
                except Exception:
                    # still starting
                    pass
                time.sleep(0.5)

            if not healthy:
                print(f'[{datetime.utcnow().isoformat()}Z] Child pid={proc.pid} failed healthcheck; killing and restarting')
                try:
                    proc.kill()
                except Exception:
                    pass
                try:
                    logf.close()
                except Exception:
                    pass
                try:
                    errf.close()
                except Exception:
                    pass
                time.sleep(restart_delay)
                continue

            # child is healthy — wait for it to exit or be interrupted
            rc = None
            try:
                rc = proc.wait()
            except KeyboardInterrupt:
                try:
                    proc.terminate()
                except Exception:
                    pass
                break
            finally:
                try:
                    logf.close()
                except Exception:
                    pass
                try:
                    errf.close()
                except Exception:
                    pass

            print(f'[{datetime.utcnow().isoformat()}Z] Child pid={proc.pid} exited rc={rc}; restarting in {restart_delay}s')
            time.sleep(restart_delay)
    finally:
        remove_pid()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    try:
        supervisor_loop(host=args.host, port=args.port)
    except Exception as e:
        print('Supervisor error:', e, file=sys.stderr)
        remove_pid()

if __name__ == '__main__':
    main()
