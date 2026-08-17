from __future__ import annotations

import json
from pathlib import Path

from gaia.adapters.experimental_home_assistant_adapter import (
    ExperimentalHomeAssistantAdapter,
)
from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import HomeResourceReference, ObservationState, ResourceId
from gaia.home.outcomes import Success
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "home_assistant"


class FixtureTransport:
    def __init__(self, payload: dict):
        self.payload = payload
        self.requested_entity = None

    def get_state(self, entity_id: str):
        self.requested_entity = entity_id
        return self.payload


def test_experimental_adapter_replaces_fake_at_full_read_path():
    payload = json.loads(
        (FIXTURE_DIR / "opening_on.json").read_text(encoding="utf-8")
    )
    reference = HomeResourceReference(payload["entity_id"])
    resource = ResolvedResource(
        resource_id=ResourceId("home.window.example"),
        external_reference=reference,
    )

    resolver = HomeResourceResolver({"example opening": (resource,)})
    transport = FixtureTransport(payload)
    provider = ExperimentalHomeAssistantAdapter(
        transport,
        {
            "on": ObservationState.OPEN,
            "off": ObservationState.CLOSED,
            "unavailable": ObservationState.UNAVAILABLE,
        },
    )
    capability = ReadOpeningStateCapability(resolver, provider)
    router = RequestRouter(capability)

    outcome = router.handle(
        Request(
            operation=RequestRouter.READ_OPENING_STATE,
            resource_label="example opening",
        )
    )

    assert isinstance(outcome, Success)
    assert outcome.resource_id == ResourceId("home.window.example")
    assert outcome.observation.resource_reference == reference
    assert outcome.observation.state is ObservationState.OPEN
    assert transport.requested_entity == reference.value
