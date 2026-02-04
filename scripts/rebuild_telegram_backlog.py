"""Rebuild and normalize the Telegram pending commands backlog.

Usage:
    python scripts/rebuild_telegram_backlog.py [--post]

By default this will:
 - load `.tmp/pending_commands.json`
 - dedupe by `id` (keep latest), normalize `created` timestamps, sort by created
 - write back the normalized file

With `--post` it will also post any `pending` items that lack a `posted_at`
flag to the configured Telegram chat using `.tmp/telegram.env`.

The script is careful and best-effort: use `--post` only if you want live resends.
"""
from pathlib import Path
import json, argparse, datetime, time

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / '.tmp' / 'pending_commands.json'
from scripts.env_utils import preferred_env_path
ENV = preferred_env_path(ROOT)
EVENTS = ROOT / 'events.ndjson'


def load_env(path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
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
    tmp.replace(path)


def parse_created(it):
    c = it.get('created')
    if not c:
        return datetime.datetime.min
    try:
        if isinstance(c, str) and c.endswith('Z'):
            return datetime.datetime.fromisoformat(c.replace('Z','+00:00'))
        return datetime.datetime.fromisoformat(c)
    except Exception:
        try:
            return datetime.datetime.fromtimestamp(float(c))
        except Exception:
            return datetime.datetime.min


def normalize_and_dedupe(items):
    # keep latest by created for duplicate ids
    byid = {}
    for it in items:
        _id = it.get('id')
        if not _id:
            continue
        cur = byid.get(_id)
        if not cur:
            byid[_id] = it
            continue
        # pick the one with later created
        a = parse_created(cur)
        b = parse_created(it)
        if b >= a:
            byid[_id] = it
    out = list(byid.values())
    out.sort(key=lambda x: parse_created(x))
    return out


def post_to_telegram(env, item):
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('TELEGRAM_NOTIFY_CHAT') or env.get('CHAT_ID') or env.get('TELEGRAM_CHAT_ID') or item.get('chat_id')
    if not token or not chat:
        raise RuntimeError('missing token/chat')
    is_test = bool((item.get('options') or {}).get('is_test'))
    warn_prefix = '⚠️ TEST COMMAND — DO NOT PRESS PROCEED\n\n' if is_test else ''
    text = warn_prefix + f"Approval requested:\n{(item.get('command') or '')}\n\nid: {item.get('id')}\ncreated: {item.get('created')}"
    if is_test:
        buttons = [
            [ { 'text': '🧪 Approve (test)', 'callback_data': f"approve:{item['id']}" }, { 'text': 'Deny', 'callback_data': f"deny:{item['id']}" } ],
            [ { 'text': 'Info', 'callback_data': f"info:{item['id']}" } ],
            [ { 'text': '🔴 Proceed (disabled - TEST)', 'callback_data': f"proceed_disabled:{item['id']}" } ]
        ]
    else:
        buttons = [
            [ { 'text': 'Approve', 'callback_data': f"approve:{item['id']}" }, { 'text': 'Deny', 'callback_data': f"deny:{item['id']}" } ],
            [ { 'text': 'Info', 'callback_data': f"info:{item['id']}" } ],
            [ { 'text': 'Proceed (disabled)', 'callback_data': f"proceed_disabled:{item['id']}" } ]
        ]
    reply_markup = { 'inline_keyboard': buttons }
    # import here to avoid top-level network requirement
    from scripts.telegram_client import send_message
    return send_message(token, chat, text, reply_markup=reply_markup)


def main(post=False):
    items = safe_load(PENDING) or []
    if not items:
        print('No pending commands file found or empty.')
        return 1
    norm = normalize_and_dedupe(items)
    # annotate created in consistent ISO Z
    for it in norm:
        dt = parse_created(it)
        try:
            it['created'] = dt.astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
        except Exception:
            try:
                it['created'] = datetime.datetime.utcnow().isoformat() + 'Z'
            except Exception:
                it['created'] = str(it.get('created'))
    safe_save(PENDING, norm)
    print(f'Wrote normalized pending commands ({len(norm)} entries) to {PENDING}')

    if post:
        env = load_env(ENV)
        sent = 0
        for it in norm:
            if it.get('status') != 'pending':
                continue
            if it.get('posted_at'):
                continue
            try:
                resp = post_to_telegram(env, it)
                it['posted_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
                it['_posted_response'] = resp
                sent += 1
                # sleep small backoff
                time.sleep(0.4)
            except Exception as e:
                print('Failed to post', it.get('id'), str(e))
        safe_save(PENDING, norm)
        print(f'Posted {sent} pending items to Telegram (posted_at set).')
    return 0


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--post', action='store_true', help='Post pending items to Telegram')
    args = p.parse_args()
    rc = main(post=args.post)
    raise SystemExit(rc)
