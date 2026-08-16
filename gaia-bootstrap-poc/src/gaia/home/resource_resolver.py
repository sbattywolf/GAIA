from __future__ import annotations

from dataclasses import dataclass

from .models import HomeResourceReference, ResourceId


@dataclass(frozen=True)
class ResolvedResource:
    resource_id: ResourceId
    external_reference: HomeResourceReference


@dataclass(frozen=True)
class UnknownResource:
    label: str


@dataclass(frozen=True)
class AmbiguousResource:
    label: str
    candidates: tuple[ResolvedResource, ...]


Resolution = ResolvedResource | UnknownResource | AmbiguousResource


class HomeResourceResolver:
    """Owns bounded Home labels; it never calls an external provider."""

    def __init__(
        self,
        mappings: dict[str, tuple[ResolvedResource, ...]],
    ) -> None:
        self._mappings = {
            self._normalise(label): tuple(resources)
            for label, resources in mappings.items()
        }

    def resolve(self, label: str) -> Resolution:
        normalised = self._normalise(label)
        candidates = self._mappings.get(normalised, ())
        if not candidates:
            return UnknownResource(label=label)
        if len(candidates) > 1:
            return AmbiguousResource(label=label, candidates=candidates)
        return candidates[0]

    @staticmethod
    def _normalise(label: str) -> str:
        return " ".join(label.strip().casefold().split())
