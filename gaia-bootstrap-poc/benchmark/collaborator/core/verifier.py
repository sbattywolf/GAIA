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


def _contains_groups(actual: Any, groups: list[list[str]]) -> bool:
    text = str(actual or "").lower()
    return all(
        any(alias.lower() in text for alias in group)
        for group in groups
    )


def _get_path(data: Any, path: str) -> Any:
    value = data
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def evaluate_golden_expectations(
    expectations: dict[str, Any],
    actual: dict[str, Any],
) -> list[str]:
    """Evaluate golden expectations with explicit operation alias handling."""
    failures: list[str] = []

    for key, wanted in expectations.items():
        if key == "path_contains_groups":
            for path, groups in wanted.items():
                value = _get_path(actual, path)
                if not _contains_groups(value, groups):
                    failures.append(
                        f"{path}: missing semantic content groups {groups!r}"
                    )
            continue

        if key == "operation" and isinstance(wanted, dict):
            actual_operation = actual.get("operation")
            aliases = wanted.get("aliases", [])
            canonical = wanted.get("canonical")

            if not aliases:
                aliases = [canonical] if canonical is not None else []

            if actual_operation not in aliases:
                failures.append(
                    "operation: expected one of "
                    f"{aliases!r} (canonical={canonical!r}), "
                    f"got {actual_operation!r}"
                )
            continue

        if key in {"target", "previous_target", "current_target"}:
            value = actual.get(key)

            if isinstance(wanted, dict):
                if isinstance(value, dict):
                    for field, aliases in wanted.items():
                        if not isinstance(aliases, list):
                            aliases = [aliases]
                        actual_value = value.get(field)
                        if not any(
                            str(alias).lower()
                            == str(actual_value or "").lower()
                            for alias in aliases
                        ):
                            failures.append(
                                f"{key}.{field}: expected one of "
                                f"{aliases!r}, got {actual_value!r}"
                            )
                else:
                    failures.append(
                        f"{key}: expected structured object"
                    )
                continue

            if not _contains_groups(value, wanted):
                failures.append(
                    f"{key}: missing semantic content groups {wanted!r}"
                )
            continue

        if key == "clarification_question":
            if wanted is True:
                answer = actual.get("answer")
                if not isinstance(answer, str) or not answer.strip():
                    failures.append(
                        "clarification_question: expected non-empty answer"
                    )
            continue

        if key == "max_questions":
            answer = str(actual.get("answer", ""))
            count = answer.count("?") + answer.count("？")
            if count > int(wanted):
                failures.append(
                    f"max_questions: expected <= {wanted}, got {count}"
                )
            continue

        actual_value = actual.get(key)

        if isinstance(wanted, list):
            if actual_value not in wanted:
                failures.append(
                    f"{key}: expected one of {wanted!r}, got {actual_value!r}"
                )
        elif actual_value != wanted:
            failures.append(
                f"{key}: expected {wanted!r}, got {actual_value!r}"
            )

    return failures

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

        if key == "target_contains_groups":
            if not _contains_groups(actual.get("target"), wanted):
                failures.append(
                    f"target: missing semantic content groups {wanted!r}"
                )
            continue


        if key == "path_contains_groups":
            for path, groups in wanted.items():
                value = _get_path(actual, path)
                if not _contains_groups(value, groups):
                    failures.append(
                        f"{path}: missing semantic content groups {groups!r}"
                    )
            continue

        if key == "previous_target_contains":
            if not _contains(actual.get("previous_target"), wanted):
                failures.append(
                    f"previous_target: missing required content {wanted!r}"
                )
            continue

        if key == "previous_target_contains_groups":
            if not _contains_groups(actual.get("previous_target"), wanted):
                failures.append(
                    "previous_target: missing semantic content groups "
                    f"{wanted!r}"
                )
            continue

        if key == "current_target_contains":
            if not _contains(actual.get("current_target"), wanted):
                failures.append(
                    f"current_target: missing required content {wanted!r}"
                )
            continue

        if key == "current_target_contains_groups":
            if not _contains_groups(actual.get("current_target"), wanted):
                failures.append(
                    "current_target: missing semantic content groups "
                    f"{wanted!r}"
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

        answer = actual.get("answer")
        if not isinstance(answer, str) or not answer.strip():
            failures.append("answer must contain the clarification question")

        max_questions = contract.get("max_questions")
        if max_questions is not None and isinstance(answer, str):
            question_count = answer.count("?") + answer.count("？")
            if question_count != max_questions:
                failures.append(
                    f"answer must contain exactly {max_questions} question(s), "
                    f"got {question_count}"
                )

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
