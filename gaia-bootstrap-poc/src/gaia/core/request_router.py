from __future__ import annotations

from dataclasses import dataclass

from gaia.home.outcomes import RequestOutcome, Unsupported
from gaia.home.read_current_resource_state import (
    ApprovalStatus,
    PolicyResult,
    ReadCurrentResourceStateRequest,
)
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability
from gaia.home.w3_outcomes import ReadCurrentResourceStateOutcome
from gaia.home.collaborator import HomeCollaborator


@dataclass(frozen=True)
class Request:
    operation: str
    resource_label: str
    policy_result: str = "Allowed"
    approval: str = "Not Required"


class RequestRouter:
    """Performs explicit deterministic routing without Home interpretation."""

    READ_OPENING_STATE = "read_opening_state"
    READ_CURRENT_RESOURCE_STATE = "read_current_state"

    def __init__(
        self,
        read_opening_state: ReadOpeningStateCapability | None = None,
        home_collaborator: HomeCollaborator | None = None,
    ) -> None:
        self._read_opening_state = read_opening_state
        self._home_collaborator = home_collaborator

    def handle(
        self, request: Request
    ) -> RequestOutcome | ReadCurrentResourceStateOutcome:
        if request.operation == self.READ_OPENING_STATE:
            if self._read_opening_state is None:
                return Unsupported(operation=request.operation)
            return self._read_opening_state.execute(request.resource_label)

        if request.operation == self.READ_CURRENT_RESOURCE_STATE:
            if self._home_collaborator is None:
                return Unsupported(operation=request.operation)
            return self._home_collaborator.read_current_state(
                ReadCurrentResourceStateRequest(
                    label=request.resource_label,
                    policy_result=PolicyResult(request.policy_result),
                    approval=ApprovalStatus(request.approval),
                )
            )

        return Unsupported(operation=request.operation)
