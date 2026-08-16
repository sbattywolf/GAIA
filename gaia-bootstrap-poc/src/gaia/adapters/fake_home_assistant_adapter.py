from __future__ import annotations

from datetime import datetime, timezone

from gaia.home.models import (
    HomeResourceReference,
    Observation,
    ObservationState,
)


class FakeHomeAssistantAdapter:
    """Deterministic in-memory state source with no external communication."""

    DEFAULT_OBSERVED_AT = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)

    def __init__(
        self,
        states: dict[HomeResourceReference, ObservationState],
        observed_at: datetime = DEFAULT_OBSERVED_AT,
    ) -> None:
        if observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")
        self._states = dict(states)
        self._observed_at = observed_at

    def get_opening_state(
        self, resource_reference: HomeResourceReference
    ) -> Observation:
        try:
            state = self._states[resource_reference]
        except KeyError as exc:
            raise LookupError(resource_reference.value) from exc

        return Observation(
            resource_reference=resource_reference,
            state=state,
            observed_at=self._observed_at,
        )
