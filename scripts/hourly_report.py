import os
import time
import json
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, '.tmp')
EVENTS = os.path.join(ROOT, 'events.ndjson')
RUN_META = os.path.join(TMP, 'run_20h.json')
LAST_MESSAGES = os.path.join(TMP, 'last_messages.log')

INTERVAL = int(os.environ.get('HOURLY_REPORT_INTERVAL_SECONDS', '3600'))  # default 1 hour
SEND_TELEGRAM = os.environ.get('HOURLY_REPORT_TELEGRAM', '0').lower() in ('1', 'true', 'yes')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.environ.get('TELEGRAM_CHAT_ID') or os.environ.get('TELEGRAM_CHAT')


def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def load_run_id():
    try:
        with open(RUN_META, 'r', encoding='utf-8') as f:
            return json.load(f).get('run_id')
    except Exception:
        return 'run_unknown'


def read_last_messages(n=10):
    try:
        with open(LAST_MESSAGES, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return lines[-n:]
    except Exception:
        return []


def read_pid_files():
    pids = {}
    for p in glob.glob(os.path.join(TMP, '*_pid.txt')):
        name = os.path.basename(p).replace('_pid.txt', '')
        try:
            with open(p, 'r', encoding='utf-8') as f:
                pid = f.read().strip()
        except Exception:
            pid = ''
        pids[name] = pid
    return pids


def tail_service_logs(lines=5):
    logs = {}
    for name in ('monitor_framework', 'resource_monitor', 'automation_runner', 'approval_listener'):
        path = os.path.join(TMP, f'{name}.out')
        try:
            with open(path, 'rb') as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                to_read = 8192
                f.seek(max(0, size - to_read))
                data = f.read().decode('utf-8', errors='replace')
                logs[name] = data.strip().splitlines()[-lines:]
        except Exception:
            logs[name] = []
    return logs


def append_event(evt: dict):
    try:
        with open(EVENTS, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, ensure_ascii=False) + '\n')
    except Exception:
        pass


def send_telegram(text: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
        return False
    try:
        import requests
    except Exception:
        return False
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': TELEGRAM_CHAT, 'text': text})
        return r.status_code == 200
    except Exception:
        return False


def build_report():
    run_id = load_run_id()
    pids = read_pid_files()
    msgs = read_last_messages(10)
    logs = tail_service_logs(3)

    report = {
        'type': 'run.hourly_report',
        'run_id': run_id,
        'timestamp': now_iso(),
        'pids': pids,
        'last_messages': msgs,
        'service_logs_preview': logs
    }
    return report


def print_report(report: dict):
    header = f"Hourly report for {report.get('run_id')} @ {report.get('timestamp')}"
    print('\n' + header)
    print('-' * len(header))
    pids = report.get('pids', {})
    if pids:
        print('PIDs: ' + ', '.join([f"{k}:{v}" for k, v in pids.items() if v]))
    msgs = report.get('last_messages') or []
    if msgs:
        print('\nLast messages:')
        for m in msgs:
            print('  ' + m)
    print('\nService logs preview:')
    for svc, lines in (report.get('service_logs_preview') or {}).items():
        print(f'  {svc}:')
        for l in lines:
            print('    ' + l)


def persist_report(report: dict):
    out = os.path.join(TMP, 'hourly_report.log')
    try:
        with open(out, 'a', encoding='utf-8') as f:
            f.write(json.dumps(report, ensure_ascii=False) + '\n')
    except Exception:
        pass


def main():
    print('Hourly report ready. Press Ctrl-C to stop.')
    while True:
        report = build_report()
        print_report(report)
        persist_report(report)
        append_event(report)
        if SEND_TELEGRAM:
            short = f"Hourly {report.get('run_id')} @ {report.get('timestamp')} - last: { (report.get('last_messages') or [''])[ -1 ] }"
            send_telegram(short)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
