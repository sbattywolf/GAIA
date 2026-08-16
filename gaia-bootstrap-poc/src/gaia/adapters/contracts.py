from __future__ import annotations

from typing import Protocol

from gaia.home.models import HomeResourceReference, Observation


class OpeningStateProvider(Protocol):
    """Reads one external opening state without applying Home meaning."""

    def get_opening_state(
        self, resource_reference: HomeResourceReference
    ) -> Observation:
        ...
