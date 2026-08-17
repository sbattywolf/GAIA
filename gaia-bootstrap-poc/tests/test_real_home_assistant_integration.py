from __future__ import annotations

import os

import pytest

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.adapters.home_assistant_http_transport import HomeAssistantHTTPTransport
from gaia.home.models import HomeResourceReference, ObservationState


def _runtime_config() -> tuple[str, str, str]:
    base_url = os.getenv("GAIA_HA_URL")
    token = os.getenv("GAIA_HA_TOKEN")
    entity_id = os.getenv("GAIA_HA_ENTITY_ID")

    if not all((base_url, token, entity_id)):
        pytest.skip(
            "Set GAIA_HA_URL, GAIA_HA_TOKEN and GAIA_HA_ENTITY_ID "
            "to run the optional live Home Assistant integration test."
        )

    return base_url, token, entity_id


@pytest.mark.integration
def test_live_home_assistant_single_entity_read():
    base_url, token, entity_id = _runtime_config()

    transport = HomeAssistantHTTPTransport(
        base_url=base_url,
        bearer_token=token,
        timeout=5.0,
    )
    adapter = ExperimentalHomeAssistantAdapter(
        transport,
        {
            "on": ObservationState.OPEN,
            "off": ObservationState.CLOSED,
            "unavailable": ObservationState.UNAVAILABLE,
        },
    )

    observation = adapter.get_opening_state(
        HomeResourceReference(entity_id)
    )

    assert observation.resource_reference.value == entity_id
    assert observation.observed_at.tzinfo is not None
    assert observation.state in {
        ObservationState.OPEN,
        ObservationState.CLOSED,
        ObservationState.UNAVAILABLE,
    }
