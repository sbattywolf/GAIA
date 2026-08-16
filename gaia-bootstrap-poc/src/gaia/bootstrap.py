from __future__ import annotations

from gaia.adapters.fake_home_assistant_adapter import FakeHomeAssistantAdapter
from gaia.core.request_router import RequestRouter
from gaia.home.models import HomeResourceReference, ObservationState, ResourceId
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource


def build_bootstrap_router() -> RequestRouter:
    """Explicit composition root for the deterministic bootstrap."""

    kitchen = ResolvedResource(
        resource_id=ResourceId("home.window.kitchen"),
        external_reference=HomeResourceReference("window_kitchen"),
    )
    bedroom_north = ResolvedResource(
        resource_id=ResourceId("home.window.bedroom.north"),
        external_reference=HomeResourceReference("window_bedroom_north"),
    )
    bedroom_south = ResolvedResource(
        resource_id=ResourceId("home.window.bedroom.south"),
        external_reference=HomeResourceReference("window_bedroom_south"),
    )
    office = ResolvedResource(
        resource_id=ResourceId("home.window.office"),
        external_reference=HomeResourceReference("window_office"),
    )
    front = ResolvedResource(
        resource_id=ResourceId("home.door.front"),
        external_reference=HomeResourceReference("front_door"),
    )
    garage = ResolvedResource(
        resource_id=ResourceId("home.door.garage"),
        external_reference=HomeResourceReference("garage_door"),
    )

    resolver = HomeResourceResolver(
        {
            "kitchen window": (kitchen,),
            "bedroom window": (bedroom_north, bedroom_south),
            "office window": (office,),
            "front door": (front,),
            "garage door": (garage,),
        }
    )
    provider = FakeHomeAssistantAdapter(
        {
            kitchen.external_reference: ObservationState.OPEN,
            bedroom_north.external_reference: ObservationState.CLOSED,
            bedroom_south.external_reference: ObservationState.CLOSED,
            office.external_reference: ObservationState.STALE,
            front.external_reference: ObservationState.CLOSED,
            garage.external_reference: ObservationState.UNAVAILABLE,
        }
    )
    capability = ReadOpeningStateCapability(resolver, provider)
    return RequestRouter(capability)
