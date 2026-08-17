from __future__ import annotations

import json
from types import SimpleNamespace
from urllib.error import HTTPError

import pytest

from gaia.adapters.home_assistant_http_transport import HomeAssistantHTTPTransport


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def test_transport_builds_bounded_state_request(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse(
            {
                "entity_id": "binary_sensor.example_opening",
                "state": "on",
                "last_updated": "2026-08-17T18:30:00+00:00",
            }
        )

    monkeypatch.setattr(
        "gaia.adapters.home_assistant_http_transport.urlopen",
        fake_urlopen,
    )

    transport = HomeAssistantHTTPTransport(
        "http://home-assistant.example",
        "runtime-token",
        timeout=3.5,
    )

    payload = transport.get_state("binary_sensor.example_opening")

    assert payload["state"] == "on"
    assert captured["request"].full_url == (
        "http://home-assistant.example/api/states/"
        "binary_sensor.example%2Eopening"
    )
    assert captured["request"].get_method() == "GET"
    assert captured["request"].get_header("Authorization") == "Bearer runtime-token"
    assert captured["request"].get_header("Accept") == "application/json"
    assert captured["timeout"] == 3.5


def test_transport_propagates_http_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr(
        "gaia.adapters.home_assistant_http_transport.urlopen",
        fake_urlopen,
    )

    transport = HomeAssistantHTTPTransport(
        "http://home-assistant.example",
        "runtime-token",
    )

    with pytest.raises(HTTPError, match="Unauthorized"):
        transport.get_state("binary_sensor.example_opening")


@pytest.mark.parametrize("payload", [None, [], "invalid"])
def test_transport_rejects_non_object_json(monkeypatch, payload):
    monkeypatch.setattr(
        "gaia.adapters.home_assistant_http_transport.urlopen",
        lambda request, timeout: FakeResponse(payload),
    )

    transport = HomeAssistantHTTPTransport(
        "http://home-assistant.example",
        "runtime-token",
    )

    with pytest.raises(ValueError, match="response is not an object"):
        transport.get_state("binary_sensor.example_opening")
