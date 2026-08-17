from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Protocol

from gaia.home.models import HomeResourceReference, Observation, ObservationState


class HomeAssistantStateTransport(Protocol):
    """Minimal transport seam for one already-resolved Home Assistant entity."""

    def get_state(self, entity_id: str) -> Mapping[str, object]:
        ...


class ExperimentalHomeAssistantAdapter:
    """Deterministic experiment for the existing OpeningStateProvider seam.

    This is deliberately not the final production adapter.

    The caller supplies the source-state mapping explicitly so that this
    experiment does not silently turn an architectural assumption into policy.
    """

    def __init__(
        self,
        transport: HomeAssistantStateTransport,
        state_mapping: Mapping[str, ObservationState],
    ) -> None:
        self._transport = transport
        self._state_mapping = {
            str(source).lower(): target
            for source, target in state_mapping.items()
        }

    def get_opening_state(
        self, resource_reference: HomeResourceReference
    ) -> Observation:
        payload = self._transport.get_state(resource_reference.value)

        if not isinstance(payload, Mapping):
            raise ValueError("Home Assistant response is not an object")

        entity_id = payload.get("entity_id")
        if entity_id != resource_reference.value:
            raise ValueError("Home Assistant response has mismatched entity_id")

        source_state = payload.get("state")
        if not isinstance(source_state, str):
            raise ValueError("Home Assistant response has invalid state")

        try:
            state = self._state_mapping[source_state.lower()]
        except KeyError as exc:
            raise ValueError(
                f"unmapped Home Assistant state: {source_state!r}"
            ) from exc

        timestamp = payload.get("last_updated")
        if not isinstance(timestamp, str):
            raise ValueError("Home Assistant response has no last_updated")

        try:
            observed_at = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise ValueError(
                "Home Assistant response has invalid last_updated"
            ) from exc

        if observed_at.tzinfo is None:
            raise ValueError("Home Assistant last_updated is not timezone-aware")

        return Observation(
            resource_reference=resource_reference,
            state=state,
            observed_at=observed_at,
        )
