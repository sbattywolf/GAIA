from flask import Flask, jsonify, render_template, request, send_file, Response
import os
import json
import subprocess
import shutil
from datetime import datetime, timedelta, timezone
import re
import uuid
import time
import threading
import math
import sqlite3
import queue
import requests
import glob
from scripts import sequence_manager as sm

# configurable agents file (repo-root by default)
AGENTS_CONFIG_PATH = os.environ.get('GAIA_AGENTS_CONFIG', os.path.join(os.getcwd(), 'agents.json'))

_AGENTS_CFG_CACHE = None

def load_agents_config():
    global _AGENTS_CFG_CACHE
    if _AGENTS_CFG_CACHE is not None:
        return _AGENTS_CFG_CACHE
    cfg = []
    try:
        if os.path.exists(AGENTS_CONFIG_PATH):
            with open(AGENTS_CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # normalize list of agent entries
            if isinstance(data, dict):
                # support single-object keyed by id
                for k, v in data.items():
                    entry = {'id': k}
                    if isinstance(v, dict):
                        entry.update(v)
                    else:
                        entry['name'] = str(v)
                    cfg.append(entry)
            elif isinstance(data, list):
                cfg = data
    except Exception:
        cfg = []
    # normalize aliases/match tokens
    for a in cfg:
        a['id'] = str(a.get('id') or a.get('name') or '').strip()
        aliases = a.get('aliases') or []
        if isinstance(aliases, str):
            aliases = [aliases]
        a['aliases'] = [str(x).lower() for x in aliases if x]
        matches = a.get('match') or []
        if isinstance(matches, str):
            matches = [matches]
        a['match'] = [str(x).lower() for x in matches if x]
    _AGENTS_CFG_CACHE = cfg
    return cfg

app = Flask(__name__, template_folder='templates', static_folder='static')
EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', os.path.join(os.getcwd(), 'events.ndjson'))
APPR_PATH = os.path.join(os.getcwd(), '.tmp', 'approval.json')

# Instruct endpoint auth + rate limiting (simple, in-memory)
INSTRUCT_API_KEY = os.environ.get('GAIA_INSTRUCT_API_KEY')
INSTRUCT_RATE_LIMIT = int(os.environ.get('GAIA_INSTRUCT_RATE_LIMIT', '20'))
INSTRUCT_RATE_WINDOW = int(os.environ.get('GAIA_INSTRUCT_RATE_WINDOW_SECONDS', '60'))
_INSTRUCT_RATE_STORE = {}
_INSTRUCT_RATE_LOCK = threading.Lock()

# DB for persisting rate counters across restarts
GAIA_DB_PATH = os.environ.get('GAIA_DB_PATH', os.path.join(os.getcwd(), 'gaia.db'))
_RATE_DB_CONN = None
_STATE_DB_CONN = None
_STATE_QUEUE = queue.Queue()
_STATE_POLL_INTERVAL = int(os.environ.get('GAIA_AGENT_POLL_SECONDS', '10'))

def _init_rate_db():
    global _RATE_DB_CONN
    try:
        conn = sqlite3.connect(GAIA_DB_PATH, check_same_thread=False)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS instruct_rate (
                key TEXT PRIMARY KEY,
                timestamps TEXT
            )
        ''')
        conn.commit()
        _RATE_DB_CONN = conn
    except Exception:
        _RATE_DB_CONN = None


def _init_state_db():
    global _STATE_DB_CONN
    try:
        conn = sqlite3.connect(GAIA_DB_PATH, check_same_thread=False)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS agents_state (
                id TEXT PRIMARY KEY,
                last_seen TEXT,
                state TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS agents_state_history (
                id TEXT,
                ts TEXT,
                state TEXT
            )
        ''')
        conn.commit()
        _STATE_DB_CONN = conn
    except Exception:
        _STATE_DB_CONN = None

def _load_rate_timestamps(key: str):
    if not _RATE_DB_CONN:
        return []
    try:
        cur = _RATE_DB_CONN.cursor()
        cur.execute('SELECT timestamps FROM instruct_rate WHERE key = ?', (key,))
        row = cur.fetchone()
        if not row or not row[0]:
            return []
        return json.loads(row[0])
    except Exception:
        return []

def _save_rate_timestamps(key: str, arr):
    if not _RATE_DB_CONN:
        return
    try:
        cur = _RATE_DB_CONN.cursor()
        cur.execute('REPLACE INTO instruct_rate (key, timestamps) VALUES (?, ?)', (key, json.dumps(arr)))
        _RATE_DB_CONN.commit()
    except Exception:
        pass

# initialize DB on import
_init_rate_db()
_init_state_db()

def instruct_is_rate_limited(key: str) -> bool:
    now = time.time()
    cutoff = now - INSTRUCT_RATE_WINDOW
    with _INSTRUCT_RATE_LOCK:
        # load persisted timestamps first
        arr = []
        try:
            arr = _load_rate_timestamps(key)
        except Exception:
            arr = []
        # purge old
        arr = [t for t in arr if t >= cutoff]
        if len(arr) >= INSTRUCT_RATE_LIMIT:
            # persist trimmed array
            try:
                _save_rate_timestamps(key, arr)
            except Exception:
                pass
            return True
        arr.append(now)
        try:
            _save_rate_timestamps(key, arr)
        except Exception:
            # fallback to in-memory if DB write fails
            _INSTRUCT_RATE_STORE[key] = arr
        return False

def instruct_rate_retry_after(key: str) -> int:
    """Return seconds until rate window resets for this key, or 0 if not limited."""
    now = time.time()
    cutoff = now - INSTRUCT_RATE_WINDOW
    try:
        arr = _load_rate_timestamps(key) if _RATE_DB_CONN else _INSTRUCT_RATE_STORE.get(key, [])
    except Exception:
        arr = _INSTRUCT_RATE_STORE.get(key, [])
    # purge old
    arr = [t for t in arr if t >= cutoff]
    if len(arr) < INSTRUCT_RATE_LIMIT:
        return 0
    oldest = min(arr)
    retry = INSTRUCT_RATE_WINDOW - (now - oldest)
    return max(0, math.ceil(retry))


def read_last_events(n=50):
    if not os.path.exists(EVENTS_PATH):
        return []
    try:
        with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-n:]
    except Exception:
        return []
    events = []
    for l in lines:
        l = l.strip()
        if not l:
            continue
        try:
            events.append(json.loads(l))
        except Exception:
            events.append({'raw': l})
    return events


def _save_agent_state(id: str, state: dict):
    if not _STATE_DB_CONN:
        return
    try:
        cur = _STATE_DB_CONN.cursor()
        now = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
        cur.execute('REPLACE INTO agents_state (id, last_seen, state) VALUES (?, ?, ?)', (id, now, json.dumps(state, ensure_ascii=False)))
        cur.execute('INSERT INTO agents_state_history (id, ts, state) VALUES (?, ?, ?)', (id, now, json.dumps(state, ensure_ascii=False)))
        _STATE_DB_CONN.commit()
    except Exception:
        pass


def _load_agent_state(id: str):
    if not _STATE_DB_CONN:
        return None
    try:
        cur = _STATE_DB_CONN.cursor()
        cur.execute('SELECT last_seen, state FROM agents_state WHERE id = ?', (id,))
        row = cur.fetchone()
        if not row:
            return None
        return {'last_seen': row[0], 'state': json.loads(row[1])}
    except Exception:
        return None


