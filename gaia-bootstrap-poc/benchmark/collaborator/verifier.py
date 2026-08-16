#!/usr/bin/env python3

from pathlib import Path
import re

import yaml


BASE_DIR = Path(__file__).resolve().parent
ASSERTIONS_FILE = BASE_DIR / "assertions.yaml"


def load_assertions():
    data = yaml.safe_load(
        ASSERTIONS_FILE.read_text(encoding="utf-8")
    )
    return data["tests"]


def count_questions(text):
    return len(re.findall(r"[?؟]", text))


def verify_response(test_name, response, actual_tool_calls=0):
    assertions = load_assertions()

    if test_name not in assertions:
        raise KeyError(f"Unknown collaborator test: {test_name}")

    spec = assertions[test_name]
    text = response.lower()

    failures = []

    for item in spec.get("must_contain", []):
        if item.lower() not in text:
            failures.append(
                f"missing required text: {item}"
            )

    any_items = spec.get("must_contain_any", [])

    if any_items:
        if not any(item.lower() in text for item in any_items):
            failures.append(
                "none of required alternatives found: "
                + ", ".join(any_items)
            )

    for item in spec.get("must_not_contain", []):
        if item.lower() in text:
            failures.append(
                f"forbidden text found: {item}"
            )

    expected_tools = spec.get("expected_tool_calls")

    if expected_tools is not None:
        if actual_tool_calls != expected_tools:
            failures.append(
                f"expected {expected_tools} tool calls, "
                f"got {actual_tool_calls}"
            )

    response_contract = spec.get("response_contract", {})

    if response_contract.get("question_only"):
        if count_questions(response) != 1:
            failures.append(
                "expected exactly one clarification question"
            )

    max_questions = response_contract.get("max_questions")

    if max_questions is not None:
        if count_questions(response) > max_questions:
            failures.append(
                f"expected at most {max_questions} question(s)"
            )

    return {
        "success": not failures,
        "failures": failures,
    }


if __name__ == "__main__":
    result = verify_response(
        "C05_ambiguous_request",
        "Quale luce vuoi spegnere?",
        actual_tool_calls=0,
    )

    print(result)
