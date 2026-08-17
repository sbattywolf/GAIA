#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent
DOMAINS_DIR = BASE_DIR / "domains"
RESULTS_DIR = BASE_DIR / "results"
MODELS_FILE = BASE_DIR / "models.yaml"

OLLAMA_URL = "http://localhost:11434"

sys.path.insert(0, str(BASE_DIR / "core"))

from scoring import score_model
from verifier import verify_response


DOMAIN_TESTS = {
    "home_assistant": [
        "C01_intent_recognition",
        "C02_tool_selection",
        "C03_home_assistant_action",
        "C04_invalid_entity",
        "C05_ambiguous_request",
        "C06_multiturn_state",
    ],
}


def load_models():
    data = yaml.safe_load(MODELS_FILE.read_text(encoding="utf-8"))
    return data.get("models", [])


def load_test(domain, name):
    path = DOMAINS_DIR / domain / "tests" / f"{name}.md"
    return path.read_text(encoding="utf-8")


def ollama_show(model):
    response = requests.post(
        f"{OLLAMA_URL}/api/show",
        json={"name": model},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def ollama_generate(model, prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
    response.raise_for_status()
    return response.json()


def extract_tool_calls(data):
    calls = data.get("tool_calls", [])
    return calls if isinstance(calls, list) else []


def run_test(model, domain, test_name):
    prompt = load_test(domain, test_name)
    start = time.monotonic()

    try:
        data = ollama_generate(model, prompt)
        response = data.get("response", "")
        tool_calls = extract_tool_calls(data)

        verification = verify_response(
            test_name,
            response,
            actual_tool_calls=len(tool_calls),
            assertions_path=DOMAINS_DIR / domain / "assertions.yaml",
        )

        error = None
    except Exception as exc:
        response = ""
        tool_calls = []
        verification = None
        error = f"{type(exc).__name__}: {exc}"

    elapsed = round(time.monotonic() - start, 3)

    if error:
        return {
            "name": test_name,
            "success": False,
            "score": 0.0,
            "elapsed_seconds": elapsed,
            "tool_calls": tool_calls,
            "verification": {
                "success": False,
                "failures": [f"runner error: {error}"],
            },
            "response": response,
        }

    return {
        "name": test_name,
        "success": verification.success,
        "score": verification.score,
        "elapsed_seconds": elapsed,
        "tool_calls": tool_calls,
        "verification": {
            "success": verification.success,
            "failures": verification.failures,
            "parsed": verification.parsed,
        },
        "response": response,
    }


def run_domain(model, domain):
    tests = [
        run_test(model, domain, test_name)
        for test_name in DOMAIN_TESTS[domain]
    ]
    return tests, score_model(tests)


def main():
    parser = argparse.ArgumentParser(
        description="GAIA Collaborator Benchmark v2"
    )
    parser.add_argument(
        "--domain",
        default="home_assistant",
        choices=sorted(DOMAIN_TESTS),
    )
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    models = load_models()

    print("=== GAIA Collaborator Benchmark v2 ===")
    print(f"Domain: {args.domain}")

    for index, item in enumerate(models, start=1):
        name = item["name"]
        model = item["ollama"]

        print()
        print(f"MODEL {index}/{len(models)}: {name} -> {model}")

        try:
            metadata = ollama_show(model)
            print("capabilities:", metadata.get("capabilities", []))
        except Exception as exc:
            print(
                f"model verification failed: "
                f"{type(exc).__name__}: {exc}"
            )
            continue

        tests, summary = run_domain(model, args.domain)

        for result in tests:
            status = "PASS" if result["success"] else "FAIL"
            print(
                f"  {result['name']}: {status} "
                f"({result['elapsed_seconds']:.3f}s)"
            )

            for failure in result["verification"]["failures"]:
                print(f"    {failure}")

        document = {
            "benchmark_version": "0.2-collaborator",
            "domain": args.domain,
            "model_name": name,
            "ollama_model": model,
            "success": summary["score"] == 1.0,
            "score": summary["score"],
            "summary": summary,
            "tests": tests,
        }

        output = RESULTS_DIR / f"{name}.json"
        output.write_text(
            json.dumps(
                document,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        print(f"  saved: {output}")


if __name__ == "__main__":
    main()