def _tail_file(path, n=50):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read().splitlines()
        return '\n'.join(data[-n:])
    except Exception:
        return ''


def probe_agent_by_cfg(cfg, pids_map):
    # cfg: agent config dict from agents.json
    aid = cfg.get('id') or cfg.get('name') or ''
    aid = str(aid)
    res = {'id': aid, 'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')}
    # pid info
    pid_entry = pids_map.get(aid) if pids_map else None
    pid = None
    alive = False
    fallback = False
    last_log = ''
    if pid_entry:
        if isinstance(pid_entry, dict):
            pid = pid_entry.get('pid')
            outp = pid_entry.get('out') or ''
            errp = pid_entry.get('err') or ''
            if '.fallback.' in outp or '.fallback.' in errp:
                fallback = True
            # tail out
            if outp and os.path.exists(outp):
                last_log = _tail_file(outp, 20)
        else:
            try:
                pid = int(pid_entry)
            except Exception:
                pid = None
    if pid:
        alive = _pid_is_running(pid)
    res.update({'pid': pid, 'alive': bool(alive), 'fallback': bool(fallback), 'last_log': last_log})

    # optional health probe via cfg.health_url
    health = None
    try:
        health_url = cfg.get('health_url')
        if health_url:
            # simple GET
            r = requests.get(health_url, timeout=2)
            try:
                health = r.json()
            except Exception:
                health = {'status_code': r.status_code, 'text': r.text[:200]}
    except Exception:
        health = None
    if health is not None:
        res['health'] = health

    return res


def probe_all_agents():
    cfgs = load_agents_config()
    # read pids map
    pids_path = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
    pmap = {}
    if os.path.exists(pids_path):
        try:
            with open(pids_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            pmap = data.get('pids') if isinstance(data, dict) and 'pids' in data else data
        except Exception:
            pmap = {}
    results = {}
    for c in cfgs:
        try:
            st = probe_agent_by_cfg(c, pmap)
            results[st['id']] = st
            # persist
            _save_agent_state(st['id'], st)
            # enqueue event for SSE
            try:
                _STATE_QUEUE.put_nowait(st)
            except Exception:
                pass
        except Exception:
            continue
    return results


def _state_poller_loop():
    while True:
        try:
            probe_all_agents()
        except Exception:
            pass
        time.sleep(_STATE_POLL_INTERVAL)


_STATE_POLLER_THREAD = threading.Thread(target=_state_poller_loop, daemon=True)
_STATE_POLLER_THREAD.start()


@app.route('/api/events')
def api_events():
    n = int(request.args.get('n', 50))
    return jsonify(read_last_events(n))


@app.route('/api/approval/state')
def api_approval_state():
    """Return the current approval artifact if present."""
    try:
        if not os.path.exists(APPR_PATH):
            return jsonify({'ok': True, 'approved': False, 'file': None})
        with open(APPR_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'ok': True, 'approved': True, 'file': APPR_PATH, 'payload': data})
    except Exception:
        return jsonify({'ok': False, 'error': 'read_failed'})


@app.route('/api/approval/stream')
def api_approval_stream():
    """SSE stream that emits an `approval` event when `.tmp/approval.json` is created/updated."""
    def gen():
        last_mtime = 0
        while True:
            try:
                if os.path.exists(APPR_PATH):
                    m = os.path.getmtime(APPR_PATH)
                    if m and m != last_mtime:
                        last_mtime = m
                        try:
                            with open(APPR_PATH, 'r', encoding='utf-8') as f:
                                payload = json.load(f)
                        except Exception:
                            payload = {'ok': False}
                        safe = json.dumps(payload, ensure_ascii=False)
                        yield f"event: approval\n"
                        yield f"data: {safe}\n\n"
                # heartbeat
                yield ':\n\n'
                time.sleep(1)
            except GeneratorExit:
                return
            except Exception:
                time.sleep(1)

    return Response(gen(), mimetype='text/event-stream')


@app.route('/api/telegram/health')
def api_telegram_health():
    """Return current telegram health JSON if present."""
    hpath = os.path.join(os.getcwd(), '.tmp', 'telegram_health.json')
    qpath = os.path.join(os.getcwd(), '.tmp', 'telegram_queue.json')
    out = {'ok': True, 'health': None, 'queue_len': None}
    try:
        if os.path.exists(hpath):
            with open(hpath, 'r', encoding='utf-8') as f:
                out['health'] = json.load(f)
    except Exception:
        out['health'] = None
    try:
        if os.path.exists(qpath):
            with open(qpath, 'r', encoding='utf-8') as f:
                q = json.load(f)
                out['queue_len'] = len(q) if isinstance(q, list) else None
    except Exception:
        out['queue_len'] = None
    return jsonify(out)


@app.route('/api/telegram/failures')
def api_telegram_failures():
    """Return a count and recent lines from `events.ndjson` related to Telegram failures."""
    path = os.path.join(os.getcwd(), 'events.ndjson')
    out = {'ok': True, 'count': 0, 'recent': []}
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            recent = []
            for l in lines[-1000:]:
                low = l.lower()
                if 'telegram' in low and ('fail' in low or 'error' in low or 'not found' in low or 'invalid-token' in low):
                    recent.append(l)
            out['count'] = len(recent)
            out['recent'] = recent[-10:]
    except Exception:
        out['ok'] = False
    return jsonify(out)


@app.route('/api/telegram/approvers')
def api_telegram_approvers():
    """Return configured approver Telegram user IDs (from TELEGRAM_APPROVER_IDS env var)."""
    cfg = os.environ.get('TELEGRAM_APPROVER_IDS')
    out = {'ok': True, 'approvers': []}
    try:
        if cfg:
            out['approvers'] = [int(x.strip()) for x in cfg.split(',') if x.strip()]
    except Exception:
        out['approvers'] = []
    return jsonify(out)


@app.route('/api/telegram/stream')
def api_telegram_stream():
    """SSE stream that emits telegram health and queue changes."""
    def gen():
        last_h_mtime = 0
        last_q_mtime = 0
        while True:
            try:
                # health file
                hpath = os.path.join(os.getcwd(), '.tmp', 'telegram_health.json')
                if os.path.exists(hpath):
                    m = os.path.getmtime(hpath)
                    if m and m != last_h_mtime:
                        last_h_mtime = m
                        try:
                            with open(hpath, 'r', encoding='utf-8') as f:
                                payload = json.load(f)
                        except Exception:
                            payload = {'ok': False}
                        safe = json.dumps(payload, ensure_ascii=False)
                        yield f"event: telegram_health\n"
                        yield f"data: {safe}\n\n"

                # queue file
                qpath = os.path.join(os.getcwd(), '.tmp', 'telegram_queue.json')
                if os.path.exists(qpath):
                    qm = os.path.getmtime(qpath)
                    if qm and qm != last_q_mtime:
                        last_q_mtime = qm
                        try:
                            with open(qpath, 'r', encoding='utf-8') as f:
                                q = json.load(f)
                        except Exception:
                            q = []
                        yield f"event: telegram_queue\n"
                        yield f"data: {json.dumps({'len': len(q) if isinstance(q, list) else None})}\n\n"

                # heartbeat
                yield ':\n\n'
                time.sleep(1)
            except GeneratorExit:
                return
            except Exception:
                time.sleep(1)

    return Response(gen(), mimetype='text/event-stream')


