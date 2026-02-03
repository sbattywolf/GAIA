import os
import json
from pathlib import Path
from datetime import datetime, timezone

import scripts.auto_requeue as auto_requeue
import scripts.process_telegram_queue as prq
from gaia import db as gaia_db


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp'


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return []


def test_admin_requeue_and_retry(tmp_path):
    # prepare permanent-failed with an eligible item
    perm_file = TMP / 'telegram_queue_failed_permanent.json'
    failed_file = TMP / 'telegram_queue_failed.json'
    # clear any previous state
    if perm_file.exists():
        perm_file.unlink()
    if failed_file.exists():
        failed_file.unlink()

    item = {
        'action': 'send_message',
        'chat_id': 999999,
        'text': 'requeue-test',
        '_retries': 0,
        '_failed_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    write_json(perm_file, [item])

    # run auto_requeue (admin-like action)
    out = auto_requeue.run(dry_run=False)
    assert out['requeued'] == 1

    # ensure requeued item is now in failed file
    failed = read_json(failed_file)
    assert len(failed) >= 1

    # set a token so _perform_action proceeds and monkeypatch telegram_client.send_message
    os.environ['TELEGRAM_BOT_TOKEN'] = 'fake-token'

    # monkeypatch: avoid network calls by replacing the send_message function
    import scripts.telegram_client as tc

    calls = []

    def fake_send_message(token, chat_id, text, reply_to_message_id=None, **kwargs):
        calls.append({'token': token, 'chat_id': chat_id, 'text': text})
        return {'ok': True}

    tc.send_message = fake_send_message

    # run the retry worker once
    res = prq.process_failed_items_once()
    assert res['processed'] >= 1
    # expect at least one succeeded
    assert res['succeeded'] >= 1

    # verify an outbound send was invoked
    assert len(calls) >= 1

    # verify audit traces were written to gaia.db
    traces = gaia_db.tail_traces(100)
    # there should be at least one retry attempt trace and one success trace
    actions = [t.get('action') for t in traces]
    assert any(a and a.startswith('telegram.retry') for a in actions), f"no retry traces found in {actions}"

    # cleanup
    try:
        perm_file.unlink()
    except Exception:
        pass
    try:
        failed_file.unlink()
    except Exception:
        pass
