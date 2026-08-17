from datetime import UTC

import pytest

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.home.models import HomeResourceReference, ObservationState


class FakeTransport:
    def __init__(self, payload):
        self.payload = payload
        self.requested_entity = None

    def get_state(self, entity_id):
        self.requested_entity = entity_id
        return self.payload


def test_adapter_reads_one_already_resolved_entity():
    reference = HomeResourceReference("binary_sensor.kitchen_window")
    transport = FakeTransport(
        {
            "entity_id": "binary_sensor.kitchen_window",
            "state": "on",
            "last_updated": "2026-08-17T18:30:00+00:00",
            "attributes": {"device_class": "opening"},
        }
    )

    adapter = ExperimentalHomeAssistantAdapter(
        transport,
        {"on": ObservationState.OPEN, "off": ObservationState.CLOSED},
    )

    observation = adapter.get_opening_state(reference)

    assert transport.requested_entity == reference.value
    assert observation.resource_reference == reference
    assert observation.state is ObservationState.OPEN
    assert observation.observed_at.tzinfo is UTC


def test_adapter_rejects_unmapped_source_state():
    reference = HomeResourceReference("binary_sensor.kitchen_window")
    transport = FakeTransport(
        {
            "entity_id": reference.value,
            "state": "unknown",
            "last_updated": "2026-08-17T18:30:00+00:00",
        }
    )

    adapter = ExperimentalHomeAssistantAdapter(
        transport,
        {"on": ObservationState.OPEN, "off": ObservationState.CLOSED},
    )

    with pytest.raises(ValueError, match="unmapped Home Assistant state"):
        adapter.get_opening_state(reference)


def test_adapter_rejects_mismatched_entity():
    reference = HomeResourceReference("binary_sensor.kitchen_window")
    transport = FakeTransport(
        {
            "entity_id": "binary_sensor.other_window",
            "state": "on",
            "last_updated": "2026-08-17T18:30:00+00:00",
        }
    )

    adapter = ExperimentalHomeAssistantAdapter(
        transport,
        {"on": ObservationState.OPEN, "off": ObservationState.CLOSED},
    )

    with pytest.raises(ValueError, match="mismatched entity_id"):
        adapter.get_opening_state(reference)


def test_adapter_rejects_missing_or_naive_timestamp():
    reference = HomeResourceReference("binary_sensor.kitchen_window")
    transport = FakeTransport(
        {
            "entity_id": reference.value,
            "state": "off",
            "last_updated": "2026-08-17T18:30:00",
        }
    )

    adapter = ExperimentalHomeAssistantAdapter(
        transport,
        {"on": ObservationState.OPEN, "off": ObservationState.CLOSED},
    )

    with pytest.raises(ValueError, match="timezone-aware"):
        adapter.get_opening_state(reference)
