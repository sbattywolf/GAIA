import json
import tempfile
import shutil
import os
from pathlib import Path


def make_pending_item(id_='t1', command='echo hi', exec_request=True, status='pending', created=None):
    return {
        'id': id_,
        'chat_id': 'test_chat',
        'message_id': 'm1',
        'command': command,
        'from': {'first_name': 'UnitTester'},
        'status': status,
        'created': created or '2026-02-03T00:00:00Z',
        'options': {'exec_request': bool(exec_request)}
    }


def run_checks():
    root = Path(__file__).resolve().parents[1]
    tmpdir = Path(tempfile.mkdtemp(prefix='gaia-test-'))
    try:
        pending_path = tmpdir / 'pending_commands.json'
        # test approve + execute dry-run
        item = make_pending_item(id_='t-approve-1')
        pending_path.write_text(json.dumps([item], indent=2), encoding='utf-8')
        import importlib
        tcm = importlib.import_module('scripts.tg_command_manager')
        # monkeypatch PENDING path
        tcm.PENDING = pending_path

        print('-> Approving t-approve-1')
        res = tcm.approve('t-approve-1', actor='unit-test')
        assert res is not None and res.get('status') == 'approved'
        print(' ok approved')

        print('-> Executing dry-run t-approve-1')
        target, err = tcm.execute('t-approve-1', dry_run=True)
        assert err is None and target is not None and target.get('status') == 'executed_dryrun'
        print(' ok executed_dryrun')

        # test toggle_option
        item2 = make_pending_item(id_='t-toggle-1', exec_request=False)
        pending_path.write_text(json.dumps([item2], indent=2), encoding='utf-8')
        tcm.PENDING = pending_path
        print('-> Toggling is_test for t-toggle-1')
        opts = tcm.toggle_option('t-toggle-1', 'is_test', actor='unit')
        assert opts is not None and opts.get('is_test') is True
        print(' ok toggled is_test')

        print('\nAll checks passed')
        return 0
    except AssertionError as e:
        print('Assertion failed:', e)
        return 2
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 3
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass


if __name__ == '__main__':
    raise SystemExit(run_checks())
