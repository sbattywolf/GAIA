import os
import time
import json
import glob
import datetime
import requests
from . import backlog_source

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, '.tmp')
EVENTS = os.path.join(ROOT, 'events.ndjson')
RUN_META = os.path.join(TMP, 'run_20h.json')
LAST_MESSAGES = os.path.join(TMP, 'last_messages.log')
STOP_FILE = os.path.join(TMP, 'stop_run')

INTERVAL = int(os.environ.get('SUPERVISOR_INTERVAL_SECONDS', '600'))  # default 10 minutes
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.environ.get('TELEGRAM_CHAT_ID') or os.environ.get('TELEGRAM_CHAT')
# When true, only send Telegram summaries and do not append full run.snapshot events to events.ndjson
TELEGRAM_ONLY = os.environ.get('SUPERVISOR_TELEGRAM_ONLY', '1').lower() in ('1', 'true', 'yes')


def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def load_run_id():
    try:
        with open(RUN_META, 'r', encoding='utf-8') as f:
            return json.load(f).get('run_id')
    except Exception:
        return 'run_unknown'


def read_last_messages():
    try:
        with open(LAST_MESSAGES, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return lines[-20:]
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


def tail_service_logs():
    logs = {}
    for name in ('monitor_framework', 'resource_monitor', 'automation_runner', 'approval_listener'):
        path = os.path.join(TMP, f'{name}.out')
        try:
            with open(path, 'rb') as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                to_read = 4096
                f.seek(max(0, size - to_read))
                data = f.read().decode('utf-8', errors='replace')
                logs[name] = data.strip().splitlines()[-20:]
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
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': TELEGRAM_CHAT, 'text': text})
        return r.status_code == 200
    except Exception:
        return False


def build_snapshot():
    run_id = load_run_id()
    pids = read_pid_files()
    messages = read_last_messages()
    logs = tail_service_logs()
    snapshot = {
        'type': 'run.snapshot',
        'run_id': run_id,
        'timestamp': now_iso(),
        'pids': pids,
        'last_messages': messages[-5:],
        'service_logs_preview': {k: v[-3:] for k, v in logs.items()}
    }
    return snapshot


def main():
    send_telegram(f'Run supervisor snapshotter started for {load_run_id()}')
    while True:
        if os.path.exists(STOP_FILE):
            evt = {'type': 'run.stop.requested', 'run_id': load_run_id(), 'timestamp': now_iso(), 'payload': {'reason': 'stop_file'}}
            append_event(evt)
            send_telegram(f'Run stop requested for {load_run_id()}; exiting supervisor.')
            return

        snapshot = build_snapshot()
        # Optionally append full snapshot event to events.ndjson
        if not TELEGRAM_ONLY:
            append_event(snapshot)

        # Compose short summary for Telegram using concise backlog-oriented template
        msgs = snapshot.get('last_messages') or []
        pids = snapshot.get('pids') or {}

        # compute simple backlog stats from events.ndjson
        def backlog_stats():
            total = 0
            completed = 0
            tasks = set()
            completed_tasks = set()
            try:
                with open(EVENTS, 'r', encoding='utf-8') as ef:
                    for line in ef:
                        try:
                            j = json.loads(line)
                        except Exception:
                            continue
                        t = j.get('type', '')
                        tid = j.get('task_id') or j.get('task') or (j.get('payload') if isinstance(j.get('payload'), dict) else {}).get('task_id')
                        if not tid and isinstance(j.get('payload'), dict):
                            tid = j['payload'].get('id')
                        if t.startswith('task.') and tid:
                            tasks.add(tid)
                            if t == 'task.complete':
                                completed_tasks.add(tid)
            except Exception:
                pass
            total = len(tasks)
            completed = len(completed_tasks)
            pending = max(0, total - completed)
            return completed, total, pending

        completed, total, pending = backlog_stats()

        in_progress = ', '.join([k for k, v in pids.items() if v]) or 'None'

        # Use a concise template with top pending items (dynamic via backlog_source)
        lines = []
        lines.append(f"GAIA status — {completed}/{total} completed, {pending} pending")
        lines.append(f"In-progress: {in_progress}")
        lines.append('')
        lines.append('Top pending:')

        tops = backlog_source.get_top_pending(6)
        if tops:
            for i, t in enumerate(tops, start=1):
                # ensure numbered lines
                if str(i) not in t.split()[0]:
                    lines.append(f"{i}. {t}")
                else:
                    lines.append(t)
        else:
            # fallback static list
            lines.append('1. Monitor PR CI — Watch PR #6 / chore/fix-ci-workflow CI runs, collect failures/logs, and report back; re-run fixes until green.')
            lines.append('2. Merge PR & tag release — After CI succeeds and review, merge branch and create a small release note for online-agent/CI fixes.')
            lines.append('3. Purge leaked tokens from history — Prepare `git filter-repo` instructions and `sensitive.txt` replacement lines; coordinate force-push with collaborators.')
            lines.append('4. Add secret scanning & pre-commit — Install `detect-secrets` baseline and `pre-commit` hooks to prevent future leaks; add to CI checks.')
            lines.append('5. Create protected production environment — Create GitHub Environment `production`, add rotated secrets, require reviewers before deployment and ALLOW_COMMAND_EXECUTION toggle.')
            lines.append('6. Finalize CI smoke & integration steps — Ensure smoke-step runs and add an integration matrix for mock Telegram test; fail PR if smoke fails.')

        lines.append('')
        lines.append('More backlog stats will be added over time.')

        summary = '\n'.join(lines)
        send_telegram(summary)

        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
