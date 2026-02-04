"""Production-ready approval listener.

This implementation listens for Telegram updates (long-poll), handles
callback_query and textual approvals, writes an approval marker to
`.tmp/approval.json`, emits heartbeat to `.tmp/telegram_health.json`,
and rotates a debug log. It is safe to run in the background and will
attempt auto-proceed when `exec_request` option is set and
`ALLOW_COMMAND_EXECUTION=1` is configured.
"""

import argparse
import json
import os
import signal
import tempfile
import threading
import time
import traceback
from pathlib import Path

from gaia import events, db
from scripts import telegram_client as tc
from scripts.i18n import t as _t
from scripts import telegram_queue as tq
from scripts import telegram_idempotency as tid


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APPR_FILE = os.path.join(ROOT, '.tmp', 'approval.json')
STATE_FILE = os.path.join(ROOT, '.tmp', 'telegram_state.json')
HEALTH_FILE = os.path.join(ROOT, '.tmp', 'telegram_health.json')
DEBUG_LOG = os.path.join(ROOT, '.tmp', 'approval_debug.log')
PID_FILE = os.path.join(ROOT, '.tmp', 'approval_listener.pid')


def now():
    import datetime

    return datetime.datetime.utcnow().isoformat() + 'Z'


def log_debug(msg, obj=None, rotate_bytes=10_000_000):
    try:
        ts = now()
        line = f"{ts} - {msg}"
        if obj is not None:
            try:
                line += ' | ' + json.dumps(obj, default=str)
            except Exception:
                line += ' | ' + str(obj)
        os.makedirs(os.path.dirname(DEBUG_LOG), exist_ok=True)
        try:
            if os.path.exists(DEBUG_LOG) and os.path.getsize(DEBUG_LOG) > int(rotate_bytes):
                for i in (3, 2):
                    src = f"{DEBUG_LOG}.{i-1}"
                    dst = f"{DEBUG_LOG}.{i}"
                    if os.path.exists(src):
                        try:
                            if os.path.exists(dst):
                                os.remove(dst)
                        except Exception:
                            pass
                        try:
                            os.replace(src, dst)
                        except Exception:
                            pass
                try:
                    if os.path.exists(f"{DEBUG_LOG}.1"):
                        os.remove(f"{DEBUG_LOG}.1")
                except Exception:
                    pass
                try:
                    os.replace(DEBUG_LOG, f"{DEBUG_LOG}.1")
                except Exception:
                    pass
        except Exception:
            pass
        with open(DEBUG_LOG, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        try:
            with open(DEBUG_LOG + '.err', 'a', encoding='utf-8') as f:
                f.write('log_debug failed: ' + traceback.format_exc() + '\n')
        except Exception:
            pass


def write_approval(payload):
    os.makedirs(os.path.dirname(APPR_FILE), exist_ok=True)
    with open(APPR_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)


def _cleanup():
    try:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except Exception:
        pass
    try:
        tc.safe_save_json(HEALTH_FILE, {'running': False, 'ts': now()})
    except Exception:
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--timeout', type=int, default=1800)
    p.add_argument('--poll', type=int, default=5)
    p.add_argument('--continue-on-approve', action='store_true')
    p.add_argument('--rotate-bytes', type=int, default=10_000_000)
    args = p.parse_args()

    from scripts.env_utils import load_preferred_env
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        try:
            env = load_preferred_env(Path(ROOT))
            token = env.get('TELEGRAM_BOT_TOKEN')
        except Exception:
            token = None

    if not token:
        print('ERROR: TELEGRAM_BOT_TOKEN required')
        return 2

    # write pid
    try:
        os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='approval_pid_', suffix='.tmp', dir=os.path.join(ROOT, '.tmp'))
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(str(os.getpid()))
        os.replace(tmp, PID_FILE)
    except Exception:
        pass

    # initial health
    try:
        tc.safe_save_json(HEALTH_FILE, {'running': True, 'started': now(), 'last_seen': None, 'pid': os.getpid()})
    except Exception:
        pass

    stop_event = threading.Event()

    def _hb():
        while not stop_event.wait(max(2, args.poll)):
            try:
                h = tc.safe_load_json(HEALTH_FILE) or {}
                h['running'] = True
                h['last_seen'] = now()
                h['pid'] = os.getpid()
                tc.safe_save_json(HEALTH_FILE, h)
                log_debug('heartbeat', {'pid': h.get('pid')}, rotate_bytes=args.rotate_bytes)
            except Exception:
                pass

    t = threading.Thread(target=_hb, daemon=True)
    t.start()

    def _handle(signum, frame):
        stop_event.set()
        _cleanup()
        raise SystemExit(0)

    try:
        signal.signal(signal.SIGINT, _handle)
        signal.signal(signal.SIGTERM, _handle)
    except Exception:
        pass

    state = tc.safe_load_json(STATE_FILE) or {}
    offset = state.get('offset')

    lp_timeout = min(max(5, args.poll), 60)
    deadline = time.time() + args.timeout
    print('Listening for approvals until', time.ctime(deadline))

    while time.time() < deadline:
        try:
            resp = tc.get_updates(token, offset=offset, timeout=lp_timeout)
            if not resp or not resp.get('ok'):
                time.sleep(1)
                continue
            # Enqueue all received updates (deduplicated) and advance persisted offset
            for item in resp.get('result', []):
                offset = item.get('update_id', offset) + 1
                try:
                    try:
                        appended = tq.append_dedup(item)
                    except Exception:
                        appended = True
                    if not appended:
                        log_debug('duplicate_update_skipped', {'update_id': item.get('update_id')}, rotate_bytes=args.rotate_bytes)
                except Exception:
                    pass
                state['offset'] = offset
                tc.safe_save_json(STATE_FILE, state)

            # Drain the durable queue and process items one-by-one (idempotent handling expected)
            while True:
                queued = tq.pop_next()
                if not queued:
                    break
                try:
                    # process queued update (reuse existing inline handling)
                    item = queued
                    offset = item.get('update_id', offset) + 1
                    callback = item.get('callback_query')
                    if callback:
                        cqid = callback.get('id')
                        # skip already-processed callback queries (idempotency)
                        try:
                            if cqid and tid.seen_callback(cqid):
                                log_debug('skip_seen_callback', {'cqid': cqid}, rotate_bytes=args.rotate_bytes)
                                state['offset'] = offset
                                tc.safe_save_json(STATE_FILE, state)
                                continue
                        except Exception:
                            # if idempotency check fails, continue processing normally
                            pass
                        data = callback.get('data')
                        from_user = callback.get('from') or {}
                        from_id = from_user.get('id')
                        try:
                            # localized short ack (prefer .private then .tmp)
                            default_lang = 'en'
                            try:
                                env = load_preferred_env(Path(ROOT))
                                default_lang = env.get('TELEGRAM_DEFAULT_LANG', 'en')
                            except Exception:
                                default_lang = 'en'
                            tc.answer_callback(token, cqid, text=_t('received', default_lang))
                        except Exception:
                            try:
                                tc.record_failed_reply({'action': 'answer_callback', 'callback_query_id': cqid, 'error': traceback.format_exc(), 'update': item, 'ts': now()})
                            except Exception:
                                pass
                        log_debug('callback', {'from': from_id, 'data': data}, rotate_bytes=args.rotate_bytes)
                        if isinstance(data, str) and ':' in data:
                            cmd, arg = data.split(':', 1)
                            try:
                                from scripts import tg_command_manager as tcm
                                if cmd == 'approve':
                                    tcm.approve(arg, actor=from_id)
                                    events.make_event('command.approved', {'id': arg, 'via': 'callback', 'by': from_id})
                                    db.write_trace(action='command.approved', status='ok', details={'id': arg, 'by': from_id})
                                    log_debug('approved_via_callback', {'id': arg, 'by': from_id}, rotate_bytes=args.rotate_bytes)
                                    try:
                                        pending = tcm.list_pending()
                                        target = next((it for it in pending if it.get('id') == arg), None)
                                        opts = (target.get('options') or {}) if target else {}
                                        if opts.get('exec_request'):
                                            allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                            dry = not allow
                                            res, err = tcm.execute(arg, dry_run=dry)
                                            log_debug('auto_proceed', {'id': arg, 'res': res and {'status': res.get('status'), 'rc': res.get('rc')} if res else None, 'err': err}, rotate_bytes=args.rotate_bytes)
                                    except Exception:
                                        pass
                                elif cmd == 'deny':
                                    tcm.deny(arg, actor=from_id)
                                    events.make_event('command.denied', {'id': arg, 'via': 'callback', 'by': from_id})
                                    db.write_trace(action='command.denied', status='ok', details={'id': arg, 'by': from_id})
                                    log_debug('denied_via_callback', {'id': arg, 'by': from_id}, rotate_bytes=args.rotate_bytes)
                                elif cmd == 'proceed':
                                    try:
                                        pending = tcm.list_pending()
                                        target = next((it for it in pending if it.get('id') == arg), None)
                                        if target and target.get('status') == 'approved' and (target.get('options') or {}).get('exec_request'):
                                            allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                            dry = not allow
                                            res, err = tcm.execute(arg, dry_run=dry)
                                            log_debug('proceed', {'id': arg, 'res': res and {'status': res.get('status'), 'rc': res.get('rc')} if res else None, 'err': err}, rotate_bytes=args.rotate_bytes)
                                    except Exception:
                                        pass
                            except Exception:
                                log_debug('callback_cmd_error', {'data': data, 'err': traceback.format_exc()}, rotate_bytes=args.rotate_bytes)
                        # mark callback idempotent only after succesful processing
                        try:
                            if callback and cqid:
                                tid.mark_callback(cqid)
                        except Exception:
                            pass

                        state['offset'] = offset
                        tc.safe_save_json(STATE_FILE, state)
                        continue

                    msg = item.get('message') or item.get('channel_post')
                    if not msg:
                        state['offset'] = offset
                        tc.safe_save_json(STATE_FILE, state)
                        continue
                    text = msg.get('text', '') or ''
                    from_id = (msg.get('from') or {}).get('id') or (msg.get('chat') or {}).get('id')
                    log_debug('message', {'from': from_id, 'text': text}, rotate_bytes=args.rotate_bytes)
                    # explicit textual approve/deny
                    explicit = None
                    try:
                        import re

                        explicit = re.search(r'\b(?:/)?(approve|deny)\s+([0-9a-fA-F\-]{6,})\b', text, re.IGNORECASE)
                    except Exception:
                        explicit = None
                    if explicit:
                        verb = explicit.group(1).lower()
                        cmd_id = explicit.group(2)
                        try:
                            from scripts import tg_command_manager as tcm
                            if verb == 'approve':
                                tcm.approve(cmd_id, actor=from_id)
                                events.make_event('command.approved', {'id': cmd_id, 'via': 'text', 'by': from_id})
                                db.write_trace(action='command.approved', status='ok', details={'id': cmd_id, 'by': from_id})
                                write_approval({'approved_by': from_id, 'timestamp': now(), 'id': cmd_id})
                                try:
                                    target = next((it for it in tcm.list_pending() if it.get('id') == cmd_id), None)
                                    opts = (target.get('options') or {}) if target else {}
                                    if opts.get('exec_request'):
                                        allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                        dry = not allow
                                        res, err = tcm.execute(cmd_id, dry_run=dry)
                                        log_debug('explicit_auto_proceed', {'id': cmd_id, 'res': res and {'status': res.get('status'), 'rc': res.get('rc')} if res else None, 'err': err}, rotate_bytes=args.rotate_bytes)
                                except Exception:
                                    pass
                            else:
                                tcm.deny(cmd_id, actor=from_id)
                                events.make_event('command.denied', {'id': cmd_id, 'via': 'text', 'by': from_id})
                                db.write_trace(action='command.denied', status='ok', details={'id': cmd_id, 'by': from_id})
                        except Exception:
                            log_debug('explicit_cmd_error', {'err': traceback.format_exc()}, rotate_bytes=args.rotate_bytes)
                        state['offset'] = offset
                        tc.safe_save_json(STATE_FILE, state)
                        if args.continue_on_approve:
                            continue
                        return 0
                    state['offset'] = offset
                    tc.safe_save_json(STATE_FILE, state)
                except Exception:
                    log_debug('process_queue_item_error', {'err': traceback.format_exc()}, rotate_bytes=args.rotate_bytes)
                    try:
                        # requeue the item for retry (don't modify seen index)
                        try:
                            tq.requeue(item, front=True)
                            log_debug('requeued_item', {'update_id': item.get('update_id')}, rotate_bytes=args.rotate_bytes)
                        except Exception:
                            log_debug('requeue_failed', {'update_id': item.get('update_id')}, rotate_bytes=args.rotate_bytes)
                    except Exception:
                        pass
                    # small backoff to avoid busy looping on persistent failures
                    time.sleep(min(1, max(0.1, args.poll)))
                    continue
                callback = item.get('callback_query')
                if callback:
                    cqid = callback.get('id')
                    data = callback.get('data')
                    from_user = callback.get('from') or {}
                    from_id = from_user.get('id')
                    try:
                        # localized short ack
                        try:
                            env = load_preferred_env(Path(ROOT))
                            default_lang = env.get('TELEGRAM_DEFAULT_LANG', 'en')
                        except Exception:
                            default_lang = 'en'
                        tc.answer_callback(token, cqid, text=_t('received', default_lang))
                    except Exception:
                        try:
                            tc.record_failed_reply({'action': 'answer_callback', 'callback_query_id': cqid, 'error': traceback.format_exc(), 'update': item, 'ts': now()})
                        except Exception:
                            pass
                    log_debug('callback', {'from': from_id, 'data': data}, rotate_bytes=args.rotate_bytes)
                    if isinstance(data, str) and ':' in data:
                        cmd, arg = data.split(':', 1)
                        try:
                            from scripts import tg_command_manager as tcm
                            if cmd == 'approve':
                                tcm.approve(arg, actor=from_id)
                                events.make_event('command.approved', {'id': arg, 'via': 'callback', 'by': from_id})
                                db.write_trace(action='command.approved', status='ok', details={'id': arg, 'by': from_id})
                                log_debug('approved_via_callback', {'id': arg, 'by': from_id}, rotate_bytes=args.rotate_bytes)
                                try:
                                    pending = tcm.list_pending()
                                    target = next((it for it in pending if it.get('id') == arg), None)
                                    opts = (target.get('options') or {}) if target else {}
                                    if opts.get('exec_request'):
                                        allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                        dry = not allow
                                        res, err = tcm.execute(arg, dry_run=dry)
                                        log_debug('auto_proceed', {'id': arg, 'res': res and {'status': res.get('status'), 'rc': res.get('rc')} if res else None, 'err': err}, rotate_bytes=args.rotate_bytes)
                                except Exception:
                                    pass
                            elif cmd == 'deny':
                                tcm.deny(arg, actor=from_id)
                                events.make_event('command.denied', {'id': arg, 'via': 'callback', 'by': from_id})
                                db.write_trace(action='command.denied', status='ok', details={'id': arg, 'by': from_id})
                                log_debug('denied_via_callback', {'id': arg, 'by': from_id}, rotate_bytes=args.rotate_bytes)
                            elif cmd == 'proceed':
                                try:
                                    pending = tcm.list_pending()
                                    target = next((it for it in pending if it.get('id') == arg), None)
                                    if target and target.get('status') == 'approved' and (target.get('options') or {}).get('exec_request'):
                                        allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                        dry = not allow
                                        res, err = tcm.execute(arg, dry_run=dry)
                                        log_debug('proceed', {'id': arg, 'res': res and {'status': res.get('status'), 'rc': res.get('rc')} if res else None, 'err': err}, rotate_bytes=args.rotate_bytes)
                                except Exception:
                                    pass
                        except Exception:
                            log_debug('callback_cmd_error', {'data': data, 'err': traceback.format_exc()}, rotate_bytes=args.rotate_bytes)
                    state['offset'] = offset
                    tc.safe_save_json(STATE_FILE, state)
                    continue

                msg = item.get('message') or item.get('channel_post')
                if not msg:
                    continue
                text = msg.get('text', '') or ''
                from_id = (msg.get('from') or {}).get('id') or (msg.get('chat') or {}).get('id')
                log_debug('message', {'from': from_id, 'text': text}, rotate_bytes=args.rotate_bytes)
                # explicit textual approve/deny
                explicit = None
                try:
                    import re

                    explicit = re.search(r'\\b(?:/)?(approve|deny)\\s+([0-9a-fA-F\\-]{6,})\\b', text, re.IGNORECASE)
                except Exception:
                    explicit = None
                if explicit:
                    verb = explicit.group(1).lower()
                    cmd_id = explicit.group(2)
                    try:
                        from scripts import tg_command_manager as tcm
                        if verb == 'approve':
                            tcm.approve(cmd_id, actor=from_id)
                            events.make_event('command.approved', {'id': cmd_id, 'via': 'text', 'by': from_id})
                            db.write_trace(action='command.approved', status='ok', details={'id': cmd_id, 'by': from_id})
                            write_approval({'approved_by': from_id, 'timestamp': now(), 'id': cmd_id})
                            try:
                                target = next((it for it in tcm.list_pending() if it.get('id') == cmd_id), None)
                                opts = (target.get('options') or {}) if target else {}
                                if opts.get('exec_request'):
                                    allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                    dry = not allow
                                    res, err = tcm.execute(cmd_id, dry_run=dry)
                                    log_debug('explicit_auto_proceed', {'id': cmd_id, 'res': res and {'status': res.get('status'), 'rc': res.get('rc')} if res else None, 'err': err}, rotate_bytes=args.rotate_bytes)
                            except Exception:
                                pass
                        else:
                            tcm.deny(cmd_id, actor=from_id)
                            events.make_event('command.denied', {'id': cmd_id, 'via': 'text', 'by': from_id})
                            db.write_trace(action='command.denied', status='ok', details={'id': cmd_id, 'by': from_id})
                    except Exception:
                        log_debug('explicit_cmd_error', {'err': traceback.format_exc()}, rotate_bytes=args.rotate_bytes)
                    if args.continue_on_approve:
                        state['offset'] = offset
                        tc.safe_save_json(STATE_FILE, state)
                        continue
                    return 0

                state['offset'] = offset
                tc.safe_save_json(STATE_FILE, state)

        except Exception:
            log_debug('poll_error', {'err': traceback.format_exc()}, rotate_bytes=args.rotate_bytes)
            time.sleep(1)
            continue

    stop_event.set()
    _cleanup()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
