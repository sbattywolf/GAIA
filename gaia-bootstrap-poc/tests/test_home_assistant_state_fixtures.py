from __future__ import annotations

import json
from pathlib import Path

import pytest

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.home.models import HomeResourceReference, ObservationState


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "home_assistant"
REFERENCE = HomeResourceReference("binary_sensor.example_opening")


class FixtureTransport:
    def __init__(self, payload):
        self.payload = payload

    def get_state(self, entity_id):
        assert entity_id == REFERENCE.value
        return self.payload


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def make_adapter(payload: dict) -> ExperimentalHomeAssistantAdapter:
    return ExperimentalHomeAssistantAdapter(
        FixtureTransport(payload),
        {
            "on": ObservationState.OPEN,
            "off": ObservationState.CLOSED,
            "unavailable": ObservationState.UNAVAILABLE,
        },
    )


@pytest.mark.parametrize(
    ("fixture", "expected"),
    [
        ("opening_on.json", ObservationState.OPEN),
        ("opening_off.json", ObservationState.CLOSED),
        ("opening_unavailable.json", ObservationState.UNAVAILABLE),
    ],
)
def test_realistic_home_assistant_state_fixtures(fixture, expected):
    observation = make_adapter(load_fixture(fixture)).get_opening_state(REFERENCE)

    assert observation.resource_reference == REFERENCE
    assert observation.state is expected
    assert observation.observed_at.tzinfo is not None


def test_malformed_timestamp_is_rejected():
    with pytest.raises(ValueError, match="invalid last_updated"):
        make_adapter(load_fixture("opening_malformed.json")).get_opening_state(
            REFERENCE
        )
