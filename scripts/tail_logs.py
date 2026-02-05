import os
import time
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, '.tmp')
WATCH_GLOB = os.path.join(TMP, '*.out')
POLL_INTERVAL = float(os.environ.get('TAIL_POLL_SECONDS', '0.5'))


def open_files():
    files = {}
    for path in glob.glob(WATCH_GLOB):
        try:
            f = open(path, 'rb')
            f.seek(0, os.SEEK_END)
            files[path] = {'f': f, 'pos': f.tell()}
        except Exception:
            continue
    return files


def scan_new_files(current):
    paths = set(glob.glob(WATCH_GLOB))
    added = paths - set(current.keys())
    removed = set(current.keys()) - paths
    for p in added:
        try:
            f = open(p, 'rb')
            f.seek(0, os.SEEK_END)
            current[p] = {'f': f, 'pos': f.tell()}
            print(f"[tail] watching new file: {os.path.basename(p)}")
        except Exception:
            pass
    for p in removed:
        try:
            current[p]['f'].close()
        except Exception:
            pass
        del current[p]
        print(f"[tail] stopped watching removed file: {os.path.basename(p)}")


def tail_loop():
    files = open_files()
    print('[tail] starting tail of .tmp/*.out; Ctrl-C to stop')
    try:
        while True:
            scan_new_files(files)
            for path, meta in list(files.items()):
                f = meta['f']
                f.seek(meta['pos'])
                data = f.read()
                if data:
                    try:
                        text = data.decode('utf-8', errors='replace')
                    except Exception:
                        text = str(data)
                    for line in text.splitlines():
                        print(f"[{os.path.basename(path)}] {line}")
                    meta['pos'] = f.tell()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print('\n[tail] stopped by user')
    finally:
        for meta in files.values():
            try:
                meta['f'].close()
            except Exception:
                pass


if __name__ == '__main__':
    tail_loop()
