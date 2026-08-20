"""
HC-1070: Bounded Home Collaborator Implementation

This module implements the specific bounded Home Collaborator for 
the HC-1070 milestone, which is a read-only collaborator that operates 
within the PM-001 architectural boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from gaia.adapters.light_contracts import LightStateProvider
from gaia.home.models import HomeResourceReference, ResourceId
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource
from gaia.home.w3_outcomes import ReadCurrentResourceStateOutcome
from gaia.home.read_current_resource_state import ReadCurrentResourceStateCapability, ReadCurrentResourceStateRequest


@dataclass(frozen=True)
class HC1070CollaboratorRequest:
    """HC-1070 specific request structure."""
    
    # This is a bounded request for one specific resource
    label: str


class HC1070Collaborator:
    """
    Bounded Home Collaborator for HC-1070.
    
    This collaborator implements the read-only semantic for exactly 
    one resource (home.light.living_room) as defined by PM-001.
    """
    
    def __init__(
        self,
        resolver: HomeResourceResolver,
        provider: LightStateProvider,
    ) -> None:
        """Initialize the HC-1070 Collaborator with a resolver and provider."""
        self._capability = ReadCurrentResourceStateCapability(resolver, provider)
        
    def read_current_state(
        self, request: HC1070CollaboratorRequest
    ) -> ReadCurrentResourceStateOutcome:
        """
        Execute a read operation for the bounded Home resource.
        
        This method is the single entry point for the HC-1070 collaborator
        that performs a read operation on exactly one resource.
        """
        # Convert the HC-1070 request to the standard request format
        standard_request = ReadCurrentResourceStateRequest(request.label)
        return self._capability.execute(standard_request)