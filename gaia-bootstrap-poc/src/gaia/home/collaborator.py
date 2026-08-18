from __future__ import annotations

from .read_current_resource_state import (
    ReadCurrentResourceStateCapability,
    ReadCurrentResourceStateRequest,
)
from .w3_outcomes import ReadCurrentResourceStateOutcome


class HomeCollaborator:
    """Bounded Home collaborator for one-resource current-state reads."""

    def __init__(self, capability: ReadCurrentResourceStateCapability) -> None:
        self._capability = capability

    def read_current_state(
        self, request: ReadCurrentResourceStateRequest
    ) -> ReadCurrentResourceStateOutcome:
        return self._capability.execute(request)
