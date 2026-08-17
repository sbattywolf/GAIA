from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Score:
    earned: float
    possible: float
    passed: bool

    @property
    def ratio(self) -> float:
        return self.earned / self.possible if self.possible else 0.0


def score_case(*, verifier_success: bool, weight: float = 1.0) -> Score:
    possible = float(weight)
    earned = possible if verifier_success else 0.0
    return Score(earned=earned, possible=possible, passed=verifier_success)


def score_golden_model(tests):
    """Score golden results using each test's declared weight."""
    earned = 0.0
    possible = 0.0

    for test in tests:
        golden = test.get("golden", {})
        weight = float(golden.get("weight", 1.0))
        possible += weight

        if golden.get("passed") is True:
            earned += weight

    ratio = earned / possible if possible else 0.0

    return {
        "score": ratio,
        "earned": earned,
        "possible": possible,
        "ratio": ratio,
        "passed": sum(
            1
            for test in tests
            if test.get("golden", {}).get("passed") is True
        ),
        "total": len(tests),
    }

def score_suite(results: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [
        score_case(
            verifier_success=bool(item.get("success")),
            weight=float(item.get("weight", 1.0)),
        )
        for item in results
    ]

    earned = sum(item.earned for item in scores)
    possible = sum(item.possible for item in scores)

    return {
        "earned": earned,
        "possible": possible,
        "ratio": earned / possible if possible else 0.0,
        "passed": sum(1 for item in scores if item.passed),
        "total": len(scores),
    }

def score_model(results):
    """Aggregate the runner's list of per-test results."""
    if not isinstance(results, list):
        raise TypeError("score_model expects a list of test results")

    total = len(results)
    passed = sum(
        1
        for item in results
        if isinstance(item, dict) and item.get("success") is True
    )

    possible = float(total)
    earned = float(passed)
    ratio = earned / possible if possible else 0.0

    return {
        "score": ratio,
        "earned": earned,
        "possible": possible,
        "ratio": ratio,
        "passed": passed,
        "total": total,
    }


