import json
from agents import agent_utils


def test_idempotency_key_consistent():
    payload = {'a': 1, 'b': 2}
    k1 = agent_utils.idempotency_key('src', payload)
    k2 = agent_utils.idempotency_key('src', {'b': 2, 'a': 1})
    assert k1 == k2
    assert isinstance(k1, str) and len(k1) == 32


def test_retry_with_backoff_success(monkeypatch):
    calls = {'n': 0}

    def fn():
        calls['n'] += 1
        if calls['n'] < 2:
            raise ValueError('temp')
        return 'ok'

    # inject no-op sleep
    res = agent_utils.retry_with_backoff(fn, retries=3, base_backoff=0.0, sleep=lambda s: None)
    assert res == 'ok'
    assert calls['n'] == 2


def test_retry_with_backoff_fail(monkeypatch):
    def fn():
        raise RuntimeError('boom')

    try:
        agent_utils.retry_with_backoff(fn, retries=2, base_backoff=0.0, sleep=lambda s: None)
    except RuntimeError as e:
        assert 'boom' in str(e)
    else:
        raise AssertionError('should have raised')
