from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VerificationResult:
    success: bool
    score: float
    failures: list[str]
    parsed: dict[str, Any] | None


@dataclass(frozen=True)
class GoldenCase:
    name: str
    expectations: dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0


@dataclass(frozen=True)
class GoldenSuite:
    domain: str
    cases: dict[str, GoldenCase]


def load_golden_cases(path: str) -> GoldenSuite:
    import yaml

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    cases = {}
    for name, spec in (data.get("cases") or {}).items():
        cases[name] = GoldenCase(
            name=name,
            expectations=spec.get("expectations") or {},
            weight=float(spec.get("weight", 1.0)),
        )

    return GoldenSuite(
        domain=str(data.get("domain", "")),
        cases=cases,
    )


def is_mapping(value: Any) -> bool:
    return isinstance(value, dict)


def get_path(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current
