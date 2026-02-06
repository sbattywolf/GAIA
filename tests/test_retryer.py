import time
import pytest

from agents.retryer import retry, RetryError


class HTTPError(Exception):
    def __init__(self, status_code, msg=''):
        super().__init__(msg)
        self.status_code = status_code


def test_retry_succeeds_after_retries(monkeypatch):
    calls = {'count': 0}
    sleeps = []

    def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(time, 'sleep', fake_sleep)

    @retry(max_attempts=4, initial_delay=0.1, backoff=2.0, retry_on_exceptions=(HTTPError,))
    def flaky():
        calls['count'] += 1
        if calls['count'] < 3:
            raise HTTPError(429, 'rate limit')
        return 'ok'

    res = flaky()
    assert res == 'ok'
    assert calls['count'] == 3
    # expected sleeps: 0.1, 0.2 (two retries before success)
    assert pytest.approx(sleeps) == [0.1, 0.2]


def test_retry_fails_on_non_retryable_status(monkeypatch):
    sleeps = []
    monkeypatch.setattr(time, 'sleep', lambda s: sleeps.append(s))

    @retry(max_attempts=3, initial_delay=0.01, backoff=2.0, retry_on_exceptions=(HTTPError,))
    def bad():
        # 400 is not retryable per default retry_statuses
        raise HTTPError(400, 'bad request')

    with pytest.raises(Exception):
        bad()
    # should not sleep because status is non-retryable
    assert sleeps == []


def test_retry_raises_retryerror_after_exhaustion(monkeypatch):
    sleeps = []
    monkeypatch.setattr(time, 'sleep', lambda s: sleeps.append(s))

    @retry(max_attempts=2, initial_delay=0.05, backoff=2.0, retry_on_exceptions=(Exception,))
    def always_fail():
        raise Exception('boom')

    with pytest.raises(RetryError):
        always_fail()
    # one sleep should have occurred between attempts
    assert len(sleeps) == 1
