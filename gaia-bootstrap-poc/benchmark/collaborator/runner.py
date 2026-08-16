#!/usr/bin/env python3

import json
import sys
import time
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent
BENCHMARK_DIR = BASE_DIR.parent
TESTS_DIR = BASE_DIR / "tests"
RESULTS_DIR = BASE_DIR / "results"
MODELS_FILE = BASE_DIR / "models.yaml"

OLLAMA_URL = "http://localhost:11434"

sys.path.insert(0, str(BENCHMARK_DIR))

from telemetry import TelemetrySession
from collaborator.verifier import verify_response


TESTS = [
    "C01_intent_recognition",
    "C02_tool_selection",
    "C03_home_assistant_action",
    "C04_invalid_entity",
    "C05_ambiguous_request",
    "C06_multiturn_state",
]


def load_models():
    data = yaml.safe_load(
        MODELS_FILE.read_text(encoding="utf-8")
    )
    return data.get("models", [])


def load_test(name):
    path = TESTS_DIR / f"{name}.md"

    if not path.exists():
        raise FileNotFoundError(path)

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

    if isinstance(calls, list):
        return calls

    return []


def run_test(model, test_name):
    prompt = load_test(test_name)

    telemetry = TelemetrySession()
    telemetry.start()

    start = time.monotonic()

    try:
        data = ollama_generate(model, prompt)

        elapsed = round(
            time.monotonic() - start,
            3,
        )

        response = data.get("response", "")
        tool_calls = extract_tool_calls(data)

        verification = verify_response(
            test_name,
            response,
            actual_tool_calls=len(tool_calls),
        )

    except Exception as exc:
        elapsed = round(
            time.monotonic() - start,
            3,
        )

        response = ""
        tool_calls = []

        verification = {
            "success": False,
            "failures": [
                f"runner error: {type(exc).__name__}: {exc}"
            ],
        }

    finally:
        telemetry.stop()

    return {
        "name": test_name,
        "success": verification["success"],
        "elapsed_seconds": elapsed,
        "tool_calls": tool_calls,
        "verification": verification,
        "telemetry": telemetry.result(),
        "response": response,
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    models = load_models()

    print("=== GAIA Collaborator Benchmark v0.1 ===")
    print(f"Repository: {BENCHMARK_DIR.parent}")

    print()
    print("Models:")

    for item in models:
        print(
            f"  {item['name']} -> {item['ollama']}"
        )

    for index, item in enumerate(models, start=1):
        name = item["name"]
        model = item["ollama"]

        print()
        print("=" * 72)
        print(f"MODEL {index}/{len(models)}: {name}")
        print(f"OLLAMA: {model}")
        print("=" * 72)

        try:
            metadata = ollama_show(model)
            capabilities = metadata.get("capabilities", [])
        except Exception as exc:
            print(
                f"  model verification failed: "
                f"{type(exc).__name__}: {exc}"
            )
            continue

        print("  capabilities:", capabilities)

        tests = []

        for test_name in TESTS:
            print(f"  TEST: {test_name}")

            result = run_test(model, test_name)
            tests.append(result)

            status = (
                "PASS"
                if result["success"]
                else "FAIL"
            )

            print(
                f"  {test_name}: {status} "
                f"({result['elapsed_seconds']:.3f}s)"
            )

            for failure in result["verification"]["failures"]:
                print(f"      {failure}")

        overall_success = all(
            test["success"]
            for test in tests
        )

        result_document = {
            "benchmark_version": "0.1-collaborator",
            "model_name": name,
            "ollama_model": model,
            "model_verified": True,
            "success": overall_success,
            "tests": tests,
        }

        output = (
            RESULTS_DIR
            / f"{name}.json"
        )

        output.write_text(
            json.dumps(
                result_document,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        print(f"  saved: {output}")

    print()
    print("=" * 72)
    print("COLLABORATOR BENCHMARK COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
