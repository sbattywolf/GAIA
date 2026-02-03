import json
from pathlib import Path

import pytest

import scripts.telegram_queue as tq


def test_append_and_pop(tmp_path, monkeypatch):
    qpath = tmp_path / 'telegram_queue.json'
    seen = tmp_path / 'telegram_queue_seen.json'
    monkeypatch.setattr(tq, 'Q_PATH', qpath)
    monkeypatch.setattr(tq, 'SEEN_PATH', seen)

    update = {'update_id': 1001, 'message': {'text': 'hello'}}
    # first append should succeed
    assert tq.append_dedup(update) is True
    # duplicate append should be rejected
    assert tq.append_dedup(update) is False

    lst = tq.list_queue()
    assert isinstance(lst, list) and len(lst) == 1

    popped = tq.pop_next()
    assert popped is not None and popped.get('update_id') == 1001
    # queue is now empty
    assert tq.pop_next() is None


def test_dedupe_by_update_id(tmp_path, monkeypatch):
    qpath = tmp_path / 'telegram_queue.json'
    seen = tmp_path / 'telegram_queue_seen.json'
    monkeypatch.setattr(tq, 'Q_PATH', qpath)
    monkeypatch.setattr(tq, 'SEEN_PATH', seen)

    u1 = {'update_id': 2001}
    u2 = {'update_id': '2001'}  # different type but same numeric id

    assert tq.append_dedup(u1) is True
    # second append should be considered duplicate
    assert tq.append_dedup(u2) is False
    assert len(tq.list_queue()) == 1
