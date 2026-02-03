import json
import requests


def test_retry_worker_handles_requests_http_error(tmp_path, monkeypatch):
    import scripts.process_telegram_queue as prq
    import scripts.telegram_client as tc

    # prepare failed file with one answer_callback item
    failed_item = {'action': 'answer_callback', 'callback_query_id': 'cb-httperr', 'update': {'update_id': 201}, '_retries': 0}
    prq.FAILED_FILE.parent.mkdir(parents=True, exist_ok=True)
    prq.FAILED_FILE.write_text(json.dumps([failed_item], indent=2), encoding='utf-8')

    # craft a requests HTTPError with response.status_code = 400
    class DummyResp:
        def __init__(self, status_code):
            self.status_code = status_code

    http_err = requests.exceptions.HTTPError('400 Client Error')
    http_err.response = DummyResp(400)

    def fake_answer(token, cqid, text=None, show_alert=False, timeout=6):
        raise http_err

    monkeypatch.setattr(tc, 'answer_callback', fake_answer)

    out = prq.process_failed_items_once()
    assert out['processed'] == 1
    assert out['succeeded'] == 0
    assert out['moved_permanent'] == 1

    perm = json.loads(prq.PERM_FAILED_FILE.read_text(encoding='utf-8') or '[]')
    assert len(perm) == 1
    assert perm[0].get('callback_query_id') == 'cb-httperr'
