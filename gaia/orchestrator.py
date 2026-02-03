"""Orchestrator for a simple dry-run -> apply flow with approval checkpoints recorded to `gaia.db`.

Usage:
  from gaia import orchestrator
  orchestrator.run_sequence(auto_approve=False)

Behavior:
- Performs installer dry-run (via `gaia.installer`), records a checkpoint `dryrun_complete`.
- If `auto_approve` is False, records `approval_required` and exits with code 2.
- If `auto_approve` is True, proceeds to apply, records `apply_complete` or `apply_failed`.
"""
from . import installer, db, events, alerts
import os
import datetime
import time


def _ts():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def run_sequence(venv_path='.venv', requirements='requirements.txt', allow_system=False, auto_approve=False):
    trace_id = None
    # 1) Dry-run
    db.write_trace(action='orchestrator.start', status='running', details={'venv': venv_path, 'requirements': requirements})
    # installer.run_apply with apply=False (dry-run)
    rc = installer.run_apply(apply=False, venv_path=venv_path, requirements=requirements, allow_system=allow_system)
    db.write_trace(action='orchestrator.dryrun_complete', status='ok' if rc == 0 else 'failed', details={'rc': rc})
    events.append_event({'type': 'orchestrator.dryrun', 'payload': {'rc': rc, 'venv': venv_path, 'requirements': requirements}, 'timestamp': _ts()})

    if rc != 0:
        db.write_trace(action='orchestrator.halt', status='dryrun_failed', details={'rc': rc})
        return 3

    # 2) Approval checkpoint
    db.write_trace(action='orchestrator.approval_required', status='pending', details={'auto_approve': bool(auto_approve)})
    events.append_event({'type': 'orchestrator.approval_required', 'payload': {'auto_approve': auto_approve}, 'timestamp': _ts()})

    approval_file = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'approval.json')
    approval_file = os.path.normpath(approval_file)

    if not auto_approve:
        # send Telegram approval request
        try:
            msg = 'GAIA: dry-run complete. Reply APPROVE in the bot chat to allow apply (expires in 30m).'
            alerts.send_telegram(message=msg)
        except Exception:
            pass

        # wait for approval file written by approval_listener_runner
        wait_until = time.time() + 30 * 60
        while time.time() < wait_until:
            try:
                if os.path.exists(approval_file):
                    with open(approval_file, 'r', encoding='utf-8') as f:
                        apr = f.read().strip()
                    if apr:
                        db.write_trace(action='orchestrator.approval_observed', status='ok', details={'file': approval_file})
                        events.append_event({'type': 'orchestrator.approval_observed', 'payload': {'file': approval_file}, 'timestamp': _ts()})
                        break
            except Exception:
                pass
            time.sleep(5)
        else:
            db.write_trace(action='orchestrator.approval_timeout', status='timeout')
            events.append_event({'type': 'orchestrator.approval_timeout', 'payload': {}, 'timestamp': _ts()})
            return 2

    # 3) Apply
    db.write_trace(action='orchestrator.apply.start', status='running')
    rc2 = installer.run_apply(apply=True, venv_path=venv_path, requirements=requirements, allow_system=allow_system)
    if rc2 == 0:
        db.write_trace(action='orchestrator.apply.complete', status='ok')
        events.append_event({'type': 'orchestrator.apply.complete', 'payload': {'rc': rc2}, 'timestamp': _ts()})
        return 0
    else:
        db.write_trace(action='orchestrator.apply.failed', status='failed', details={'rc': rc2})
        events.append_event({'type': 'orchestrator.apply.failed', 'payload': {'rc': rc2}, 'timestamp': _ts()})
        return 4
