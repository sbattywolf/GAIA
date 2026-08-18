from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from gaia.adapters.light_contracts import (
    InvalidLightResourceReference,
    LightStateProvider,
    MalformedLightProviderResponse,
)

from .light_models import LightObservation, LightObservationState
from .models import HomeResourceReference, ResourceId
from .resource_resolver import (
    AmbiguousResource,
    HomeResourceResolver,
    ResolvedResource,
    UnknownResource,
)
from .w3_outcomes import (
    ApprovalRequired,
    CurrentStateSuccess,
    Denied,
    ExecutionFailure,
    Indeterminate,
    InformationStale,
    InvalidResourceReference,
    ReadCurrentResourceStateOutcome,
    ResourceAmbiguous,
    ResourceNotFound,
    SourceUnavailable,
)


@dataclass(frozen=True)
class ReadCurrentResourceStateRequest:
    """Already-authorized semantic input for the W3 read Capability."""

    label: str


class ReadCurrentResourceStateCapability:
    """Semantic W3 read capability with exactly-one-Resource scope."""

    OPERATION = "read_current_state"

    def __init__(
        self,
        resolver: HomeResourceResolver,
        provider: LightStateProvider,
    ) -> None:
        self._resolver = resolver
        self._provider = provider

    def execute(
        self, request: ReadCurrentResourceStateRequest
    ) -> ReadCurrentResourceStateOutcome:
        resolution = self._resolver.resolve(request.label)
        if isinstance(resolution, UnknownResource):
            return ResourceNotFound(label=request.label)
        if isinstance(resolution, AmbiguousResource):
            return ResourceAmbiguous(
                label=request.label,
                candidate_ids=tuple(
                    candidate.resource_id for candidate in resolution.candidates
                ),
            )

        return self._read_one(resolution)

    def _read_one(
        self, resource: ResolvedResource
    ) -> ReadCurrentResourceStateOutcome:
        try:
            observation = self._provider.get_light_state(
                resource.external_reference
            )
        except (InvalidLightResourceReference, LookupError):
            return InvalidResourceReference(
                resource_id=resource.resource_id,
                reason="invalid or unknown external resource reference",
            )
        except MalformedLightProviderResponse as exc:
            return ExecutionFailure(reason=str(exc))
        except ConnectionError:
            return SourceUnavailable(resource_id=resource.resource_id)
        except Exception as exc:
            return ExecutionFailure(
                reason=f"provider failure: {type(exc).__name__}"
            )

        if not isinstance(observation, LightObservation):
            return ExecutionFailure(reason="provider returned malformed observation")
        if observation.resource_id != resource.resource_id:
            return ExecutionFailure(reason="provider returned mismatched ResourceId")
        if observation.resource_reference != resource.external_reference:
            return ExecutionFailure(
                reason="provider returned mismatched resource reference"
            )

        if observation.state is LightObservationState.UNAVAILABLE:
            return SourceUnavailable(resource_id=resource.resource_id)
        if observation.state is LightObservationState.STALE:
            return InformationStale(
                resource_id=resource.resource_id,
                observation=observation,
            )

        if observation.state not in (
            LightObservationState.ON,
            LightObservationState.OFF,
        ):
            return ExecutionFailure(reason="provider returned invalid light state")

        if observation.observed_at.tzinfo is None:
            return ExecutionFailure(reason="observation timestamp is not timezone-aware")

        return CurrentStateSuccess(
            resource_id=resource.resource_id,
            observation=observation,
        )