@app.route('/api/pending_commands')
def api_pending_commands():
    """Return the current pending commands list from `.tmp/pending_commands.json`."""
    path = os.path.join(os.getcwd(), '.tmp', 'pending_commands.json')
    try:
        if not os.path.exists(path):
            return jsonify({'ok': True, 'pending': []})
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'ok': True, 'pending': data})
    except Exception:
        return jsonify({'ok': False, 'pending': []}), 500


@app.route('/api/pending_commands/stream')
def api_pending_commands_stream():
    """SSE stream that emits `pending_commands` when `.tmp/pending_commands.json` changes."""
    def gen():
        last_mtime = 0
        p = os.path.join(os.getcwd(), '.tmp', 'pending_commands.json')
        while True:
            try:
                if os.path.exists(p):
                    m = os.path.getmtime(p)
                    if m and m != last_mtime:
                        last_mtime = m
                        try:
                            with open(p, 'r', encoding='utf-8') as f:
                                payload = json.load(f)
                        except Exception:
                            payload = []
                        safe = json.dumps({'pending': payload}, ensure_ascii=False)
                        yield f"event: pending_commands\n"
                        yield f"data: {safe}\n\n"
                # heartbeat
                yield ':\n\n'
                time.sleep(1)
            except GeneratorExit:
                return
            except Exception:
                time.sleep(1)

    return Response(gen(), mimetype='text/event-stream')


@app.route('/api/pending_commands/approve', methods=['POST'])
def api_pending_commands_approve():
    """Approve a pending command by id. Requires `GAIA_MONITOR_API_KEY` env var to match `key` in JSON body for basic protection."""
    try:
        body = request.get_json() or {}
        cid = body.get('id') or body.get('command_id')
        key = body.get('key')
        expected = os.environ.get('GAIA_MONITOR_API_KEY')
        if expected and expected != key:
            return jsonify({'ok': False, 'error': 'unauthorized'}), 401
        if not cid:
            return jsonify({'ok': False, 'error': 'missing_id'}), 400
        # delegate to tg_command_manager.approve
        try:
            from scripts import tg_command_manager as tcm
            res = tcm.approve(cid)
            if not res:
                return jsonify({'ok': False, 'error': 'not_found'}), 404
            # return resulting item
            return jsonify({'ok': True, 'approved': True, 'item': res})
        except Exception as e:
            return jsonify({'ok': False, 'error': 'approve_failed', 'detail': str(e)}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': 'bad_request', 'detail': str(e)}), 400


@app.route('/api/pending_commands', methods=['GET'])
def api_pending_commands_list():
    """Return list of pending commands (most recent last)."""
    try:
        from scripts import tg_command_manager as tcm
        items = tcm.list_pending() or []
        return jsonify({'ok': True, 'pending': items})
    except Exception as e:
        return jsonify({'ok': False, 'error': 'list_failed', 'detail': str(e)}), 500


@app.route('/api/pending_commands/toggle_test', methods=['POST'])
def api_pending_commands_toggle_test():
    """Toggle `is_test` option for a pending command via tg_command_manager.toggle_option."""
    try:
        body = request.get_json() or {}
        cid = body.get('id')
        key = body.get('key')
        expected = os.environ.get('GAIA_MONITOR_API_KEY')
        if expected and expected != key:
            return jsonify({'ok': False, 'error': 'unauthorized'}), 401
        if not cid:
            return jsonify({'ok': False, 'error': 'missing_id'}), 400
        from scripts import tg_command_manager as tcm
        opts = tcm.toggle_option(cid, 'is_test', actor='monitor')
        if opts is None:
            return jsonify({'ok': False, 'error': 'not_found'}), 404
        return jsonify({'ok': True, 'id': cid, 'options': opts})
    except Exception as e:
        return jsonify({'ok': False, 'error': 'toggle_failed', 'detail': str(e)}), 500


@app.route('/api/pending_commands/deny', methods=['POST'])
def api_pending_commands_deny():
    """Deny a pending command by id. Protected by `GAIA_MONITOR_API_KEY` similar to approve."""
    try:
        body = request.get_json() or {}
        cid = body.get('id') or body.get('command_id')
        key = body.get('key')
        expected = os.environ.get('GAIA_MONITOR_API_KEY')
        if expected and expected != key:
            return jsonify({'ok': False, 'error': 'unauthorized'}), 401
        if not cid:
            return jsonify({'ok': False, 'error': 'missing_id'}), 400
        try:
            from scripts import tg_command_manager as tcm
            res = tcm.deny(cid)
            if not res:
                return jsonify({'ok': False, 'error': 'not_found'}), 404
            return jsonify({'ok': True, 'denied': True, 'item': res})
        except Exception as e:
            return jsonify({'ok': False, 'error': 'deny_failed', 'detail': str(e)}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': 'bad_request', 'detail': str(e)}), 400


@app.route('/api/pending_commands/postpone', methods=['POST'])
def api_pending_commands_postpone():
    """Postpone a pending command (mark status)."""
    try:
        body = request.get_json() or {}
        cid = body.get('id') or body.get('command_id')
        key = body.get('key')
        expected = os.environ.get('GAIA_MONITOR_API_KEY')
        if expected and expected != key:
            return jsonify({'ok': False, 'error': 'unauthorized'}), 401
        if not cid:
            return jsonify({'ok': False, 'error': 'missing_id'}), 400
        try:
            from scripts import tg_command_manager as tcm
            items = tcm.list_pending()
            target = next((it for it in items if it.get('id') == cid), None)
            if not target:
                return jsonify({'ok': False, 'error': 'not_found'}), 404
            target['status'] = 'postponed'
            target['postponed_at'] = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
            try:
                tcm.safe_save(tcm.PENDING, items)
            except Exception:
                pass
            try:
                tcm.write_audit(cid, 'postponed', {'via': 'monitor'})
            except Exception:
                pass
            return jsonify({'ok': True, 'postponed': True, 'item': target})
        except Exception as e:
            return jsonify({'ok': False, 'error': 'postpone_failed', 'detail': str(e)}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': 'bad_request', 'detail': str(e)}), 400


@app.route('/api/pending_commands/info', methods=['GET'])
def api_pending_commands_info():
    """Return full info for a pending command id."""
    cid = request.args.get('id') or request.args.get('command_id')
    if not cid:
        return jsonify({'ok': False, 'error': 'missing_id'}), 400
    try:
        from scripts import tg_command_manager as tcm
        items = tcm.list_pending()
        target = next((it for it in items if it.get('id') == cid), None)
        if not target:
            return jsonify({'ok': False, 'error': 'not_found'}), 404
        return jsonify({'ok': True, 'item': target})
    except Exception as e:
        return jsonify({'ok': False, 'error': 'info_failed', 'detail': str(e)}), 500


@app.route('/api/sequences/active')
def api_sequences_active():
    """Return the current active task file if present."""
    path = os.path.join(os.getcwd(), '.tmp', 'active_task.json')
    try:
        if not os.path.exists(path):
            return jsonify({'ok': True, 'active': False, 'file': None})
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'ok': True, 'active': True, 'payload': data})
    except Exception:
        return jsonify({'ok': False, 'error': 'read_failed'})


@app.route('/api/sequences/todos')
def api_sequences_todos():
    path = os.path.join(os.getcwd(), '.tmp', 'sequence_todos.json')
    try:
        if not os.path.exists(path):
            return jsonify({'ok': True, 'todos': {}})
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'ok': True, 'todos': data})
    except Exception:
        return jsonify({'ok': False, 'todos': {}})


