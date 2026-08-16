from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass(frozen=True)
class ResourceId:
    """Canonical GAIA resource identity."""

    value: str


@dataclass(frozen=True)
class HomeResourceReference:
    """External reference understood by a Home state provider."""

    value: str


class ObservationState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    UNAVAILABLE = "UNAVAILABLE"
    STALE = "STALE"


@dataclass(frozen=True)
class Observation:
    """Source-grounded observation returned by a provider."""

    resource_reference: HomeResourceReference
    state: ObservationState
    observed_at: datetime
