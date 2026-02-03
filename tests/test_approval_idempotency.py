import pytest

import scripts.telegram_queue as tq


def test_idempotent_enqueue(tmp_path, monkeypatch):
    qpath = tmp_path / 'telegram_queue.json'
    seen = tmp_path / 'telegram_queue_seen.json'
    monkeypatch.setattr(tq, 'Q_PATH', qpath)
    monkeypatch.setattr(tq, 'SEEN_PATH', seen)

    update = {
        'update_id': 3001,
        'callback_query': {
            'id': 'cq1',
            'data': 'approve:abc123',
            'from': {'id': 10},
        },
    }

    assert tq.append_dedup(update) is True
    # replayed identical update should not be appended
    assert tq.append_dedup(dict(update)) is False

    # processing the queue yields exactly one item
    first = tq.pop_next()
    assert first is not None and first.get('update_id') == 3001
    assert tq.pop_next() is None