@app.route('/api/sequences/proposals')
def api_sequences_proposals():
    path = os.path.join(os.getcwd(), 'doc', 'SEQUENCE_PROPOSALS.md')
    try:
        if not os.path.exists(path):
            return jsonify({'ok': True, 'proposals': ''})
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read()
        return jsonify({'ok': True, 'proposals': txt})
    except Exception:
        return jsonify({'ok': False, 'proposals': ''})


@app.route('/api/controller/active')
def api_controller_active():
    """Return active task and its open todos."""
    try:
        active_path = os.path.join(os.getcwd(), '.tmp', 'active_task.json')
        if not os.path.exists(active_path):
            return jsonify({'ok': True, 'active': False, 'payload': None})
        with open(active_path, 'r', encoding='utf-8') as f:
            active = json.load(f)
        # load todos for this sequence
        todos = sm._load_todos()
        seq_id = active.get('active_sequence')
        filtered = {k: v for k, v in (todos or {}).items() if v.get('seq_id') == seq_id}
        return jsonify({'ok': True, 'active': True, 'payload': active, 'todos': filtered})
    except Exception:
        return jsonify({'ok': False, 'error': 'read_failed'})


@app.route('/api/controller/todos')
def api_controller_todos():
    try:
        todos = sm._load_todos()
        return jsonify({'ok': True, 'todos': todos})
    except Exception:
        return jsonify({'ok': False, 'todos': {}})


@app.route('/api/controller/claim', methods=['POST'])
def api_controller_claim():
    try:
        body = request.get_json() or {}
        tid = body.get('id')
        actor = body.get('actor') or body.get('claimed_by') or 'unknown'
        if not tid:
            return jsonify({'ok': False, 'error': 'missing_id'}), 400
        todos = sm._load_todos()
        if tid not in todos:
            return jsonify({'ok': False, 'error': 'not_found'}), 404
        t = todos[tid]
        t['status'] = 'claimed'
        t['assigned'] = actor
        t['assigned_at'] = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
        sm._save_todos(todos)
        return jsonify({'ok': True, 'todo': t})
    except Exception as e:
        return jsonify({'ok': False, 'error': 'claim_failed', 'detail': str(e)}), 500


@app.route('/api/controller/complete', methods=['POST'])
def api_controller_complete():
    try:
        body = request.get_json() or {}
        tid = body.get('id')
        actor = body.get('actor') or 'unknown'
        notes = body.get('notes')
        if not tid:
            return jsonify({'ok': False, 'error': 'missing_id'}), 400
        todos = sm._load_todos()
        t = todos.get(tid)
        if not t:
            return jsonify({'ok': False, 'error': 'not_found'}), 404
        # parse tid -> seq_id:step[:sub]
        parts = tid.split(':')
        seq_id = parts[0]
        if len(parts) == 3:
            si = int(parts[1]); sj = int(parts[2])
            ok = sm._mark_todo_done(seq_id, si, sj)
        else:
            si = int(parts[1]); sj = None
            ok = sm._mark_todo_done(seq_id, si, None)
        if not ok:
            return jsonify({'ok': False, 'error': 'mark_failed'}), 500
        # update metadata
        todos = sm._load_todos()
        updated = todos.get(tid)
        if updated is not None:
            updated['completed_by'] = actor
            if notes:
                updated['notes'] = notes
            sm._save_todos(todos)
        # maybe finish sequence
        sm._maybe_finish_sequence(seq_id)
        return jsonify({'ok': True, 'todo': updated})
    except Exception as e:
        return jsonify({'ok': False, 'error': 'complete_failed', 'detail': str(e)}), 500


@app.route('/api/sequences/stream')
def api_sequences_stream():
    def gen():
        last_t_mtime = 0
        last_a_mtime = 0
        todos_path = os.path.join(os.getcwd(), '.tmp', 'sequence_todos.json')
        active_path = os.path.join(os.getcwd(), '.tmp', 'active_task.json')
        while True:
            try:
                if os.path.exists(todos_path):
                    m = os.path.getmtime(todos_path)
                    if m and m != last_t_mtime:
                        last_t_mtime = m
                        try:
                            with open(todos_path, 'r', encoding='utf-8') as f:
                                payload = json.load(f)
                        except Exception:
                            payload = {}
                        yield f"event: todos\n"
                        yield f"data: {json.dumps(payload)}\n\n"
                if os.path.exists(active_path):
                    m = os.path.getmtime(active_path)
                    if m and m != last_a_mtime:
                        last_a_mtime = m
                        try:
                            with open(active_path, 'r', encoding='utf-8') as f:
                                payload = json.load(f)
                        except Exception:
                            payload = {}
                        yield f"event: active\n"
                        yield f"data: {json.dumps(payload)}\n\n"
                yield ':\n\n'
                time.sleep(1)
            except GeneratorExit:
                return
            except Exception:
                time.sleep(1)

    return Response(gen(), mimetype='text/event-stream')


@app.route('/sequences')
def sequences_page():
    return render_template('sequences.html')


@app.route('/api/events/stream')
def api_events_stream():
    """Server-Sent Events endpoint that streams appended lines from `events.ndjson`.
    Each line is emitted as a single SSE `data:` message containing the JSON line.
    """
    def gen():
        # wait until file exists
        last_path = EVENTS_PATH
        while not os.path.exists(last_path):
            # send a heartbeat while waiting
            yield ': heartbeat\n\n'
            time.sleep(0.5)
        try:
            with open(last_path, 'r', encoding='utf-8') as fh:
                # seek to end so we only stream new events
                fh.seek(0, os.SEEK_END)
                while True:
                    line = fh.readline()
                    if not line:
                        # heartbeat to keep connection alive
                        yield ':\n\n'
                        time.sleep(0.5)
                        continue
                        line = line.strip()
                        if not line:
                            continue
                        # try to parse JSON to extract event type and emit named SSE events
                        try:
                            parsed = json.loads(line)
                            ev_type = parsed.get('type') or parsed.get('event') or 'event'
                            # normalize to simple token
                            ev_name = str(ev_type).strip().lower().replace(' ', '-').replace('.', '-')
                            if ev_name == 'instruction':
                                ev_name = 'instruct'
                            # emit named event then data
                            yield f"event: {ev_name}\n"
                            # ensure data is a single-line JSON string
                            safe = json.dumps(parsed, ensure_ascii=False)
                            yield f"data: {safe}\n\n"
                        except Exception:
                            # fallback: emit raw as generic event
                            yield f"data: {line}\n\n"
        except GeneratorExit:
            return
        except Exception:
            # on unexpected error, yield periodic heartbeats
            while True:
                yield ':\n\n'
                time.sleep(1)

    return Response(gen(), mimetype='text/event-stream')


def find_powershell():
    # prefer pwsh, fallback to powershell
    for name in ('pwsh', 'powershell'):
        path = shutil.which(name)
        if path:
            return path
    return None


