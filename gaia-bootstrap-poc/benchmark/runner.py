#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml
import requests

from telemetry import TelemetrySession


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = Path(__file__).resolve().parent
TESTS_DIR = BENCHMARK_DIR / "tests"
RESULTS_DIR = BENCHMARK_DIR / "results"
MODELS_FILE = BENCHMARK_DIR / "models.yaml"

OLLAMA_URL = "http://localhost:11434"

TESTS = [
    {
        "name": "T01_read_agents",
        "required_tools": ["read_file"],
    },
    {
        "name": "T02_precise_retrieval",
        "required_tools": ["read_file"],
    },
    {
        "name": "T03_architecture_evidence",
        "required_tools": ["search"],
    },
    {
        "name": "T04_evidence_verification",
        "required_tools": ["search"],
    },
    {
        "name": "T05_adr_status_and_gate",
        "required_tools": ["read_file", "search"],
    },
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


def ollama_generate(model, prompt, collect_model_metrics=False):
    """
    Uses the Ollama chat API with the benchmark tool definitions.

    The actual tool loop is intentionally simple:
    model -> tool call -> tool result -> model.
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from the repository.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filePath": {
                            "type": "string"
                        },
                        "startLine": {
                            "type": "integer"
                        },
                        "endLine": {
                            "type": "integer"
                        },
                    },
                    "required": ["filePath"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search",
                "description": "Search the repository for text or a pattern.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string"
                        },
                        "path": {
                            "type": "string"
                        },
                    },
                    "required": ["pattern"],
                },
            },
        },
    ]

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    tool_calls = []

    model_metrics = {
        "request_count": 0,
        "prompt_tokens": 0,
        "output_tokens": 0,
        "prompt_eval_duration_ns": 0,
        "eval_duration_ns": 0,
        "load_duration_ns": 0,
        "total_duration_ns": 0,
    } if collect_model_metrics else None

    for _ in range(20):
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "tools": tools,
                "stream": False,
            },
            timeout=600,
        )

        response.raise_for_status()
        data = response.json()

        if collect_model_metrics:
            model_metrics["request_count"] += 1

            for key in (
                "prompt_eval_count",
                "eval_count",
                "prompt_eval_duration",
                "eval_duration",
                "load_duration",
                "total_duration",
            ):
                value = data.get(key)

                if value is None:
                    continue

                if key == "prompt_eval_count":
                    model_metrics["prompt_tokens"] += value
                elif key == "eval_count":
                    model_metrics["output_tokens"] += value
                elif key == "prompt_eval_duration":
                    model_metrics["prompt_eval_duration_ns"] += value
                elif key == "eval_duration":
                    model_metrics["eval_duration_ns"] += value
                elif key == "load_duration":
                    model_metrics["load_duration_ns"] += value
                elif key == "total_duration":
                    model_metrics["total_duration_ns"] += value

        message = data.get("message", {})

        messages.append(message)

        calls = message.get("tool_calls") or []

        if not calls:
            return {
                "response": message.get("content", ""),
                "tool_calls": tool_calls,
                "model_metrics": (
                    finalize_model_metrics(model_metrics)
                    if collect_model_metrics
                    else None
                ),
            }

        for call in calls:
            function = call.get("function", {})
            name = function.get("name")
            arguments = function.get("arguments", {})

            tool_calls.append(
                {
                    "name": name,
                    "arguments": arguments,
                }
            )

            result = execute_tool(name, arguments)

            messages.append(
                {
                    "role": "tool",
                    "content": result,
                }
            )

    return {
        "response": "",
        "tool_calls": tool_calls,
        "model_metrics": (
            finalize_model_metrics(model_metrics)
            if collect_model_metrics
            else None
        ),
        "error": "maximum tool iterations exceeded",
    }


def finalize_model_metrics(metrics):
    eval_duration = metrics["eval_duration_ns"]
    prompt_duration = metrics["prompt_eval_duration_ns"]

    output_tokens = metrics["output_tokens"]
    prompt_tokens = metrics["prompt_tokens"]

    return {
        **metrics,
        "prompt_tokens_per_second": (
            prompt_tokens / (prompt_duration / 1_000_000_000)
            if prompt_duration > 0
            else None
        ),
        "output_tokens_per_second": (
            output_tokens / (eval_duration / 1_000_000_000)
            if eval_duration > 0
            else None
        ),
    }


def execute_tool(name, arguments):
    if name == "read_file":
        return execute_read_file(arguments)

    if name == "search":
        return execute_search(arguments)

    return json.dumps(
        {
            "error": f"unknown tool: {name}"
        }
    )


def execute_read_file(arguments):
    file_path = arguments.get("filePath")

    if not file_path:
        return json.dumps(
            {"error": "filePath is required"}
        )

    path = (ROOT / file_path).resolve()

    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return json.dumps(
            {"error": "path outside repository"}
        )

    if not path.exists() or not path.is_file():
        return json.dumps(
            {"error": "file not found"}
        )

    lines = path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    start = arguments.get("startLine", 1)
    end = arguments.get(
        "endLine",
        len(lines),
    )

    start = max(1, start)
    end = min(len(lines), end)

    selected = lines[start - 1:end]

    return "\n".join(
        f"{i}: {line}"
        for i, line in enumerate(
            selected,
            start=start,
        )
    )


def execute_search(arguments):
    pattern = arguments.get("pattern", "")
    relative_path = arguments.get("path", "")

    base = (
        ROOT / relative_path
        if relative_path
        else ROOT
    )

    try:
        base = base.resolve()
        base.relative_to(ROOT.resolve())
    except ValueError:
        return json.dumps(
            {"error": "path outside repository"}
        )

    if not base.exists():
        return json.dumps(
            {"error": "search path not found"}
        )

    try:
        result = subprocess.run(
            [
                "grep",
                "-R",
                "-n",
                "-I",
                "--exclude-dir=.git",
                pattern,
                str(base),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return json.dumps(
            {"error": "search timeout"}
        )

    output = result.stdout

    # Prevent enormous tool results.
    if len(output) > 30000:
        output = output[:30000]

    return output


def verify_model_running(expected_model):
    result = subprocess.run(
        ["ollama", "ps"],
        capture_output=True,
        text=True,
    )

    output = result.stdout

    return {
        "verified": expected_model in output,
        "output": output,
    }


def stop_model(model):
    subprocess.run(
        ["ollama", "stop", model],
        capture_output=True,
        text=True,
        timeout=60,
    )


def verify_tools(test, tool_calls):
    required = set(test["required_tools"])
    actual = {
        call["name"]
        for call in tool_calls
    }

    missing = sorted(required - actual)

    return {
        "required_tools": sorted(required),
        "actual_tools": sorted(actual),
        "missing_tools": missing,
        "tool_use_pass": len(missing) == 0,
    }


def run_test(model, test, collect_model_metrics=False):
    name = test["name"]
    prompt = load_test(name)

    print(f"  TEST: {name}")

    start = time.time()

    telemetry = TelemetrySession(
        interval_seconds=2.0
    )
    telemetry.start()

    result = ollama_generate(
        model,
        prompt,
        collect_model_metrics=collect_model_metrics,
    )

    telemetry.sample()
    telemetry.stop()

    elapsed = time.time() - start

    tool_calls = result.get(
        "tool_calls",
        [],
    )

    tool_verification = verify_tools(
        test,
        tool_calls,
    )

    success = (
        "error" not in result
        and tool_verification["tool_use_pass"]
    )

    print(
        f"  {name}: "
        f"{'PASS' if success else 'FAIL'} "
        f"({elapsed:.3f}s)"
    )

    if not tool_verification["tool_use_pass"]:
        print(
            "      missing tools:",
            tool_verification["missing_tools"],
        )

    return {
        "name": name,
        "success": success,
        "elapsed_seconds": round(
            elapsed,
            3,
        ),
        "tool_calls": tool_calls,
        "tool_verification": tool_verification,
        "telemetry": telemetry.result(),
        "model_metrics": result.get(
            "model_metrics"
        ),
        "response": result.get(
            "response",
            "",
        ),
        "error": result.get("error"),
    }


def run_model(model_info, index, total, collect_model_metrics=False):
    name = model_info["name"]
    ollama_model = model_info["ollama"]

    print()
    print("=" * 72)
    print(
        f"MODEL {index}/{total}: {name}"
    )
    print(
        f"OLLAMA: {ollama_model}"
    )
    print("=" * 72)

    metadata = ollama_show(
        ollama_model
    )

    capabilities = metadata.get(
        "capabilities",
        [],
    )

    print(
        "  capabilities:",
        capabilities,
    )

    verification = verify_model_running(
        ollama_model
    )

    tests = []

    for test in TESTS:
        result = run_test(
            ollama_model,
            test,
            collect_model_metrics=collect_model_metrics,
        )
        tests.append(result)

    overall_success = all(
        test["success"]
        for test in tests
    )

    output = {
        "benchmark_version": "1.2-tool-validation",
        "model_name": name,
        "ollama_model": ollama_model,
        "capabilities": capabilities,
        "model_verification": verification,
        "success": overall_success,
        "tests": tests,
    }

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        RESULTS_DIR
        / f"{name}.json"
    )

    output_path.write_text(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        "  saved:",
        output_path,
    )

    print(
        "  stopping model..."
    )

    stop_model(
        ollama_model
    )

    post_stop = verify_model_running(
        ollama_model
    )

    print(
        "  post-stop verification:",
        "OK"
        if not post_stop["verified"]
        else "WARNING",
    )


def main():
    parser = argparse.ArgumentParser(
        description="GAIA Engineer Benchmark"
    )
    parser.add_argument(
        "--performance",
        action="store_true",
        help="Collect Ollama model performance metrics.",
    )
    args = parser.parse_args()

    print(
        "=== GAIA Engineer Benchmark v1.2 ==="
    )

    print(
        "Repository:",
        ROOT,
    )

    models = load_models()

    print()
    print("Models:")

    for model in models:
        print(
            f"  {model['name']} -> "
            f"{model['ollama']}"
        )

    for index, model in enumerate(
        models,
        start=1,
    ):
        run_model(
            model,
            index,
            len(models),
            collect_model_metrics=args.performance,
        )

    print()
    print("=" * 72)
    print("BENCHMARK COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
