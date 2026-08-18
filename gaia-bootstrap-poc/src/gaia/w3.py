from __future__ import annotations

from gaia.adapters.light_contracts import LightStateProvider
from gaia.core.request_router import RequestRouter
from gaia.home.collaborator import HomeCollaborator
from gaia.home.models import HomeResourceReference, ResourceId
from gaia.home.read_current_resource_state import (
    ReadCurrentResourceStateCapability,
)
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource


LIVING_ROOM_LIGHT = ResolvedResource(
    resource_id=ResourceId("home.light.living_room"),
    external_reference=HomeResourceReference("light.living_room"),
)


def build_w3_router(provider: LightStateProvider) -> RequestRouter:
    """Compose the bounded W3 Single Home Read path."""
    resolver = HomeResourceResolver(
        {"living-room light": (LIVING_ROOM_LIGHT,)}
    )
    capability = ReadCurrentResourceStateCapability(resolver, provider)
    collaborator = HomeCollaborator(capability)
    return RequestRouter(home_collaborator=collaborator)
