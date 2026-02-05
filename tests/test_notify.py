import importlib.util
import pathlib
import time
import os


spec = importlib.util.spec_from_file_location('notify', pathlib.Path('scripts/notify.py').resolve())
notify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notify)


def test_fmt_message_contains_fields():
    msg = notify.fmt_message('unit-agent', 'running', 'doing work', metrics={'a': 1})
    assert 'Agent: unit-agent' in msg
    assert 'Status: running' in msg
    assert 'Summary: doing work' in msg
    assert 'a: 1' in msg


def test_throttle_should_send():
    # ensure .tmp exists and remove sent file
    sf = pathlib.Path(' .tmp').resolve() if False else pathlib.Path('.tmp')
    sf.mkdir(exist_ok=True)
    sent = sf / 'notify_sent.json'
    try:
        if sent.exists():
            sent.unlink()
    except Exception:
        pass

    # first call should allow send
    ok1 = notify.should_send_now('test-key', min_interval=2)
    assert ok1 is True
    notify.record_send('test-key')
    # immediate second should be throttled
    ok2 = notify.should_send_now('test-key', min_interval=2)
    assert ok2 is False
    # after waiting it should be allowed
    time.sleep(2)
    ok3 = notify.should_send_now('test-key', min_interval=2)
    assert ok3 is True
