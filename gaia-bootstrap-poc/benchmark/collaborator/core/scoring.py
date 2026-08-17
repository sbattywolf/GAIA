from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TestScore:
    passed: bool
    score: float
    failures: list[str]


def score_test(success: bool, failures: list[str]) -> TestScore:
    return TestScore(
        passed=success,
        score=1.0 if success else 0.0,
        failures=failures,
    )


def score_model(test_results: list[dict]) -> dict:
    total = len(test_results)
    passed = sum(1 for item in test_results if item.get("success") is True)
    score = passed / total if total else 0.0

    return {
        "passed": passed,
        "total": total,
        "score": score,
        "percentage": round(score * 100.0, 2),
    }
