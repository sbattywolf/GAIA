"""Minimal resource monitor stub using psutil (optional).
If `psutil` is unavailable, the module prints guidance.
"""
import time
import shutil

try:
    import psutil
except Exception:
    psutil = None


def status():
    if not psutil:
        print('psutil not installed; install with: pip install psutil')
        return 2
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    print(f'CPU: {cpu}%, Mem: {mem.percent}% ({mem.used/1024**2:.1f} MiB of {mem.total/1024**2:.1f} MiB)')
    return 0


def watch(interval=5):
    if not psutil:
        print('psutil not installed; install with: pip install psutil')
        return 2
    try:
        while True:
            status()
            time.sleep(interval)
    except KeyboardInterrupt:
        print('watch stopped')
        return 0


def handle(action: str):
    if action == 'status':
        return status()
    if action == 'watch':
        return watch()
    print('unknown resource action')
    return 1
