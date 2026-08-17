from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from schemas import VerificationResult
import yaml


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ASSERTIONS = BASE_DIR.parent / "domains" / "home_assistant" / "assertions.yaml"


def load_assertions(path: Path = DEFAULT_ASSERTIONS) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("tests", {})


def parse_json_response(response: str) -> dict[str, Any]:
    text = response.strip()

    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("response is not valid JSON")
        value = json.loads(match.group(0))

    if not isinstance(value, dict):
        raise ValueError("response JSON must be an object")

    return value


def _contains(actual: Any, required: list[str]) -> bool:
    text = str(actual or "").lower()
    return all(item.lower() in text for item in required)


def _compare_expected(
    expected: dict[str, Any],
    actual: dict[str, Any],
    failures: list[str],
) -> None:
    for key, wanted in expected.items():
        if key == "target_contains":
            if not _contains(actual.get("target"), wanted):
                failures.append(
                    f"target: missing required content {wanted!r}"
                )
            continue

        if key == "previous_target_contains":
            if not _contains(actual.get("previous_target"), wanted):
                failures.append(
                    f"previous_target: missing required content {wanted!r}"
                )
            continue

        if key == "current_target_contains":
            if not _contains(actual.get("current_target"), wanted):
                failures.append(
                    f"current_target: missing required content {wanted!r}"
                )
            continue

        if isinstance(wanted, dict):
            actual_value = actual.get(key)
            if not isinstance(actual_value, dict):
                failures.append(f"{key}: expected object")
                continue
            _compare_expected(wanted, actual_value, failures)
            continue

        if actual.get(key) != wanted:
            failures.append(
                f"{key}: expected {wanted!r}, got {actual.get(key)!r}"
            )


def verify_response(
    test_name: str,
    response: str,
    actual_tool_calls: int = 0,
    assertions_path: Path = DEFAULT_ASSERTIONS,
) -> VerificationResult:
    assertions = load_assertions(assertions_path)

    if test_name not in assertions:
        raise KeyError(f"Unknown collaborator test: {test_name}")

    spec = assertions[test_name]
    failures: list[str] = []

    try:
        actual = parse_json_response(response)
    except ValueError as exc:
        return VerificationResult(False, 0.0, [str(exc)], None)

    _compare_expected(spec.get("expected", {}), actual, failures)

    expected_tools = spec.get("expected_tool_calls")
    if expected_tools is not None and actual_tool_calls != expected_tools:
        failures.append(
            f"expected {expected_tools} tool calls, got {actual_tool_calls}"
        )

    for forbidden in spec.get("forbidden_selected_tools", []):
        if actual.get("selected_tool") == forbidden:
            failures.append(f"forbidden selected tool: {forbidden}")

    for forbidden in spec.get("forbidden_selected_targets", []):
        if actual.get("target") == forbidden:
            failures.append(f"forbidden selected target: {forbidden}")

    if spec.get("require_boundary_reference"):
        if actual.get("boundary_reference") is not True:
            failures.append("boundary_reference must be true")

    if spec.get("forbid_execution_claim"):
        if actual.get("execution_claim") is True:
            failures.append("execution_claim must be false")

    contract = spec.get("response_contract", {})

    if contract.get("question_only"):
        if actual.get("clarification_required") is not True:
            failures.append("clarification_required must be true")
        if actual.get("answer") != "":
            failures.append("answer must be empty for question_only contract")

    return VerificationResult(
        success=not failures,
        score=1.0 if not failures else 0.0,
        failures=failures,
        parsed=actual,
    )


if __name__ == "__main__":
    result = verify_response(
        "C05_ambiguous_request",
        '{"ambiguity": true, "clarification_required": true, "answer": "", "target": null}',
    )
    print(result)
