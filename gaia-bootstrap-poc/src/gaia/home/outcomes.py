from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .models import Observation, ResourceId


@dataclass(frozen=True)
class Success:
    resource_id: ResourceId
    observation: Observation


@dataclass(frozen=True)
class PartialSuccess:
    """Reserved for a later, explicitly approved multi-resource flow."""


@dataclass(frozen=True)
class ClarificationRequired:
    label: str


@dataclass(frozen=True)
class ResourceAmbiguous:
    label: str
    candidate_ids: tuple[ResourceId, ...]


@dataclass(frozen=True)
class SourceUnavailable:
    resource_id: ResourceId


@dataclass(frozen=True)
class InformationStale:
    resource_id: ResourceId
    observation: Observation


@dataclass(frozen=True)
class Denied:
    """Defined by the accepted outcome vocabulary; not emitted in this slice."""


@dataclass(frozen=True)
class Indeterminate:
    """Defined by the accepted outcome vocabulary; not emitted in this slice."""


@dataclass(frozen=True)
class Unsupported:
    operation: str


@dataclass(frozen=True)
class Failure:
    reason: str


ReadOpeningStateOutcome: TypeAlias = (
    Success
    | ClarificationRequired
    | ResourceAmbiguous
    | SourceUnavailable
    | InformationStale
    | Failure
)

RequestOutcome: TypeAlias = ReadOpeningStateOutcome | Unsupported
