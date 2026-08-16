from __future__ import annotations

from gaia.adapters.contracts import OpeningStateProvider

from .models import Observation, ObservationState
from .outcomes import (
    ClarificationRequired,
    Failure,
    InformationStale,
    ReadOpeningStateOutcome,
    ResourceAmbiguous,
    SourceUnavailable,
    Success,
)
from .resource_resolver import (
    AmbiguousResource,
    HomeResourceResolver,
    ResolvedResource,
    UnknownResource,
)


class ReadOpeningStateCapability:
    """Coordinates one read without knowing provider implementation details."""

    def __init__(
        self,
        resolver: HomeResourceResolver,
        provider: OpeningStateProvider,
    ) -> None:
        self._resolver = resolver
        self._provider = provider

    def execute(self, label: str) -> ReadOpeningStateOutcome:
        resolution = self._resolver.resolve(label)
        if isinstance(resolution, UnknownResource):
            return ClarificationRequired(label=label)
        if isinstance(resolution, AmbiguousResource):
            return ResourceAmbiguous(
                label=label,
                candidate_ids=tuple(
                    candidate.resource_id for candidate in resolution.candidates
                ),
            )

        return self._read_resolved(resolution)

    def _read_resolved(self, resource: ResolvedResource) -> ReadOpeningStateOutcome:
        try:
            observation = self._provider.get_opening_state(
                resource.external_reference
            )
        except Exception as exc:
            return Failure(reason=f"provider failure: {type(exc).__name__}")

        if not isinstance(observation, Observation):
            return Failure(reason="provider returned malformed observation")
        if observation.resource_reference != resource.external_reference:
            return Failure(reason="provider returned mismatched resource reference")
        if not isinstance(observation.state, ObservationState):
            return Failure(reason="provider returned invalid observation state")

        if observation.state is ObservationState.UNAVAILABLE:
            return SourceUnavailable(resource_id=resource.resource_id)
        if observation.state is ObservationState.STALE:
            return InformationStale(
                resource_id=resource.resource_id,
                observation=observation,
            )
        return Success(resource_id=resource.resource_id, observation=observation)
