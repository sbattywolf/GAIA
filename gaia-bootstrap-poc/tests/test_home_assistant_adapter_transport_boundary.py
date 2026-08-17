from __future__ import annotations

import pytest

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.home.models import HomeResourceReference, ObservationState


REFERENCE = HomeResourceReference("binary_sensor.example_opening")


class RaisingTransport:
    def get_state(self, entity_id):
        assert entity_id == REFERENCE.value
        raise TimeoutError("simulated Home Assistant transport timeout")


class PayloadTransport:
    def __init__(self, payload):
        self.payload = payload

    def get_state(self, entity_id):
        assert entity_id == REFERENCE.value
        return self.payload


def make_adapter(transport):
    return ExperimentalHomeAssistantAdapter(
        transport,
        {
            "on": ObservationState.OPEN,
            "off": ObservationState.CLOSED,
            "unavailable": ObservationState.UNAVAILABLE,
        },
    )


def test_transport_exception_is_not_converted_to_success():
    with pytest.raises(TimeoutError, match="simulated Home Assistant transport timeout"):
        make_adapter(RaisingTransport()).get_opening_state(REFERENCE)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        "not-an-object",
        42,
    ],
)
def test_non_object_transport_payload_is_rejected(payload):
    with pytest.raises(ValueError, match="response is not an object"):
        make_adapter(PayloadTransport(payload)).get_opening_state(REFERENCE)


def test_missing_source_state_is_rejected():
    payload = {
        "entity_id": REFERENCE.value,
        "last_updated": "2026-08-17T18:30:00+00:00",
    }

    with pytest.raises(ValueError, match="invalid state"):
        make_adapter(PayloadTransport(payload)).get_opening_state(REFERENCE)
