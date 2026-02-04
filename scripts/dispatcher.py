"""Dispatcher: process queued Telegram messages, parse intents, call gaia.agent_manager,
and reply conversationally via Telegram.

This is a simple rules-based dispatcher for commands:
- "status" or "report": returns agent status
- "list agents" or "list": lists known agents
- "start <agent>" / "stop <agent>": starts/stops agents via gaia.agent_manager
- "help": short help text

Usage: python scripts/dispatcher.py
"""
import re
import time
import json
from pathlib import Path
from scripts.env_utils import preferred_env_path
from contextlib import redirect_stdout
import io

ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = ROOT / '.tmp' / 'telegram_queue.json'
ENV_FILE = preferred_env_path(ROOT)

def load_env():
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        if '=' not in line: continue
        k,v = line.split('=',1)
        env[k.strip()] = v.strip()
    return env

def safe_load_json(p):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return []

def safe_save_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    tmp.replace(p)

def parse_intent(text: str):
    t = (text or '').strip()
    lc = t.lower()
    if re.search(r'\b(report|status)\b', lc):
        return ('status', None)
    if re.search(r'\b(list agents|list)\b', lc):
        return ('list', None)
    m = re.search(r'\bstart\s+(\S+)\b', lc)
    if m:
        return ('start', m.group(1))
    m = re.search(r'\bstop\s+(\S+)\b', lc)
    if m:
        return ('stop', m.group(1))
    if re.search(r'\bhelp\b', lc):
        return ('help', None)
    return ('unknown', None)

def reply_for_unknown():
    return ("I'm not sure what you meant. Try 'report', 'list', 'start <agent>', "
            "or 'stop <agent>'. Send 'help' for more info.")

def run_once():
    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    from scripts import telegram_client as tc
    from gaia import agent_manager as am

    queue = safe_load_json(QUEUE_FILE) or []
    if not queue:
        print('No queued messages')
        return 0

    while queue:
        item = queue.pop(0)
        safe_save_json(QUEUE_FILE, queue)
        chat_id = item.get('chat_id')
        mid = item.get('message_id')
        text = (item.get('text') or '').strip()
        user = (item.get('from') or {}).get('first_name')
        intent, arg = parse_intent(text)
        # initial conversational ACK
        try:
            ack = f"Hi {user}! I'll process your request: '{text[:200]}'"
            tc.send_message(token, chat_id, ack, reply_to_message_id=mid)
        except Exception:
            pass

        if intent == 'status':
            # build a friendly agent summary using agent_manager internals
            try:
                agents_cfg = am._load_agents()
            except Exception:
                agents_cfg = []
            pids = am._read_pids()
            lines = []
            if not agents_cfg:
                # fallback to status()
                buf = io.StringIO()
                with redirect_stdout(buf):
                    try:
                        am.status()
                    except Exception as e:
                        print('status error', e)
                body = buf.getvalue().strip() or 'No status available.'
                reply = f"Agent status summary:\n{body}"
            else:
                for a in agents_cfg:
                    aid = str(a.get('id') or a.get('name') or '').strip()
                    entry = pids.get(aid) if isinstance(pids, dict) else None
                    pid = None
                    alive = False
                    try:
                        if isinstance(entry, dict):
                            pid = entry.get('pid')
                        else:
                            pid = int(entry)
                    except Exception:
                        pid = None
                    try:
                        alive = bool(am._pid_is_running(pid)) if pid else False
                    except Exception:
                        alive = False
                    st = 'online' if alive else 'stopped'
                    lines.append(f"- {aid}: {st} (pid:{pid or '—'})")
                reply = "Agent status summary:\n" + "\n".join(lines) if lines else 'No agents found.'
        elif intent == 'list':
            buf = io.StringIO()
            with redirect_stdout(buf):
                try:
                    am.list_agents()
                except Exception as e:
                    print('list error', e)
            body = buf.getvalue().strip() or 'No agents.'
            reply = f"Known agents:\n{body}"
        elif intent == 'start' and arg:
            # call start_agent and capture return code
            buf = io.StringIO()
            with redirect_stdout(buf):
                try:
                    rc = am.start_agent(arg)
                    print('start rc', rc)
                except Exception as e:
                    print('start error', e)
            reply = f"Start request for '{arg}':\n{buf.getvalue()}"
        elif intent == 'stop' and arg:
            buf = io.StringIO()
            with redirect_stdout(buf):
                try:
                    rc = am.stop_agent(arg)
                    print('stop rc', rc)
                except Exception as e:
                    print('stop error', e)
            reply = f"Stop request for '{arg}':\n{buf.getvalue()}"
        elif intent == 'help':
            reply = ("Commands: 'report'/'status' — show agent status; 'list' — list agents; "
                     "'start <agent>' / 'stop <agent>' — control agents.")
        else:
            reply = reply_for_unknown()

        # send reply
        try:
            tc.send_message(token, chat_id, reply, reply_to_message_id=mid)
        except Exception:
            # on failure, append to failed file (best-effort)
            failed = safe_load_json(ROOT / '.tmp' / 'telegram_queue_failed.json') or []
            item['_error'] = 'send_failed'
            failed.append(item)
            safe_save_json(ROOT / '.tmp' / 'telegram_queue_failed.json', failed)

        # small pause
        time.sleep(0.5)

    print('Dispatcher run complete')
    return 0

if __name__ == '__main__':
    raise SystemExit(run_once())
