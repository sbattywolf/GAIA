#!/usr/bin/env python3

import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
RESULTS_DIR = BASE_DIR / "results"


CLASSIFICATIONS = {
    "DOCUMENTATO",
    "IMPLEMENTATO",
    "PARZIALMENTE IMPLEMENTATO",
    "NON DIMOSTRATO",
}

CONCEPTS = [
    "Core",
    "Capability",
    "Adapter",
    "Home Assistant boundary",
    "Bootstrap POC",
]


def extract_classification(text, concept):
    """
    Best-effort extraction.

    This is intentionally not a semantic judge.
    It only detects an explicit classification near the concept.
    """

    pattern = re.compile(
        rf"{re.escape(concept)}"
        rf".{{0,300}}?"
        rf"(DOCUMENTATO|IMPLEMENTATO|PARZIALMENTE IMPLEMENTATO|NON DIMOSTRATO)",
        re.IGNORECASE | re.DOTALL,
    )

    match = pattern.search(text)

    if not match:
        return None

    return match.group(1).upper()


def extract_paths(text):
    """
    Extract repository-looking paths from the model response.
    """

    candidates = re.findall(
        r"""
        (?:
            [A-Za-z0-9_.-]+/
        )+
        [A-Za-z0-9_.-]+
        (?:\.[A-Za-z0-9_.-]+)?
        """,
        text,
        re.VERBOSE,
    )

    result = []

    for candidate in candidates:
        candidate = candidate.strip("`'\".,:;()")

        if candidate not in result:
            result.append(candidate)

    return result


def path_is_safe_and_exists(path):
    try:
        candidate = (REPO_ROOT / path).resolve()
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return False

    return candidate.exists()


def evaluate_test(test):
    response = test.get("response", "")
    tool_calls = test.get("tool_calls", [])

    tool_names = [
        call.get("name")
        for call in tool_calls
    ]

    return {
        "success": test.get("success", False),
        "tool_calls": len(tool_calls),
        "tool_names": tool_names,
        "response_length": len(response),
    }


def evaluate_t03(test):
    response = test.get("response", "")
    tool_calls = test.get("tool_calls", [])

    paths = extract_paths(response)

    existing = []
    missing = []

    for path in paths:
        if path_is_safe_and_exists(path):
            existing.append(path)
        else:
            missing.append(path)

    return {
        "tool_calls": len(tool_calls),
        "tool_names": [
            call.get("name")
            for call in tool_calls
        ],
        "paths_found_in_response": paths,
        "existing_paths": existing,
        "missing_paths": missing,
        "existing_path_count": len(existing),
        "missing_path_count": len(missing),
    }


def evaluate_model(path):
    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    result = {
        "benchmark_version": data.get("benchmark_version"),
        "model_name": data.get("model_name"),
        "model_verified": data.get(
            "model_verification",
            {},
        ).get("verified", False),
        "tests": {},
    }

    for test in data.get("tests", []):
        name = test.get("name")

        result["tests"][name] = evaluate_test(test)

        if name in {
            "T03_architecture_evidence",
            "T04_evidence_verification",
        }:
            result["tests"][name]["evidence"] = evaluate_t03(test)

    return result


def main():
    reports = []

    for path in sorted(RESULTS_DIR.glob("*.json")):
        reports.append(
            evaluate_model(path)
        )

    output = BASE_DIR / "evaluation-v0.json"

    output.write_text(
        json.dumps(
            reports,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {output}")

    for report in reports:
        print()
        print("=" * 70)
        print(report["model_name"])
        print("=" * 70)

        print(
            "model verified:",
            report["model_verified"],
        )

        for name, test in report["tests"].items():
            print(
                name,
                "| tools:",
                test["tool_calls"],
            )

            if "evidence" in test:
                evidence = test["evidence"]

                print(
                    "  existing evidence paths:",
                    evidence["existing_path_count"],
                )

                print(
                    "  missing evidence paths:",
                    evidence["missing_path_count"],
                )


if __name__ == "__main__":
    main()
