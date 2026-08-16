from __future__ import annotations

from dataclasses import dataclass

from gaia.home.outcomes import RequestOutcome, Unsupported
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability


@dataclass(frozen=True)
class Request:
    operation: str
    resource_label: str


class RequestRouter:
    """Performs explicit deterministic routing without Home interpretation."""

    READ_OPENING_STATE = "read_opening_state"

    def __init__(self, read_opening_state: ReadOpeningStateCapability) -> None:
        self._read_opening_state = read_opening_state

    def handle(self, request: Request) -> RequestOutcome:
        if request.operation != self.READ_OPENING_STATE:
            return Unsupported(operation=request.operation)
        return self._read_opening_state.execute(request.resource_label)
