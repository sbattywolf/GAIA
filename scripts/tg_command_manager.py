"""Telegram command manager (prototype, dry-run by default).

This script parses inbound Telegram messages for commands, enqueues them
to `.tmp/pending_commands.json` for human approval, and provides CLI
operations to list, approve, and (optionally) execute commands.

Safety: actual command execution is disabled unless environment variable
`ALLOW_COMMAND_EXECUTION=1` is present in `.tmp/telegram.env` and the
`--execute` flag is passed to the CLI. This avoids accidental remote code
execution while testing.
"""
from pathlib import Path
import json
import time
import argparse
import uuid
import os
from datetime import datetime
import sqlite3
from datetime import timedelta

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp'
PENDING = TMP / 'pending_commands.json'
ENV_FILE = TMP / 'telegram.env'
EVENTS = ROOT / 'events.ndjson'
DB_PATH = ROOT / 'gaia.db'


def _init_db():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS command_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command_id TEXT,
                action TEXT,
                ts TEXT,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception:
        pass


def write_audit(command_id, action, details=None):
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute('INSERT INTO command_audit (command_id, action, ts, details) VALUES (?, ?, ?, ?)',
                    (str(command_id), action, now(), json.dumps(details or {})))
        conn.commit()
        conn.close()
    except Exception:
        pass


# initialize DB for audit
_init_db()

def load_env():
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        if '=' not in line: continue
        k,v=line.split('=',1)
        env[k.strip()] = v.strip()
    return env