@app.route('/api/agents/status')
def api_agents_status():
    pid_file = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
    status = {'running': False, 'pids': None}
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            status['pids'] = data
            # determine if any PID is actually running
            try:
                pmap = data.get('pids') if isinstance(data, dict) and 'pids' in data else data
                alive_any = False
                alive_map = {}
                if isinstance(pmap, dict):
                    for k, v in pmap.items():
                        pid = None
                        if isinstance(v, dict):
                            pid = v.get('pid')
                        else:
                            try:
                                pid = int(v)
                            except Exception:
                                pid = None
                        is_alive = False
                        if pid:
                            is_alive = _pid_is_running(pid)
                        alive_map[k] = {'pid': pid, 'alive': is_alive}
                        if is_alive:
                            alive_any = True
                status['alive'] = alive_map
                status['running'] = bool(alive_any)
            except Exception:
                status['running'] = True
        except Exception:
            status['pids'] = None
    return jsonify(status)


def _pid_is_running(pid: int) -> bool:
    """Check whether a process with PID `pid` is running.
    Uses `tasklist` on Windows and `os.kill(pid, 0)` on POSIX.
    """
    try:
        pid = int(pid)
    except Exception:
        return False
    # Windows: use tasklist filter
    if os.name == 'nt':
        try:
            out = subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'], stderr=subprocess.DEVNULL, text=True)
            # tasklist returns a line with the process name and PID when found; when not found it returns a message
            if str(pid) in out and 'No tasks' not in out:
                return True
            return False
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True


