from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .models import HomeResourceReference, ResourceId


class LightObservationState(str, Enum):
    ON = "ON"
    OFF = "OFF"
    UNAVAILABLE = "UNAVAILABLE"
    STALE = "STALE"


@dataclass(frozen=True)
class LightObservation:
    resource_id: ResourceId
    resource_reference: HomeResourceReference
    state: LightObservationState
    observed_at: datetime
