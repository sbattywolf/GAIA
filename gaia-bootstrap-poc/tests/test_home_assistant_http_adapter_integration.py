from __future__ import annotations

import json
from pathlib import Path

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.adapters.home_assistant_http_transport import HomeAssistantHTTPTransport
from gaia.home.models import HomeResourceReference, ObservationState


FIXTURE = Path(__file__).parent / "fixtures" / "home_assistant" / "opening_on.json"


def test_adapter_uses_http_transport_without_changing_provider_contract(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(payload).encode("utf-8")

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["authorization"] = request.get_header("Authorization")
        return FakeResponse()

    monkeypatch.setattr(
        "gaia.adapters.home_assistant_http_transport.urlopen",
        fake_urlopen,
    )

    transport = HomeAssistantHTTPTransport(
        "http://home-assistant.example",
        "runtime-token",
        timeout=2.0,
    )
    adapter = ExperimentalHomeAssistantAdapter(
        transport,
        {
            "on": ObservationState.OPEN,
            "off": ObservationState.CLOSED,
            "unavailable": ObservationState.UNAVAILABLE,
        },
    )

    reference = HomeResourceReference(payload["entity_id"])
    observation = adapter.get_opening_state(reference)

    assert observation.resource_reference == reference
    assert observation.state is ObservationState.OPEN
    assert captured["url"].endswith("/api/states/binary_sensor.example_opening")
    assert captured["timeout"] == 2.0
    assert captured["authorization"] == "Bearer runtime-token"
