import json
import os
import subprocess
import sys
from typing import Optional
from . import db
import datetime
import tempfile
import time
import math

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
AGENTS_JSON = os.path.join(ROOT, 'agents.json')
PIDS_FILE = os.path.join(ROOT, '.tmp', 'agents_pids.json')


def _load_agents():
    try:
        with open(AGENTS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def _ensure_tmp():
    p = os.path.join(ROOT, '.tmp')
    os.makedirs(p, exist_ok=True)
    return p


def list_agents():
    agents = _load_agents()
    for a in agents:
        print(a.get('id') or a.get('name'))
    return 0


def _read_pids():
    # tolerate short races where the pids file is being written
    attempts = 3
    delay = 0.05
    for i in range(attempts):
        try:
            with open(PIDS_FILE, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                # normalize shape to dict
                if isinstance(data, dict) and 'pids' in data:
                    return data.get('pids') or {}
                if isinstance(data, dict):
                    return data
                return {}
        except Exception:
            time.sleep(delay)
            delay *= 2
    return {}


def _pid_is_running(pid: int) -> bool:
    try:
        pid = int(pid)
    except Exception:
        return False
    if os.name == 'nt':
        try:
            out = subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'], stderr=subprocess.DEVNULL, text=True)
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


def _append_event(evt):
    # Append an NDJSON event to the repo-level events.ndjson
    try:
        events_file = os.path.join(ROOT, 'events.ndjson')
        with open(events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, default=str) + '\n')
    except Exception:
        pass


def _trace(action, agent_id=None, status=None, details=None):
    try:
        db.write_trace(action=action, agent_id=agent_id, status=status, details=details)
    except Exception:
        pass


def _write_pids(d):
    _ensure_tmp()
    # write atomically
    fd, tmp = tempfile.mkstemp(prefix='agents_pids_', suffix='.json', dir=os.path.join(ROOT, '.tmp'))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump({'pids': d}, f, indent=2)
        os.replace(tmp, PIDS_FILE)
    except Exception:
        try:
            if os.path.exists(tmp): os.remove(tmp)
        except Exception:
            pass


def _retry_run(cmd, timeout=60, attempts=3, backoff=0.5):
    """Run a subprocess with simple retry/backoff on transient failures.

    Returns subprocess.CompletedProcess on success or raises the last exception.
    """
    last_exc = None
    for n in range(1, attempts + 1):
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, text=True)
            return proc
        except subprocess.TimeoutExpired as e:
            last_exc = e
            _append_event({'type': 'agent.subproc.timeout', 'cmd': cmd, 'attempt': n, 'timeout': timeout, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'})
        except Exception as e:
            last_exc = e
            _append_event({'type': 'agent.subproc.error', 'cmd': cmd, 'attempt': n, 'error': str(e), 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'})
        # backoff before retrying
        if n < attempts:
            time.sleep(backoff * (2 ** (n - 1)))
    # exhausted
    if last_exc:
        raise last_exc


def start_agent(agent_id: Optional[str]):
    agents = _load_agents()
    target = None
    for a in agents:
        if a.get('id') == agent_id or a.get('name') == agent_id:
            target = a
            break
    if not target:
        print('Agent not found:', agent_id)
        return 2

    # check existing pids for single-instance enforcement
    existing = _read_pids()
    if existing and isinstance(existing, dict):
        ent = existing.get(agent_id) or existing.get(agent_id.lower())
        try:
            pid = ent.get('pid') if isinstance(ent, dict) else int(ent)
        except Exception:
            pid = None
        if pid:
            # basic liveness check
            if _pid_is_running(pid):
                _append_event({'type': 'agent.start.skipped', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'reason': 'already_running', 'pid': pid})
                _trace('start', agent_id=agent_id, status='skipped', details={'pid': pid})
                print(f'Agent {agent_id} already running as pid {pid} - skipping start')
                return 4

    # Use existing start script wrapper
    script = os.path.join(ROOT, 'scripts', 'start_agents.ps1')
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script, '-AgentId', agent_id]
    print('Starting agent via:', ' '.join(cmd))
    try:
        proc = _retry_run(cmd, timeout=60, attempts=3, backoff=0.5)
        stdout = proc.stdout or ''
        stderr = proc.stderr or ''
        # attempt to read updated pids file
        time.sleep(0.5)
        pids = _read_pids()
        _append_event({'type': 'agent.start', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'pids': pids, 'stdout': stdout[:4000], 'stderr': stderr[:4000]})
        if proc.returncode == 0:
            _trace('start', agent_id=agent_id, status='started', details={'pids': pids})
            return 0
        else:
            _trace('start', agent_id=agent_id, status='failed', details={'returncode': proc.returncode, 'stderr': stderr})
            return 3
    except subprocess.TimeoutExpired as e:
        _append_event({'type': 'agent.start.timeout', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'details': str(e)})
        _trace('start', agent_id=agent_id, status='timeout', details={'error': str(e)})
        return 5
    except Exception as e:
        _append_event({'type': 'agent.start.error', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'details': str(e)})
        _trace('start', agent_id=agent_id, status='error', details={'error': str(e)})
        return 6


def stop_agent(agent_id: Optional[str]):
    script = os.path.join(ROOT, 'scripts', 'stop_agents.ps1')
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script, '-AgentId', agent_id]
    print('Stopping agent via:', ' '.join(cmd))
    try:
        proc = _retry_run(cmd, timeout=60, attempts=3, backoff=0.5)
        stdout = proc.stdout or ''
        stderr = proc.stderr or ''
        # best-effort: remove entry from pid map if it's gone
        time.sleep(0.3)
        pids = _read_pids()
        # if removed, record stop event
        _append_event({'type': 'agent.stop', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'pids': pids, 'stdout': stdout[:4000], 'stderr': stderr[:4000]})
        _trace('stop', agent_id=agent_id, status='stopped', details={'pids': pids})
        return 0
    except subprocess.TimeoutExpired as e:
        _append_event({'type': 'agent.stop.timeout', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'details': str(e)})
        _trace('stop', agent_id=agent_id, status='timeout', details={'error': str(e)})
        return 5
    except subprocess.CalledProcessError as e:
        _append_event({'type': 'agent.stop.failure', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'error': str(e)})
        _trace('stop', agent_id=agent_id, status='failed', details={'error': str(e)})
        return 3
    except Exception as e:
        _append_event({'type': 'agent.stop.error', 'agent_id': agent_id, 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'details': str(e)})
        _trace('stop', agent_id=agent_id, status='error', details={'error': str(e)})
        return 6


def status():
    pids = _read_pids()
    print('Agent PIDs:', json.dumps(pids, indent=2))
    return 0


def handle(action: str, agent_id: Optional[str] = None):
    if action == 'list':
        return list_agents()
    if action == 'start':
        return start_agent(agent_id)
    if action == 'stop':
        return stop_agent(agent_id)
    if action == 'status':
        return status()
    if action == 'probe':
        return probe(agent_id)
    print('Unknown action')
    return 1


def probe(agent_id: Optional[str]):
    # Simple probe: check pid file and log file
    pids = _read_pids()
    entry = pids.get(agent_id)
    if not entry:
        print('No pid entry for', agent_id)
        return 2
    pid = entry.get('pid')
    print('Agent', agent_id, 'pid', pid)
    return 0


def monitor_action(action: str):
    if action == 'status':
        return status()
    if action == 'stream':
        print('Stream not implemented in CLI; use the web UI')
        return 0
    return 1
