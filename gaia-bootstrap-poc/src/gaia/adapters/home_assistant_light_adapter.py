from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import Callable

from .light_contracts import (
    InvalidLightResourceReference,
    LightStateProvider,
    MalformedLightProviderResponse,
)
from .experimental_home_assistant_adapter import HomeAssistantStateTransport
from gaia.home.light_models import LightObservation, LightObservationState
from gaia.home.models import HomeResourceReference, ResourceId


class HomeAssistantLightAdapter(LightStateProvider):
    """Single read-only Home Assistant binding for one Light Resource."""

    def __init__(
        self,
        transport: HomeAssistantStateTransport,
        resource_id: ResourceId,
        *,
        max_age: timedelta | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._transport = transport
        self._resource_id = resource_id
        self._max_age = max_age
        self._now = now or (lambda: datetime.now(timezone.utc))

    def get_light_state(
        self, resource_reference: HomeResourceReference
    ) -> LightObservation:
        self._validate_reference(resource_reference)
        payload = self._transport.get_state(resource_reference.value)

        if not isinstance(payload, Mapping):
            raise MalformedLightProviderResponse(
                "Home Assistant response is not an object"
            )

        entity_id = payload.get("entity_id")
        if entity_id != resource_reference.value:
            raise MalformedLightProviderResponse(
                "Home Assistant response has mismatched entity_id"
            )

        source_state = payload.get("state")
        if not isinstance(source_state, str):
            raise MalformedLightProviderResponse(
                "Home Assistant response has invalid state"
            )

        timestamp = payload.get("last_updated")
        if not isinstance(timestamp, str):
            raise MalformedLightProviderResponse(
                "Home Assistant response has no last_updated"
            )

        try:
            observed_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise MalformedLightProviderResponse(
                "Home Assistant response has invalid last_updated"
            ) from exc

        if observed_at.tzinfo is None:
            raise MalformedLightProviderResponse(
                "Home Assistant last_updated is not timezone-aware"
            )

        state = {
            "on": LightObservationState.ON,
            "off": LightObservationState.OFF,
            "unavailable": LightObservationState.UNAVAILABLE,
        }.get(source_state.casefold())

        if state is None:
            raise MalformedLightProviderResponse(
                f"unsupported Home Assistant light state: {source_state!r}"
            )

        if (
            self._max_age is not None
            and state in (LightObservationState.ON, LightObservationState.OFF)
            and self._now() - observed_at > self._max_age
        ):
            state = LightObservationState.STALE

        return LightObservation(
            resource_id=self._resource_id,
            resource_reference=resource_reference,
            state=state,
            observed_at=observed_at,
        )

    @staticmethod
    def _validate_reference(
        resource_reference: HomeResourceReference,
    ) -> None:
        value = resource_reference.value
        if (
            value.count(".") != 1
            or not value.split(".", 1)[0]
            or not value.split(".", 1)[1]
        ):
            raise InvalidLightResourceReference(
                "malformed Home Assistant entity identifier"
            )
