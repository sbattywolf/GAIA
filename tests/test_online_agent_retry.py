import requests
from scripts import online_agent


def test_request_with_retry_success_after_transient_errors(monkeypatch):
    calls = {"count": 0}

    class DummyResp:
        def __init__(self, status=200, text="ok", json_data=None):
            self.status_code = status
            self.text = text
            self._json = json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(f"HTTP {self.status_code}")

        def json(self):
            if self._json is None:
                raise ValueError("no json")
            return self._json

    def fake_post(url, json=None, headers=None, timeout=None):
        calls["count"] += 1
        # fail first two calls with server error, succeed on third
        if calls["count"] < 3:
            return DummyResp(status=500, text="server error", json_data=None)
        return DummyResp(status=200, json_data={"ok": True})

    monkeypatch.setattr(online_agent.requests, "post", fake_post)

    res = online_agent.request_with_retry("post", "https://example.local", json_payload={"a": 1}, max_retries=4)

    assert isinstance(res, dict)
    assert res.get("ok") is True
    assert calls["count"] == 3
