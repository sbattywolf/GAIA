from __future__ import annotations

from typing import Protocol

from gaia.home.light_models import LightObservation
from gaia.home.models import HomeResourceReference


class InvalidLightResourceReference(ValueError):
    """The bounded Home-light external reference is malformed."""


class MalformedLightProviderResponse(ValueError):
    """The bounded Home-light provider response is malformed."""


class LightStateProvider(Protocol):
    """Reads one explicitly resolved Home light resource."""

    def get_light_state(
        self, resource_reference: HomeResourceReference
    ) -> LightObservation:
        ...
