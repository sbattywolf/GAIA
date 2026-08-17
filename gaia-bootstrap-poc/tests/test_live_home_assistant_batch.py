from __future__ import annotations

import os

import pytest

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.adapters.home_assistant_http_transport import HomeAssistantHTTPTransport
from gaia.home.models import HomeResourceReference, ObservationState


def _entity_ids() -> list[str]:
    raw = os.getenv("GAIA_HA_ENTITY_IDS", "")
    entity_ids = [item.strip() for item in raw.split(",") if item.strip()]

    if not entity_ids:
        single = os.getenv("GAIA_HA_ENTITY_ID", "").strip()
        if single:
            entity_ids = [single]

    if not entity_ids:
        pytest.skip(
            "Set GAIA_HA_ENTITY_IDS (comma-separated) or GAIA_HA_ENTITY_ID "
            "to run the optional live Home Assistant integration test."
        )

    return list(dict.fromkeys(entity_ids))


@pytest.mark.integration
def test_live_home_assistant_batch_read():
    base_url = os.getenv("GAIA_HA_URL")
    token = os.getenv("GAIA_HA_TOKEN")
    entity_ids = _entity_ids()

    if not base_url or not token:
        pytest.skip(
            "Set GAIA_HA_URL and GAIA_HA_TOKEN to run the optional "
            "live Home Assistant integration test."
        )

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

    failures: list[str] = []
    observations = []

    for entity_id in entity_ids:
        try:
            observation = adapter.get_opening_state(
                HomeResourceReference(entity_id)
            )
            observations.append((entity_id, observation))
        except Exception as exc:
            failures.append(f"{entity_id}: {type(exc).__name__}: {exc}")

    assert not failures, (
        "Live Home Assistant batch read failures:\n"
        + "\n".join(failures)
    )

    assert len(observations) == len(entity_ids)
    assert all(
        observation.resource_reference.value == entity_id
        for entity_id, observation in observations
    )
    assert all(
        observation.observed_at.tzinfo is not None
        for _, observation in observations
    )
    assert all(
        observation.state
        in {
            ObservationState.OPEN,
            ObservationState.CLOSED,
            ObservationState.UNAVAILABLE,
        }
        for _, observation in observations
    )
