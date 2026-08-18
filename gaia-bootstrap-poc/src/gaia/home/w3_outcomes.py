from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .outcomes import Unsupported
from .light_models import LightObservation
from .models import ResourceId


@dataclass(frozen=True)
class CurrentStateSuccess:
    resource_id: ResourceId
    observation: LightObservation


@dataclass(frozen=True)
class ResourceNotFound:
    label: str


@dataclass(frozen=True)
class ResourceAmbiguous:
    label: str
    candidate_ids: tuple[ResourceId, ...]


@dataclass(frozen=True)
class InvalidResourceReference:
    resource_id: ResourceId
    reason: str


@dataclass(frozen=True)
class SourceUnavailable:
    resource_id: ResourceId


@dataclass(frozen=True)
class InformationStale:
    resource_id: ResourceId
    observation: LightObservation


@dataclass(frozen=True)
class ExecutionFailure:
    reason: str


@dataclass(frozen=True)
class Denied:
    reason: str = "policy denied"


@dataclass(frozen=True)
class Indeterminate:
    reason: str = "policy indeterminate"


@dataclass(frozen=True)
class ApprovalRequired:
    reason: str = "approval required"


ReadCurrentResourceStateOutcome: TypeAlias = (
    CurrentStateSuccess
    | ResourceNotFound
    | ResourceAmbiguous
    | InvalidResourceReference
    | SourceUnavailable
    | InformationStale
    | ExecutionFailure
    | Denied
    | Indeterminate
    | ApprovalRequired
    | Unsupported
)
