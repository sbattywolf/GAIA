import requests


def test_classify_httperror_429_transient():
    import scripts.process_telegram_queue as prq

    class DummyResp:
        def __init__(self, status_code):
            self.status_code = status_code

    http_err = requests.exceptions.HTTPError('429 Too Many Requests')
    http_err.response = DummyResp(429)

    assert prq._classify_exception(http_err) == 'transient'


def test_classify_httperror_500_transient():
    import scripts.process_telegram_queue as prq

    class DummyResp:
        def __init__(self, status_code):
            self.status_code = status_code

    http_err = requests.exceptions.HTTPError('500 Server Error')
    http_err.response = DummyResp(500)

    assert prq._classify_exception(http_err) == 'transient'