def safe_load(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return []

def safe_save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    os.replace(str(tmp), str(path))

def now():
    return datetime.utcnow().isoformat() + 'Z'

def parse_commands_from_text(text: str):
    """Very small parser: lines starting with `run:` or triple-backtick blocks are commands."""
    cmds = []
    # code block parser
    if '```' in text:
        parts = text.split('```')
        for i in range(1, len(parts), 2):
            cmds.append(parts[i].strip())
    # run: prefix
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith('run:'):
            cmds.append(line[len('run:'):].strip())
    return [c for c in cmds if c]

def enqueue_command(chat_id, message_id, text, sender):
    # expire old items first
    expire_old()
    items = safe_load(PENDING) or []
    cmds = parse_commands_from_text(text)
    added = []
    for c in cmds:
        item = {
            'id': str(uuid.uuid4()),
            'chat_id': chat_id,
            'message_id': message_id,
            'command': c,
            'from': sender,
            'status': 'pending',
            'created': now(),
        }
        items.append(item)
        added.append(item)
        append_event({'type': 'command.enqueued', 'payload': {'id': item['id'], 'chat_id': chat_id, 'message_id': message_id, 'command_preview': c[:120]}, 'timestamp': now()})
        # write audit row
        try:
            write_audit(item['id'], 'enqueued', {'chat_id': chat_id, 'message_id': message_id, 'command': c})
        except Exception:
            pass
    safe_save(PENDING, items)
    # Send a short approval notifier to the configured Telegram chat (best-effort)
    try:
        env = load_env()
        token = env.get('TELEGRAM_BOT_TOKEN')
        # allow override to notify a specific admin chat id
        notify_chat = env.get('TELEGRAM_NOTIFY_CHAT') or env.get('CHAT_ID') or env.get('TELEGRAM_CHAT_ID') or chat_id
        if token and added:
            monitor_base = env.get('MONITOR_BASE_URL') or os.environ.get('MONITOR_BASE_URL')
            lines = [f"Approval requested ({len(added)}):"]
            for a in added:
                preview = a['command'].strip().splitlines()[0][:200]
                lines.append(f"- {preview}")
                lines.append(f"  id: {a['id']}")
                lines.append(f"  created: {a['created']}")
                lines.append(f"  CLI approve: python scripts/tg_command_manager.py approve {a['id']}")
                if monitor_base:
                    lines.append(f"  UI: {monitor_base} (open Pending Commands)")
                lines.append('')
            lines.append('Note: execution is disabled by default (ALLOW_COMMAND_EXECUTION=1 to enable).')
            msg = "\n".join(lines)
            try:
                from scripts.telegram_client import send_message
                # send per-command message with action buttons (callback_data)
                for a in added:
                    text = f"Approval requested:\n{(a['command'][:240])}\n\nid: {a['id']}\ncreated: {a['created']}"
                    # Minimal interactive buttons: Approve / Deny / Info / Proceed (disabled initially)
                    buttons = [
                        [ { 'text': 'Approve', 'callback_data': f"approve:{a['id']}" }, { 'text': 'Deny', 'callback_data': f"deny:{a['id']}" } ],
                        [ { 'text': 'Info', 'callback_data': f"info:{a['id']}" } ],
                        [ { 'text': 'Proceed (disabled)', 'callback_data': f"proceed_disabled:{a['id']}" } ]
                    ]
                    # optionally include monitor URL button as well
                    if monitor_base:
                        url = monitor_base.rstrip('/') + '/?tab=overview'
                        try:
                            url = monitor_base.rstrip('/') + '/?tab=overview#pending'
                        except Exception:
                            pass
                        buttons.append([{'text': 'Open Monitor', 'url': url}])
                    reply_markup = { 'inline_keyboard': buttons }
                    send_message(token, notify_chat, text, reply_markup=reply_markup)
                append_event({'type': 'approval.requested', 'payload': {'count': len(added)}, 'timestamp': now()})
            except Exception:
                append_event({'type': 'approval.requested.failed', 'payload': {'count': len(added)}, 'timestamp': now()})
    except Exception:
        pass

    return added

def list_pending():
    expire_old()
    return safe_load(PENDING) or []

def approve(id_or_index, actor=None):
    expire_old()
    items = safe_load(PENDING) or []
    if not items:
        return None
    # allow numeric index or id
    target = None
    try:
        idx = int(id_or_index)
        if 0 <= idx < len(items):
            target = items[idx]
    except Exception:
        for it in items:
            if it.get('id') == id_or_index:
                target = it
                break
    if not target:
        return None
    target['status'] = 'approved'
    target['approved_at'] = now()
    if actor:
        target['approved_by'] = actor
    safe_save(PENDING, items)
    append_event({'type': 'command.approved', 'payload': {'id': target['id'], 'chat_id': target['chat_id']}, 'timestamp': now()})
    # write audit
    try:
        write_audit(target['id'], 'approved', {'chat_id': target.get('chat_id'), 'approved_at': target.get('approved_at'), 'by': actor})
    except Exception:
        pass
    # notify via Telegram (best-effort)
    try:
        env = load_env()
        token = env.get('TELEGRAM_BOT_TOKEN')
        chat = env.get('CHAT_ID') or env.get('TELEGRAM_CHAT_ID') or target.get('chat_id')
        if token and chat:
            from scripts.telegram_client import send_message
            note = f"Command approved: id={target['id']}\n{(target.get('command') or '').strip()}\nTo execute: python scripts/tg_command_manager.py execute {target['id']} --execute (requires ALLOW_COMMAND_EXECUTION=1)"
            try:
                send_message(token, chat, note)
            except Exception:
                pass
    except Exception:
        pass
    return target


def deny(id_or_index, actor=None):
    items = safe_load(PENDING) or []
    if not items:
        return None
    target = None
    try:
        idx = int(id_or_index)
        if 0 <= idx < len(items):
            target = items[idx]
    except Exception:
        for it in items:
            if it.get('id') == id_or_index:
                target = it
                break
    if not target:
        return None
    target['status'] = 'denied'
    target['denied_at'] = now()
    if actor:
        target['denied_by'] = actor
    safe_save(PENDING, items)
    append_event({'type': 'command.denied', 'payload': {'id': target['id'], 'chat_id': target.get('chat_id')}, 'timestamp': now()})
    try:
        write_audit(target['id'], 'denied', {'chat_id': target.get('chat_id'), 'by': actor})
    except Exception:
        pass
    return target


def toggle_option(command_id, option_key, actor=None):
    """Toggle a boolean option for a pending command (returns the new state dict or None)."""
    items = safe_load(PENDING) or []
    target = None
    for it in items:
        if it.get('id') == command_id:
            target = it
            break
    if not target:
        return None
    opts = target.get('options') or {}
    newv = not bool(opts.get(option_key))
    opts[option_key] = bool(newv)
    target['options'] = opts
    safe_save(PENDING, items)
    append_event({'type': 'command.option.toggled', 'payload': {'id': command_id, 'option': option_key, 'value': newv, 'by': actor}, 'timestamp': now()})
    try:
        write_audit(command_id, 'option_toggled', {'option': option_key, 'value': newv, 'by': actor})
    except Exception:
        pass
    return opts

def execute(id_or_index, dry_run=True):
    env = load_env()
    allow = env.get('ALLOW_COMMAND_EXECUTION') == '1'
    items = safe_load(PENDING) or []
    expire_old()
    target = None
    try:
        idx = int(id_or_index)
        if 0 <= idx < len(items):
            target = items[idx]
    except Exception:
        for it in items:
            if it.get('id') == id_or_index:
                target = it
                break
    if not target:
        return None, 'not_found'
    if target.get('status') != 'approved':
        return None, 'not_approved'
    # execution behavior
    if dry_run or not allow:
        target['status'] = 'executed_dryrun'
        target['executed_at'] = now()
        target['_note'] = 'dry-run (no real execution)'
        safe_save(PENDING, items)
        append_event({'type': 'command.executed.dryrun', 'payload': {'id': target['id'], 'command': target['command']}, 'timestamp': now()})
        try:
            write_audit(target['id'], 'executed_dryrun', {'command': target.get('command')})
        except Exception:
            pass
        return target, None
    # real execution (dangerous): spawn subprocess safely (not implemented by default)
    try:
        import subprocess
        proc = subprocess.run(target['command'], shell=True, capture_output=True, text=True, timeout=60)
        target['status'] = 'executed'
        target['executed_at'] = now()
        target['rc'] = proc.returncode
        target['stdout'] = proc.stdout[:4000]
        target['stderr'] = proc.stderr[:4000]
        safe_save(PENDING, items)
        append_event({'type': 'command.executed', 'payload': {'id': target['id'], 'rc': proc.returncode}, 'timestamp': now()})
        try:
            write_audit(target['id'], 'executed', {'rc': proc.returncode})
        except Exception:
            pass
        return target, None
    except Exception as e:
        target['_error'] = str(e)
        target['status'] = 'failed'
        safe_save(PENDING, items)
        append_event({'type': 'command.execute.error', 'payload': {'id': target['id'], 'error': str(e)}, 'timestamp': now()})
        try:
            write_audit(target['id'], 'execute_error', {'error': str(e)})
        except Exception:
            pass
        return target, str(e)


def expire_old(retention_days=7):
    """Expire pending commands older than `retention_days` days."""
    try:
        items = safe_load(PENDING) or []
        if not items:
            return
        changed = False
        now_dt = datetime.utcnow()
        out_items = []
        for it in items:
            created = it.get('created')
            try:
                if created and isinstance(created, str) and created.endswith('Z'):
                    cdt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                else:
                    cdt = datetime.fromisoformat(created)
            except Exception:
                cdt = None
            if cdt and (now_dt - cdt) > timedelta(days=retention_days):
                # mark expired
                it['status'] = 'expired'
                it['expired_at'] = now()
                append_event({'type': 'command.expired', 'payload': {'id': it.get('id')}, 'timestamp': now()})
                try:
                    write_audit(it.get('id'), 'expired', {'created': created})
                except Exception:
                    pass
                changed = True
                # keep in list for history purposes
                out_items.append(it)
            else:
                out_items.append(it)
        if changed:
            safe_save(PENDING, out_items)
    except Exception:
        pass

def append_event(obj):
    try:
        EVENTS.parent.mkdir(parents=True, exist_ok=True)
        with open(EVENTS, 'a', encoding='utf-8') as f:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    except Exception:
        pass

def cli():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd')
    en = sub.add_parser('enqueue')
    en.add_argument('--chat', required=True)
    en.add_argument('--message-id', required=True)
    en.add_argument('--text', required=True)
    en.add_argument('--sender', default='unknown')

    ls = sub.add_parser('list')
    ls.add_argument('--all', action='store_true')

    ap = sub.add_parser('approve')
    ap.add_argument('id_or_index')

    ex = sub.add_parser('execute')
    ex.add_argument('id_or_index')
    ex.add_argument('--execute', action='store_true', help='Perform real execution (requires ALLOW_COMMAND_EXECUTION=1 in .tmp/telegram.env)')

    args = p.parse_args()
    if args.cmd == 'enqueue':
        added = enqueue_command(args.chat, args.message_id, args.text, args.sender)
        print('added', len(added))
        for a in added:
            print(a['id'], a['command'][:120])
    elif args.cmd == 'list':
        items = list_pending()
        for i, it in enumerate(items):
            print(i, it.get('id'), it.get('status'), it.get('command')[:140])
    elif args.cmd == 'approve':
        t = approve(args.id_or_index)
        if not t:
            print('not found')
        else:
            print('approved', t['id'])
    elif args.cmd == 'execute':
        dry = not args.execute
        t, err = execute(args.id_or_index, dry_run=dry)
        if not t:
            print('not found or error', err)
        else:
            print('executed status=', t.get('status'))
    else:
        p.print_help()

if __name__ == '__main__':
    cli()