@app.route('/api/agents/pids_status')
def api_agents_pids_status():
    """Return the PID map from `.tmp/agents_pids.json` with a per-agent alive flag."""
    pids_path = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
    if not os.path.exists(pids_path):
        return jsonify({'found': False})
    try:
        with open(pids_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        pmap = data.get('pids') if isinstance(data, dict) and 'pids' in data else data
        status = {}
        if isinstance(pmap, dict):
            for k, v in pmap.items():
                pid = None
                if isinstance(v, dict):
                    pid = v.get('pid')
                else:
                    try:
                        pid = int(v)
                    except Exception:
                        pid = None
                alive = False
                # detect whether this entry was recorded as a fallback (log filenames include '.fallback.')
                fallback = False
                try:
                    if isinstance(v, dict):
                        outp = v.get('out') or ''
                        errp = v.get('err') or ''
                        if '.fallback.' in str(outp) or '.fallback.' in str(errp):
                            fallback = True
                except Exception:
                    fallback = False
                if pid:
                    alive = _pid_is_running(pid)
                status[k] = {'pid': pid, 'alive': alive, 'fallback': bool(fallback)}
        return jsonify({'found': True, 'path': pids_path, 'pids': pmap, 'status': status})
    except Exception as e:
        return jsonify({'found': True, 'error': str(e)}), 500


@app.route('/api/agents/out_status')
def api_agents_out_status():
    # common producer output path
    candidates = [os.path.join(os.getcwd(), 'out', 'status.json'), os.path.join(os.getcwd(), 'out', 'status', 'status.json')]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return jsonify({'found': True, 'path': p, 'data': data})
            except Exception as e:
                return jsonify({'found': True, 'path': p, 'error': str(e)}), 500
    return jsonify({'found': False, 'message': 'no out/status.json found'})


def is_capability_blob(obj: dict) -> bool:
    # heuristics: has name and skills or channels
    if not isinstance(obj, dict):
        return False
    if 'name' in obj and ('skills' in obj or 'channels' in obj):
        return True
    return False


@app.route('/api/agents/capabilities')
def api_agents_capabilities():
    # scan repo for json files that look like capability files
    repo_root = os.getcwd()
    matches = []
    for root, dirs, files in os.walk(repo_root):
        # skip .git and virtualenvs
        if '.git' in root or 'venv' in root or '.venv' in root:
            continue
        for fn in files:
            if not fn.lower().endswith('.json'):
                continue
            path = os.path.join(root, fn)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    j = json.load(f)
                if is_capability_blob(j):
                    # summarize
                    summary = {
                        'path': os.path.relpath(path, repo_root),
                        'name': j.get('name'),
                        'version': j.get('version'),
                        'channels': j.get('channels'),
                        'internet_access': j.get('internet_access'),
                        'skills': [s.get('id') if isinstance(s, dict) else s for s in j.get('skills', [])]
                    }
                    matches.append(summary)
            except Exception:
                continue
    return jsonify(matches)


@app.route('/api/agents/summary')
def api_agents_summary():
    """Return a lightweight summary per detected capability/agent.
    Each entry may include: path, name, description, model (if present), mood (from out/status),
    activity scores (events counts for last 1 day and 7 days) and current todo-like tasks.
    """
    repo_root = os.getcwd()
    # reuse capabilities scanning
    caps_resp = api_agents_capabilities()
    try:
        caps = json.loads(caps_resp.get_data(as_text=True))
    except Exception:
        caps = []

    # load recent events (max 2000)
    events = read_last_events(2000)
    now = datetime.now(timezone.utc)
    def parse_ts(ts):
        if not ts:
            return None
        try:
            if isinstance(ts, str) and ts.endswith('Z'):
                return datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return datetime.fromisoformat(ts)
        except Exception:
            return None

    # load out/status.json if present to extract moods or task lists
    out_status = None
    out_candidates = [os.path.join(repo_root, 'out', 'status.json'), os.path.join(repo_root, 'out', 'status', 'status.json')]
    for p in out_candidates:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    out_status = json.load(f)
                break
            except Exception:
                out_status = None

    summaries = []
    def event_matches_cap(e, cap):
        # heuristics to attribute an event to a capability/agent
        name = (cap.get('name') or '').lower()
        path = (cap.get('path') or '').lower()
        filename = os.path.basename(path)
        candidates = []
        for k in ('type', 'source', 'target'):
            v = e.get(k)
            if isinstance(v, str):
                candidates.append(v.lower())
        p = e.get('payload')
        if isinstance(p, str):
            candidates.append(p.lower())
        if isinstance(p, dict):
            for key, val in p.items():
                if isinstance(val, str):
                    candidates.append(val.lower())
            # include JSON repr for fuzzy matches
            try:
                candidates.append(json.dumps(p).lower())
            except Exception:
                pass
        # check configured agents first (aliases/match tokens)
        agents_cfg = load_agents_config()
        if agents_cfg:
            for a in agents_cfg:
                aid = (a.get('id') or '').lower()
                # quick match against capability name or path
                if aid and (aid == name or aid == filename or aid in path):
                    return True
                # aliases and match tokens
                for tok in (a.get('aliases', []) + a.get('match', [])):
                    if not tok:
                        continue
                    for s in candidates:
                        if not s:
                            continue
                        if tok in s:
                            return True
        # fallback: original heuristics
        for s in candidates:
            if not s:
                continue
            if name and name in s:
                return True
            if filename and filename in s:
                return True
        # also check path tokens
        for t in (name, filename, path):
            if not t:
                continue
            for s in candidates:
                if s and t in s:
                    return True
        return False

    for c in caps:
        item = {'path': c.get('path'), 'name': c.get('name') or os.path.basename(c.get('path') or ''), 'version': c.get('version')}
        # read capability for metadata hints
        full = os.path.normpath(os.path.join(repo_root, c.get('path') or ''))
        desc = None
        model = None
        try:
            if os.path.exists(full):
                with open(full, 'r', encoding='utf-8') as f:
                    j = json.load(f)
                desc = j.get('description') or (j.get('meta') or {}).get('description')
                model = j.get('model') or j.get('llm') or (j.get('inference') or {}).get('model')
        except Exception:
            pass
        item['description'] = desc
        item['model'] = model

        # compute activity scores attributed to this capability
        cnt_1d = 0
        cnt_7d = 0
        matched_events = []
        for e in events:
            try:
                if not event_matches_cap(e, c):
                    continue
            except Exception:
                continue
            matched_events.append(e)
            ts = parse_ts(e.get('timestamp') or e.get('time') or '')
            if not ts:
                continue
            delta = now - ts
            if delta <= timedelta(days=1):
                cnt_1d += 1
            if delta <= timedelta(days=7):
                cnt_7d += 1
        item['scores'] = {'1d': cnt_1d, '7d': cnt_7d, 'matched_events': len(matched_events)}

        # mood and todo tasks: prefer structured out/status, then scan matched events
        mood = None
        todos = []
        if isinstance(out_status, dict):
            mood = out_status.get('mood') or out_status.get('state')
            tasks = out_status.get('tasks') or out_status.get('todo') or []
            if isinstance(tasks, list):
                for t in tasks:
                    if isinstance(t, dict):
                        if t.get('status') not in ('done', 'closed', 'completed'):
                            todos.append(t)
                    else:
                        todos.append({'task': t})

        # scan matched events for todo/task-like payloads
        if not todos:
            for e in matched_events:
                t = None
                if e.get('type') in ('todo', 'task', 'task.create', 'todo.create'):
                    t = e.get('payload') or {}
                elif isinstance(e.get('payload'), dict) and any(k in e.get('payload') for k in ('task', 'todo', 'title', 'status')):
                    p = e.get('payload')
                    if 'task' in p and isinstance(p.get('task'), dict):
                        t = p.get('task')
                    elif 'todo' in p and isinstance(p.get('todo'), dict):
                        t = p.get('todo')
                    else:
                        # normalize into a task-like dict
                        t = {'title': p.get('title') or p.get('summary') or None, 'status': p.get('status')}
                if t:
                    # normalize fields we show in UI
                    nt = {'title': t.get('title') or t.get('task') or t.get('summary') or str(t)[:240],
                          'status': t.get('status'),
                          'assignee': t.get('assignee') or t.get('owner')}
                    todos.append(nt)
                    if len(todos) >= 50:
                        break

        item['mood'] = mood
        item['todos'] = todos[:50]
        summaries.append(item)

    return jsonify(summaries)



@app.route('/api/agents/instruct', methods=['POST'])
def api_agents_instruct():
    """Accept a short instruction/message and append it to events.ndjson as an 'instruction' event.
    Expected JSON body: { "message": "text", "target": "agent-id-or-name", "meta": { ... } }
    This is intentionally lightweight for prototyping: the monitor acts as an event producer.
    """
    # auth: if an API key is configured, require it (header X-API-Key or ?api_key=)
    if INSTRUCT_API_KEY:
        got_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not got_key or got_key != INSTRUCT_API_KEY:
            return jsonify({'ok': False, 'error': 'unauthorized'}), 401

    # determine rate-limit key (prefer API key, else client IP)
    rate_key = None
    if INSTRUCT_API_KEY:
        rate_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    else:
        rate_key = request.remote_addr or 'anon'

    if instruct_is_rate_limited(str(rate_key)):
        retry = instruct_rate_retry_after(str(rate_key))
        return jsonify({'ok': False, 'error': 'rate_limited', 'retry_after': retry}), 429, {'Retry-After': str(retry)}

    try:
        body = request.get_json(force=True)
    except Exception:
        return jsonify({'ok': False, 'error': 'invalid json body'}), 400
    if not body or not isinstance(body, dict):
        return jsonify({'ok': False, 'error': 'expected JSON object with message field'}), 400
    message = body.get('message') or body.get('msg')
    if not message or not isinstance(message, str):
        return jsonify({'ok': False, 'error': 'missing or invalid message field'}), 400
    target = body.get('target')
    meta = body.get('meta') or {}

    event = {
        'type': 'instruction',
        'source': 'monitor',
        'target': target,
        'payload': {'message': message, 'meta': meta},
        'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'),
        'trace_id': uuid.uuid4().hex,
    }

    # append to events.ndjson
    try:
        os.makedirs(os.path.dirname(EVENTS_PATH), exist_ok=True)
        with open(EVENTS_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    except Exception as e:
        return jsonify({'ok': False, 'error': 'failed to append event', 'details': str(e)}), 500

    return jsonify({'ok': True, 'path': EVENTS_PATH, 'event': event})


@app.route('/api/agents/config')
def api_agents_config():
    """Return the canonical agents configuration (agents.json) for the UI to render per-agent controls."""
    try:
        cfg = load_agents_config()
        return jsonify({'ok': True, 'agents': cfg})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/agents/capability')
def api_agents_capability():
    # return the full capability JSON content for a given repo-relative path
    path = request.args.get('path')
    if not path:
        return jsonify({'error': 'missing path parameter'}), 400
    repo_root = os.getcwd()
    # normalize and ensure within repo
    full = os.path.normpath(os.path.join(repo_root, path))
    if not full.startswith(repo_root):
        return jsonify({'error': 'invalid path'}), 400
    if not os.path.exists(full):
        return jsonify({'error': 'file not found', 'path': path}), 404
    try:
        with open(full, 'r', encoding='utf-8') as f:
            j = json.load(f)
        return jsonify({'path': path, 'data': j})
    except Exception as e:
        return jsonify({'error': 'failed to read json', 'message': str(e)}), 500


@app.route('/api/agents/log')
def api_agents_log():
    """Serve per-agent logs from .tmp/logs.
    Query params:
      id: agent id (required)
      type: out|err|both (default out)
      lines: number of tail lines to return (default 200)
      download: if '1' will return file as attachment (only for single file)
    """
    aid = request.args.get('id')
    if not aid:
        return jsonify({'ok': False, 'error': 'missing id parameter'}), 400
    # sanitize id (no path traversal)
    if '/' in aid or '\\' in aid or '..' in aid:
        return jsonify({'ok': False, 'error': 'invalid id parameter'}), 400

    typ = (request.args.get('type') or 'out').lower()
    if typ not in ('out', 'err', 'both'):
        typ = 'out'
    try:
        lines = int(request.args.get('lines') or 200)
    except Exception:
        lines = 200
    download = request.args.get('download') == '1'

    log_dir = os.path.join(os.getcwd(), '.tmp', 'logs')
    if not os.path.exists(log_dir):
        return jsonify({'ok': False, 'error': 'no logs directory found'}), 404

    def find_latest(pattern):
        paths = glob.glob(os.path.join(log_dir, pattern))
        if not paths:
            return None
        paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return paths[0]

    candidates = []
    if typ == 'both':
        candidates = [find_latest(f"{aid}*.out.log"), find_latest(f"{aid}*.err.log")]
        candidates = [p for p in candidates if p]
    else:
        candidates = [find_latest(f"{aid}*.{typ}.log")]
        candidates = [p for p in candidates if p]

    if not candidates:
        return jsonify({'ok': False, 'error': 'no logs found for id', 'id': aid}), 404

    # if download and single file, use send_file
    if download and len(candidates) == 1:
        return send_file(candidates[0], as_attachment=True)

    def tail_text(path, n=200):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read().splitlines()
            return '\n'.join(data[-n:])
        except Exception:
            return ''

    result = {'ok': True, 'id': aid, 'files': []}
    for p in candidates:
        kind = 'out' if p.endswith('.out.log') else ('err' if p.endswith('.err.log') else 'log')
        result['files'].append({'path': os.path.relpath(p, os.getcwd()), 'kind': kind, 'tail': tail_text(p, lines)})

    return jsonify(result)


@app.route('/api/agents/log_preview')
def api_agents_log_preview():
    """Lightweight log preview for UI: returns last N lines across out/err files for an agent.
    Query params: id (required), lines (default 200)
    """
    aid = request.args.get('id')
    if not aid:
        return jsonify({'ok': False, 'error': 'missing id parameter'}), 400
    if '/' in aid or '\\' in aid or '..' in aid:
        return jsonify({'ok': False, 'error': 'invalid id parameter'}), 400
    try:
        lines = int(request.args.get('lines') or 200)
    except Exception:
        lines = 200
    log_dir = os.path.join(os.getcwd(), '.tmp', 'logs')
    if not os.path.exists(log_dir):
        return jsonify({'ok': False, 'error': 'no logs directory found'}), 404

    def find_latest(pattern):
        paths = glob.glob(os.path.join(log_dir, pattern))
        if not paths:
            return None
        paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return paths[0]

    candidates = [find_latest(f"{aid}*.out.log"), find_latest(f"{aid}*.err.log")]
    candidates = [p for p in candidates if p]
    if not candidates:
        return jsonify({'ok': False, 'error': 'no logs found for id', 'id': aid}), 404

    def tail_text(path, n=200):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read().splitlines()
            return '\n'.join(data[-n:])
        except Exception:
            return ''

    previews = []
    for p in candidates:
        kind = 'out' if p.endswith('.out.log') else ('err' if p.endswith('.err.log') else 'log')
        previews.append({'path': os.path.relpath(p, os.getcwd()), 'kind': kind, 'tail': tail_text(p, lines)})
    return jsonify({'ok': True, 'id': aid, 'preview': previews})


@app.route('/api/agents/probe')
def api_agents_probe():
    """Immediate probe for a single agent id. Returns stored/latest probe result (and runs a fresh probe).
    Query param: id=agent-id
    """
    aid = request.args.get('id')
    if not aid:
        return jsonify({'ok': False, 'error': 'missing id parameter'}), 400
    # find cfg
    cfg = None
    try:
        for c in load_agents_config():
            if (c.get('id') or '').lower() == aid.lower() or (c.get('name') or '').lower() == aid.lower():
                cfg = c; break
    except Exception:
        cfg = None
    # read pids map
    pids_path = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
    pmap = {}
    if os.path.exists(pids_path):
        try:
            with open(pids_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            pmap = data.get('pids') if isinstance(data, dict) and 'pids' in data else data
        except Exception:
            pmap = {}
    if cfg is None:
        # fallback: try to probe based solely on pids map key
        entry = pmap.get(aid) if isinstance(pmap, dict) else None
        fake_cfg = {'id': aid}
        res = probe_agent_by_cfg(fake_cfg, pmap)
        _save_agent_state(res['id'], res)
        try:
            _STATE_QUEUE.put_nowait(res)
        except Exception:
            pass
        return jsonify({'ok': True, 'probe': res})
    res = probe_agent_by_cfg(cfg, pmap)
    _save_agent_state(res['id'], res)
    try:
        _STATE_QUEUE.put_nowait(res)
    except Exception:
        pass
    return jsonify({'ok': True, 'probe': res})


@app.route('/api/agents/compare')
def api_agents_compare():
    """Return an aligned payload containing a live probe result and the last persisted DB state for an agent.
    Query param: id=agent-id
    """
    aid = request.args.get('id')
    if not aid:
        return jsonify({'ok': False, 'error': 'missing id parameter'}), 400
    # find cfg if present
    cfg = None
    try:
        for c in load_agents_config():
            if (c.get('id') or '').lower() == aid.lower() or (c.get('name') or '').lower() == aid.lower():
                cfg = c; break
    except Exception:
        cfg = None

    # load pids map
    pids_path = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
    pmap = {}
    if os.path.exists(pids_path):
        try:
            with open(pids_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            pmap = data.get('pids') if isinstance(data, dict) and 'pids' in data else data
        except Exception:
            pmap = {}

    # live probe (use probe_agent_by_cfg which falls back on pid map)
    try:
        probe_cfg = cfg if cfg is not None else {'id': aid}
        live = probe_agent_by_cfg(probe_cfg, pmap)
    except Exception:
        live = None

    # persisted
    try:
        persisted = _load_agent_state(aid) or None
    except Exception:
        persisted = None

    return jsonify({'ok': True, 'id': aid, 'live': live, 'persisted': persisted})


@app.route('/api/agents/state')
def api_agents_state():
    # return latest stored state for all configured agents
    cfgs = load_agents_config()
    out = {}
    for c in cfgs:
        aid = c.get('id') or c.get('name')
        if not aid: continue
        st = _load_agent_state(aid)
        out[aid] = st
    return jsonify({'ok': True, 'state': out})


@app.route('/api/agents/state/stream')
def api_agents_state_stream():
    def gen():
        # yield queued state objects as SSE named event 'agent-state'
        while True:
            try:
                st = _STATE_QUEUE.get(timeout=1.0)
                s = json.dumps(st, ensure_ascii=False)
                yield f"event: agent-state\n"
                yield f"data: {s}\n\n"
            except Exception:
                # heartbeat
                yield ':\n\n'
    return Response(gen(), mimetype='text/event-stream')


@app.route('/api/agents/start', methods=['POST'])
def api_agents_start():
    ps = find_powershell()
    if not ps:
        return jsonify({'ok': False, 'error': 'No PowerShell (pwsh/powershell) found on PATH'}), 500
    start_script = os.path.join(os.getcwd(), 'scripts', 'start_agents.ps1')
    if not os.path.exists(start_script):
        return jsonify({'ok': False, 'error': 'start_agents.ps1 not found'}), 404
    # run start script and capture output; script writes .tmp/agents_pids.json
    try:
        # allow optional JSON body: { "id": "agent-id" }
        body = None
        try:
            body = request.get_json(silent=True) or {}
        except Exception:
            body = {}
        agent_id = None
        if isinstance(body, dict):
            agent_id = body.get('id') or body.get('agent')

        # if an agent id was requested, check existing pids for a live instance and refuse to start duplicates
        if agent_id:
            pids_path_check = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
            if os.path.exists(pids_path_check):
                try:
                    with open(pids_path_check, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                    pmap = existing.get('pids') if isinstance(existing, dict) and 'pids' in existing else existing
                    if isinstance(pmap, dict):
                        for k, v in pmap.items():
                            try:
                                if str(k).lower() == str(agent_id).lower():
                                    pid = None
                                    if isinstance(v, dict):
                                        pid = v.get('pid')
                                    else:
                                        try:
                                            pid = int(v)
                                        except Exception:
                                            pid = None
                                    if pid and _pid_is_running(pid):
                                        return jsonify({'ok': False, 'error': 'agent_already_running', 'id': agent_id, 'pid': pid}), 409
                            except Exception:
                                continue
                except Exception:
                    pass

        cmd = [ps, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', start_script]
        if agent_id:
            # pass to script as parameter -AgentId
            cmd += ['-AgentId', str(agent_id)]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, text=True)
        stdout = res.stdout or ''
        stderr = res.stderr or ''
        pids_path = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
        pids = None
        if os.path.exists(pids_path):
            try:
                with open(pids_path, 'r', encoding='utf-8') as f:
                    pids = json.load(f)
            except Exception:
                pids = None
        else:
            # try parse stdout as json
            try:
                pids = json.loads(stdout)
            except Exception:
                pids = None
        return jsonify({'ok': True, 'pids': pids, 'stdout': stdout, 'stderr': stderr})
    except subprocess.TimeoutExpired as e:
        return jsonify({'ok': False, 'error': 'start script timeout', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/agents/pids')
def api_agents_pids():
    pids_path = os.path.join(os.getcwd(), '.tmp', 'agents_pids.json')
    if not os.path.exists(pids_path):
        return jsonify({'found': False})
    try:
        # read with utf-8-sig to tolerate BOMs written by some editors
        with open(pids_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        # normalize response to include `pids` key for UI convenience
        pids = data.get('pids') if isinstance(data, dict) and 'pids' in data else data
        return jsonify({'found': True, 'path': pids_path, 'data': data, 'pids': pids})
    except Exception as e:
        return jsonify({'found': True, 'error': str(e)}), 500


@app.route('/api/agents/stop', methods=['POST'])
def api_agents_stop():
    ps = find_powershell()
    if not ps:
        return jsonify({'ok': False, 'error': 'No PowerShell (pwsh/powershell) found on PATH'}), 500
    stop_script = os.path.join(os.getcwd(), 'scripts', 'stop_agents.ps1')
    if not os.path.exists(stop_script):
        return jsonify({'ok': False, 'error': 'stop_agents.ps1 not found'}), 404
    try:
        # support optional JSON body: { "id": "agent-id" }
        body = None
        try:
            body = request.get_json(silent=True) or {}
        except Exception:
            body = {}
        agent_id = None
        if isinstance(body, dict):
            agent_id = body.get('id') or body.get('agent')

        cmd = [ps, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', stop_script]
        if agent_id:
            cmd += ['-AgentId', str(agent_id)]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate(timeout=30)
        return jsonify({'ok': True, 'stdout': out.decode('utf-8', errors='ignore'), 'stderr': err.decode('utf-8', errors='ignore')})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500



@app.route('/api/service/start', methods=['POST'])
def api_service_start():
    """Start a named service by invoking its .tmp starter script.
    JSON body: { "service": "monitor" }
    Supported services map to .tmp/*.ps1 files.
    """
    body = None
    try:
        body = request.get_json(silent=True) or {}
    except Exception:
        body = {}
    svc = None
    if isinstance(body, dict):
        svc = body.get('service') or body.get('name')
    if not svc:
        return jsonify({'ok': False, 'error': 'missing service name'}), 400
    svc = str(svc)
    # mapping service -> script
    svc_map = {
        'monitor': os.path.join(os.getcwd(), '.tmp', 'start_monitor.ps1'),
        'telegram_bridge': os.path.join(os.getcwd(), '.tmp', 'telegram_bridge_job.ps1'),
        'approval_listener': os.path.join(os.getcwd(), '.tmp', 'approval_job.ps1'),
        'periodic_runner': os.path.join(os.getcwd(), '.tmp', 'periodic_job.ps1'),
        'scheduler': os.path.join(os.getcwd(), '.tmp', 'scheduler_job.ps1')
    }
    script = svc_map.get(svc)
    if not script or not os.path.exists(script):
        return jsonify({'ok': False, 'error': 'service script not found', 'service': svc, 'script': script}), 404
    ps = find_powershell() or 'powershell'
    try:
        subprocess.Popen([ps, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script])
        return jsonify({'ok': True, 'service': svc, 'script': script})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'service': svc}), 500


@app.route('/api/service/stop', methods=['POST'])
def api_service_stop():
    """Stop a named service. Implementation attempts to stop PIDs recorded in .tmp/agents_pids.json
    or, for simple monitor, will attempt to kill monitor PID file monitor_pid.txt in .tmp.
    """
    body = None
    try:
        body = request.get_json(silent=True) or {}
    except Exception:
        body = {}
    svc = None
    if isinstance(body, dict):
        svc = body.get('service') or body.get('name')
    if not svc:
        return jsonify({'ok': False, 'error': 'missing service name'}), 400
    svc = str(svc)
    # simple stop strategies per service
    try:
        if svc == 'monitor':
            # monitor writes a PID file at .tmp/monitor_pid.txt
            pidfile = os.path.join(os.getcwd(), '.tmp', 'monitor_pid.txt')
            if os.path.exists(pidfile):
                try:
                    with open(pidfile, 'r', encoding='utf-8') as f:
                        pid = int(f.read().strip())
                    if _pid_is_running(pid):
                        if os.name == 'nt':
                            subprocess.check_call(['taskkill', '/PID', str(pid), '/F'])
                        else:
                            os.kill(pid, 15)
                        try:
                            os.remove(pidfile)
                        except Exception:
                            pass
                        return jsonify({'ok': True, 'stopped': True, 'pid': pid})
                except Exception as e:
                    return jsonify({'ok': False, 'error': str(e)}), 500
            return jsonify({'ok': True, 'stopped': False, 'message': 'monitor pidfile not found'})

        # for agents and bridge, delegate to stop_agents script when possible
        if svc in ('telegram_bridge', 'approval_listener', 'periodic_runner'):
            stop_script = os.path.join(os.getcwd(), 'scripts', 'stop_agents.ps1')
            if os.path.exists(stop_script):
                ps = find_powershell() or 'powershell'
                # pass AgentId parameter matching service name so stop script removes matching entries
                proc = subprocess.Popen([ps, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', stop_script, '-AgentId', svc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate(timeout=30)
                return jsonify({'ok': True, 'service': svc, 'stdout': out.decode('utf-8', errors='ignore'), 'stderr': err.decode('utf-8', errors='ignore')})
            return jsonify({'ok': False, 'error': 'stop script not found'}), 404

        # scheduler: try to find running scheduler_job.ps1 starter and no-op (user can stop job via powershell jobs)
        if svc == 'scheduler':
            # best-effort: clear start_immediately flags in .tmp/schedule.json so scheduler won't restart
            sched = os.path.join(os.getcwd(), '.tmp', 'schedule.json')
            if os.path.exists(sched):
                try:
                    with open(sched, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    changed = False
                    for e in data:
                        if e.get('service') == 'scheduler' and e.get('start_immediately'):
                            e['start_immediately'] = False; changed = True
                    if changed:
                        with open(sched, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2)
                        return jsonify({'ok': True, 'updated_schedule': True})
                except Exception as e:
                    return jsonify({'ok': False, 'error': str(e)}), 500
            return jsonify({'ok': True, 'updated_schedule': False, 'message': 'no schedule file or no changes'})

        return jsonify({'ok': False, 'error': 'no stop strategy for service', 'service': svc}), 400
    except subprocess.TimeoutExpired as e:
        return jsonify({'ok': False, 'error': 'timeout', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)
