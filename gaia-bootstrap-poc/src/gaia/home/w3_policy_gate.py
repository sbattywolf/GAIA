from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .w3_outcomes import ApprovalRequired, Denied, Indeterminate


class PolicyResult(str, Enum):
    ALLOWED = "Allowed"
    DENIED = "Denied"
    INDETERMINATE = "Indeterminate"


class ApprovalRequirement(str, Enum):
    NOT_REQUIRED = "Not Required"
    REQUIRED = "Required"


class ApprovalGrant(str, Enum):
    NOT_GRANTED = "Not Granted"
    GRANTED = "Granted"


@dataclass(frozen=True)
class PolicyApprovalDecision:
    policy: PolicyResult = PolicyResult.ALLOWED
    approval: ApprovalRequirement = ApprovalRequirement.NOT_REQUIRED
    grant: ApprovalGrant = ApprovalGrant.NOT_GRANTED


class W3ExecutionGate:
    """Deterministic W3-only Core execution gate."""

    def decide(self, decision: PolicyApprovalDecision):
        if decision.policy is PolicyResult.DENIED:
            return Denied()
        if decision.policy is PolicyResult.INDETERMINATE:
            return Indeterminate()
        if (
            decision.approval is ApprovalRequirement.REQUIRED
            and decision.grant is not ApprovalGrant.GRANTED
        ):
            return ApprovalRequired()
        return None
