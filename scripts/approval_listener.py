"""Poll Telegram getUpdates and record an approval when the configured user sends "APPROVE".

Usage:
  $env:TELEGRAM_BOT_TOKEN='...'; $env:CHAT_ID='...'; python scripts\approval_listener.py --timeout 1800

The script polls getUpdates and writes approval events/traces to `gaia.db` and `.tmp/approval.json`.
"""
import time
import os
import argparse
import json
import re
import random
from gaia import events, db
from scripts import telegram_client as tc
import signal
import tempfile
import threading

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APPR_FILE = os.path.join(ROOT, '.tmp', 'approval.json')
QUEUE_FILE = os.path.join(ROOT, '.tmp', 'telegram_queue.json')
PID_FILE = os.path.join(ROOT, '.tmp', 'approval_listener.pid')
HEALTH_FILE = os.path.join(ROOT, '.tmp', 'telegram_health.json')


def now():
    import datetime
    return datetime.datetime.utcnow().isoformat() + 'Z'


def write_approval(payload):
    os.makedirs(os.path.join(ROOT, '.tmp'), exist_ok=True)
    with open(APPR_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--timeout', type=int, default=1800, help='Seconds to wait for approval (default 1800)')
    p.add_argument('--poll', type=int, default=5, help='Poll interval seconds')
    args = p.parse_args()

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id_env = os.environ.get('CHAT_ID')
    if not token:
        print('ERROR: TELEGRAM_BOT_TOKEN env required')
        return 2

    # state file to persist offset and reply timestamps
    state_file = os.path.join(ROOT, '.tmp', 'telegram_state.json')
    state = tc.safe_load_json(state_file) or {}
    offset = state.get('offset')
    last_replies = state.get('last_replies', {})
    queue = tc.safe_load_json(QUEUE_FILE) or []

    deadline = time.time() + args.timeout
    print('Listening for APPROVE messages until', time.ctime(deadline))

    # single-instance check
    try:
        if os.path.exists(PID_FILE):
            try:
                with open(PID_FILE, 'r', encoding='utf-8') as f:
                    old = int(f.read().strip())
                # try to detect running process
                try:
                    os.kill(old, 0)
                    print('Another approval_listener seems to be running (pid', old, ') - exiting')
                    return 0
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        pass

    # write our pid atomically
    try:
        os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='approval_pid_', suffix='.tmp', dir=os.path.join(ROOT, '.tmp'))
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(str(os.getpid()))
        os.replace(tmp, PID_FILE)
    except Exception:
        pass

    def _cleanup(signum=None, frame=None):
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception:
            pass
        try:
            # update health as stopped
            tc.safe_save_json(HEALTH_FILE, {'running': False, 'ts': now()})
        except Exception:
            pass
        raise SystemExit(0)

    # ensure cleanup on signals
    try:
        signal.signal(signal.SIGTERM, _cleanup)
        signal.signal(signal.SIGINT, _cleanup)
    except Exception:
        pass

    # initial health
    try:
        tc.safe_save_json(HEALTH_FILE, {'running': True, 'started': now(), 'last_seen': None, 'processed': 0})
    except Exception:
        pass

    # use long-poll timeout limited to 60s per Telegram API
    lp_timeout = min(max(5, int(args.poll)), 60)

    while time.time() < deadline:
        try:
            resp = tc.get_updates(token, offset=offset, timeout=lp_timeout)
            if not resp or not resp.get('ok'):
                time.sleep(1)
                continue
            for item in resp.get('result', []):
                offset = item['update_id'] + 1
                # support callback_query updates as well as messages
                callback = item.get('callback_query')
                if callback:
                    # handle inline button presses
                    cqid = callback.get('id')
                    data = callback.get('data')
                    from_user = callback.get('from') or {}
                    chat = (callback.get('message') or {}).get('chat') or {}
                    message = callback.get('message') or {}
                    from_id = from_user.get('id') or chat.get('id')
                    print('Got callback from', from_id, 'data=', data)
                    # acknowledge callback immediately
                    try:
                        tc.answer_callback(token, cqid, text='Received')
                    except Exception:
                        pass
                    # parse and act
                    try:
                        if isinstance(data, str):
                            parts = data.split(':', 1)
                            if len(parts) == 2:
                                cmd, arg = parts[0], parts[1]
                                from scripts import tg_command_manager as tcm
                                # authorization: only allow certain Telegram user IDs to approve/proceed
                                # configure via TELEGRAM_APPROVER_IDS env var (comma-separated list)
                                approvers_cfg = os.environ.get('TELEGRAM_APPROVER_IDS')
                                allowed_approvers = None
                                if approvers_cfg:
                                    try:
                                        allowed_approvers = set(int(x.strip()) for x in approvers_cfg.split(',') if x.strip())
                                    except Exception:
                                        allowed_approvers = None
                                # from_id is the Telegram user id of the actor
                                try:
                                    caller_id = int(from_id)
                                except Exception:
                                    caller_id = None
                                
                                # handle 'postpone' as a first-class action
                                if cmd == 'postpone':
                                    try:
                                        pending = tcm.list_pending()
                                        target = next((it for it in pending if it.get('id') == arg), None)
                                        if not target:
                                            tc.send_message(token, from_id, f'Command {arg} not found to postpone')
                                        else:
                                            target['status'] = 'postponed'
                                            target['postponed_at'] = now()
                                            # persist changes
                                            try:
                                                tcm.safe_save(tcm.PENDING, pending)
                                            except Exception:
                                                pass
                                            events.make_event('command.postponed', {'id': arg, 'by': from_id})
                                            try:
                                                tcm.write_audit(arg, 'postponed', {'by': from_id})
                                            except Exception:
                                                pass
                                            try:
                                                tc.send_message(token, from_id, f'Command {arg} postponed')
                                            except Exception:
                                                pass
                                    except Exception as e:
                                        print('postpone handling error', e)
                                    # persist offset and continue
                                    state['offset'] = offset
                                    tc.safe_save_json(state_file, state)
                                    continue

                                if cmd == 'approve':
                                    # check permissions
                                    if allowed_approvers and caller_id not in allowed_approvers:
                                        try:
                                            tc.send_message(token, from_id, 'Unauthorized: you are not allowed to approve commands.')
                                        except Exception:
                                            pass
                                    else:
                                        tcm.approve(arg, actor=caller_id)
                                        # Fast-path: if approver requested execution and is authorized, auto-proceed
                                        try:
                                            pending_items = tcm.list_pending()
                                            target = next((it for it in pending_items if it.get('id') == arg), None)
                                            if target:
                                                opts = target.get('options') or {}
                                                # Only auto-proceed when the actor is an allowed approver (or no approver restriction)
                                                if opts.get('exec_request') and (not allowed_approvers or caller_id in allowed_approvers):
                                                    allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                                    dry = not allow
                                                    try:
                                                        res, err = tcm.execute(arg, dry_run=dry)
                                                        if not res:
                                                            try:
                                                                tc.send_message(token, from_id, f'Auto-proceed execution failed: {err}')
                                                            except Exception:
                                                                pass
                                                        else:
                                                            summary = f"Execution status: {res.get('status')}"
                                                            if res.get('rc') is not None:
                                                                summary += f" rc={res.get('rc')}"
                                                            try:
                                                                tc.send_message(token, from_id, f'Auto-proceed result for {arg}: {summary}')
                                                            except Exception:
                                                                pass
                                                    except Exception:
                                                        pass
                                        except Exception:
                                            pass
                                    events.make_event('command.approved', {'id': arg, 'via': 'callback', 'by': from_id})
                                    db.write_trace(action='command.approved', status='ok', details={'id': arg, 'by': from_id})
                                    try:
                                        tc.send_message(token, from_id, f'Command {arg} approved (via button)')
                                    except Exception:
                                        pass
                                elif cmd == 'deny':
                                    if allowed_approvers and caller_id not in allowed_approvers:
                                        try:
                                            tc.send_message(token, from_id, 'Unauthorized: you are not allowed to deny commands.')
                                        except Exception:
                                            pass
                                    else:
                                        tcm.deny(arg, actor=caller_id)
                                    events.make_event('command.denied', {'id': arg, 'via': 'callback', 'by': from_id})
                                    db.write_trace(action='command.denied', status='ok', details={'id': arg, 'by': from_id})
                                    try:
                                        tc.send_message(token, from_id, f'Command {arg} denied (via button)')
                                    except Exception:
                                        pass
                                elif cmd == 'info':
                                    # send a brief summary of the pending command
                                    pending = tcm.list_pending()
                                    found = None
                                    for it in pending:
                                        if it.get('id') == arg:
                                            found = it
                                            break
                                    if found:
                                        try:
                                            txt = f"Command info:\n{found.get('command')}\nstatus: {found.get('status')}\ncreated: {found.get('created')}"
                                            tc.send_message(token, from_id, txt)
                                        except Exception:
                                            pass
                                elif cmd == 'toggle':
                                    # toggle an option and edit the original message to reflect new checkbox state
                                    parts2 = arg.split(':', 1)
                                    if len(parts2) == 2:
                                        cmd_id = parts2[0]
                                        opt = parts2[1]
                                        try:
                                            newopts = tcm.toggle_option(cmd_id, opt, actor=from_id)
                                            # edit the original message keyboard to update checkbox marks
                                            try:
                                                msg = callback.get('message') or {}
                                                mid = msg.get('message_id')
                                                chat = (msg.get('chat') or {}).get('id')
                                                # rebuild keyboard from newopts
                                                monitor_base = tcm.load_env().get('MONITOR_BASE_URL') or os.environ.get('MONITOR_BASE_URL')
                                                # Minimal keyboard: Approve / Deny / Info / Proceed
                                                buttons = [
                                                    [ { 'text': 'Approve', 'callback_data': f"approve:{cmd_id}" }, { 'text': 'Deny', 'callback_data': f"deny:{cmd_id}" } ],
                                                    [ { 'text': 'Info', 'callback_data': f"info:{cmd_id}" } ],
                                                ]
                                                # Add a final Proceed button row; enabled only if exec_request option selected and command is approved
                                                try:
                                                    pending = tcm.list_pending()
                                                    target = None
                                                    for it in pending:
                                                        if it.get('id') == cmd_id:
                                                            target = it
                                                            break
                                                    proceed_enabled = bool(newopts.get('exec_request')) and target and target.get('status') == 'approved'
                                                except Exception:
                                                    proceed_enabled = bool(newopts.get('exec_request'))
                                                # Always show Proceed (enabled only when exec_request & approved)
                                                if proceed_enabled:
                                                    buttons.append([{ 'text': 'Proceed ▶', 'callback_data': f"proceed:{cmd_id}" }])
                                                else:
                                                    buttons.append([{ 'text': 'Proceed (disabled)', 'callback_data': f"proceed_disabled:{cmd_id}" }])
                                                if monitor_base:
                                                    url = monitor_base.rstrip('/') + '/?tab=overview#pending'
                                                    buttons.append([{'text':'Open Monitor','url':url}])
                                                reply_markup = { 'inline_keyboard': buttons }
                                                from scripts.telegram_client import edit_message_text
                                                edit_message_text(token, chat, mid, msg.get('text') or '', reply_markup=reply_markup)
                                            except Exception:
                                                pass
                                        except Exception as e:
                                            print('toggle option failed', e)
                                elif cmd == 'proceed' or cmd == 'proceed_disabled':
                                    # proceed request (may be disabled)
                                    target_id = arg
                                    try:
                                        from scripts import tg_command_manager as tcm
                                        items = tcm.list_pending()
                                        target = next((it for it in items if it.get('id') == target_id), None)
                                        if not target:
                                            tc.send_message(token, from_id, f'Command {target_id} not found')
                                        else:
                                            # permission check for proceeding
                                            if allowed_approvers and caller_id not in allowed_approvers:
                                                tc.send_message(token, from_id, 'Unauthorized: you are not allowed to proceed/execute commands.')
                                            else:
                                                opts = target.get('options') or {}
                                                if not opts.get('exec_request'):
                                                    tc.send_message(token, from_id, 'Enable "Request Execute" option before proceeding')
                                                elif target.get('status') != 'approved':
                                                    tc.send_message(token, from_id, 'Command must be approved before proceeding')
                                                else:
                                                    # perform execution (dry-run unless allowed)
                                                    allow = tcm.load_env().get('ALLOW_COMMAND_EXECUTION') == '1'
                                                    dry = not allow
                                                    res, err = tcm.execute(target_id, dry_run=dry)
                                                    if not res:
                                                        tc.send_message(token, from_id, f'Execution failed: {err}')
                                                    else:
                                                        summary = f"Execution status: {res.get('status')}"
                                                        if res.get('rc') is not None:
                                                            summary += f" rc={res.get('rc')}"
                                                        tc.send_message(token, from_id, f'Proceed result for {target_id}: {summary}')
                                    except Exception as e:
                                        print('proceed handling error', e)
                    except Exception as e:
                        print('callback handling error', e)
                    # persist offset and continue
                    state['offset'] = offset
                    tc.safe_save_json(state_file, state)
                    continue
                msg = item.get('message') or item.get('channel_post')
                if not msg:
                    continue
                chat = msg.get('chat', {})
                text = msg.get('text', '') or ''
                from_id = chat.get('id')
                print('Got message from', from_id, 'text=', text)
                # update health last_seen
                try:
                    h = tc.safe_load_json(HEALTH_FILE) or {}
                    h['last_seen'] = now()
                    tc.safe_save_json(HEALTH_FILE, h)
                except Exception:
                    pass

                # persist offset immediately so restarts don't reprocess
                state['offset'] = offset
                tc.safe_save_json(state_file, state)

                # ignore other chats if CHAT_ID configured
                if chat_id_env and str(from_id) != str(chat_id_env):
                    print('Ignoring message from other chat', from_id)
                    continue

                # small rate-limit on generic ACKs per chat (seconds)
                ack_min_interval = 60
                now_ts = int(time.time())

                # Ack templates (varying, friendlier)
                WARM_ACKS = [
                    "Thanks — I'll take a look and get back to you shortly.",
                    "Got it — I'm on it and will update you soon.",
                    "Thanks for the note. I'll check this and reply when I have an update.",
                    "Received — I'll investigate and report back shortly.",
                ]

                GENERIC_ACKS = [
                    "Message received — noted.",
                    "I heard you — thanks, I'll process this.",
                    "Thanks, I've queued this and will respond after checking.",
                ]

                def _maybe_send_ack(chat_id, first_name=None):
                    last = last_replies.get(str(chat_id)) or 0
                    if now_ts - int(last) < ack_min_interval:
                        return False
                    try:
                        template = random.choice(GENERIC_ACKS)
                        if first_name:
                            text_to_send = f"Hi {first_name}, {template}"
                        else:
                            text_to_send = f"GAIA Monitor: {template}"
                        tc.send_message(token, chat_id, text_to_send)
                        last_replies[str(chat_id)] = now_ts
                        state['last_replies'] = last_replies
                        tc.safe_save_json(state_file, state)
                        return True
                    except Exception:
                        return False

                if isinstance(text, str):
                    if re.search(r'\b(?:/)?approve\b', text, re.IGNORECASE):
                        payload = {'approved_by': from_id, 'timestamp': now(), 'raw': msg}
                        events.make_event('approval.received', payload)
                        db.write_trace(action='approval.received', status='ok', details=payload)
                        write_approval(payload)
                        print('Approval recorded (matched):', text)
                        try:
                            tc.send_message(token, from_id, 'GAIA Monitor: approval received and recorded. Thank you.')
                        except Exception:
                            pass
                        return 0
                    else:
                        # Immediate ACK for greetings (bypass rate-limit)
                        if re.search(r"\b(hi|hello|hey|heelo)\b", text, re.IGNORECASE):
                            try:
                                # friendlier immediate ACK for greetings
                                first = (msg.get('from') or {}).get('first_name')
                                warm = random.choice(WARM_ACKS)
                                if first:
                                    ack_text = f"Hi {first}! {warm}"
                                else:
                                    ack_text = f"GAIA Monitor: {warm}"
                                tc.send_message(token, from_id, ack_text, reply_to_message_id=msg.get('message_id'))
                            except Exception:
                                pass
                        else:
                            # generic acknowledgement for other messages (rate-limited)
                            first = (msg.get('from') or {}).get('first_name')
                            _maybe_send_ack(from_id, first_name=first)

                        # enqueue the message for sequential processing (store minimal fields)
                        try:
                            item = {'chat_id': from_id, 'message_id': msg.get('message_id'), 'text': text, 'from': msg.get('from'), 'ts': now()}
                            queue.append(item)
                            tc.safe_save_json(QUEUE_FILE, queue)
                            events.make_event('telegram.enqueued', {'chat_id': from_id, 'message_id': msg.get('message_id')})
                            db.write_trace(action='telegram.enqueued', status='ok', details=item)
                        except Exception:
                            pass

                        # process queue sequentially (one-by-one)
                        while True:
                            try:
                                queue = tc.safe_load_json(QUEUE_FILE) or []
                                if not queue:
                                    break
                                next_item = queue.pop(0)
                                # persist trimmed queue immediately
                                tc.safe_save_json(QUEUE_FILE, queue)
                                # show typing indicator while we prepare/send the reply
                                class TypingIndicator:
                                    def __init__(self, token, chat_id, interval=4.0):
                                        self.token = token
                                        self.chat_id = chat_id
                                        self.interval = interval
                                        self._stop = threading.Event()
                                        self._thr = None

                                    def _loop(self):
                                        try:
                                            while not self._stop.wait(self.interval):
                                                try:
                                                    tc.send_chat_action(self.token, self.chat_id, action='typing')
                                                except Exception:
                                                    pass
                                        except Exception:
                                            pass

                                    def start(self):
                                        self._stop.clear()
                                        self._thr = threading.Thread(target=self._loop, daemon=True)
                                        self._thr.start()

                                    def stop(self):
                                        try:
                                            self._stop.set()
                                        except Exception:
                                            pass
                                        try:
                                            if self._thr:
                                                self._thr.join(timeout=0.1)
                                        except Exception:
                                            pass
                                # build reply referencing original message
                                chatid = next_item.get('chat_id')
                                mid = next_item.get('message_id')
                                orig = (next_item.get('text') or '').strip()
                                reply_text = f"Processing your message (id:{mid}): '{(orig[:200] + '...') if len(orig)>200 else orig}'"
                                ti = TypingIndicator(token, chatid)
                                ti.start()
                                try:
                                    # send reply while typing indicator runs
                                    tc.send_message(token, chatid, reply_text, reply_to_message_id=mid)
                                    events.make_event('telegram.processed', {'chat_id': chatid, 'message_id': mid, 'reply': reply_text})
                                    db.write_trace(action='telegram.processed', status='ok', details={'chat_id': chatid, 'message_id': mid})
                                    # update health processed count
                                    try:
                                        h = tc.safe_load_json(HEALTH_FILE) or {}
                                        h['processed'] = int(h.get('processed', 0)) + 1
                                        h['last_processed'] = now()
                                        tc.safe_save_json(HEALTH_FILE, h)
                                    except Exception:
                                        pass
                                except Exception as e:
                                    # if send fails, requeue at front and break to avoid tight loop
                                    queue.insert(0, next_item)
                                    tc.safe_save_json(QUEUE_FILE, queue)
                                    events.make_event('telegram.process_failed', {'chat_id': chatid, 'message_id': mid, 'error': str(e)})
                                    db.write_trace(action='telegram.process_failed', status='failed', details={'error': str(e)})
                                    ti.stop()
                                    break
                                finally:
                                    try:
                                        ti.stop()
                                    except Exception:
                                        pass
                                # small pause between replies
                                time.sleep(1)
                            except Exception:
                                break
        except Exception as e:
            print('poll error:', e)
            time.sleep(2)
            continue

    print('Timeout waiting for approval')
    events.make_event('approval.timeout', {'timeout': args.timeout})
    db.write_trace(action='approval.timeout', status='timeout', details={'timeout': args.timeout})
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
