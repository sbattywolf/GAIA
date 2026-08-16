#!/usr/bin/env python3

import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
ENGINEER_RESULTS = BASE / "results"
COLLABORATOR_RESULTS = BASE / "collaborator" / "results"


def load_results(directory):
    results = []

    if not directory.exists():
        return results

    for path in sorted(directory.glob("*.json")):
        try:
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
            results.append(data)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"WARNING: cannot read {path}: {exc}")

    return results


def summarize(data):
    tests = data.get("tests", [])

    passed = sum(
        1 for test in tests
        if test.get("success") is True
    )

    total_time = sum(
        float(test.get("elapsed_seconds", 0))
        for test in tests
    )

    times = [
        (test.get("name"), float(test.get("elapsed_seconds", 0)))
        for test in tests
        if "elapsed_seconds" in test
    ]

    fastest = min(times, key=lambda x: x[1]) if times else ("-", 0)
    slowest = max(times, key=lambda x: x[1]) if times else ("-", 0)

    return {
        "model": data.get("model_name") or data.get("model"),
        "benchmark": data.get("benchmark_version"),
        "passed": passed,
        "total": len(tests),
        "success": data.get("success"),
        "total_time": total_time,
        "avg_time": total_time / len(tests) if tests else 0,
        "fastest": fastest,
        "slowest": slowest,
        "capabilities": data.get("capabilities", []),
    }


def print_table(title, rows):
    print()
    print("=" * 120)
    print(title)
    print("=" * 120)

    if not rows:
        print("No local result files found.")
        return

    print(
        f"{'MODEL':<28} | "
        f"{'PASS':>5} | "
        f"{'TIME(s)':>10} | "
        f"{'AVG(s)':>8} | "
        f"{'FASTEST':<28} | "
        f"{'SLOWEST':<28}"
    )

    print("-" * 120)

    for row in rows:
        fastest = (
            f"{row['fastest'][0]} "
            f"({row['fastest'][1]:.2f}s)"
        )
        slowest = (
            f"{row['slowest'][0]} "
            f"({row['slowest'][1]:.2f}s)"
        )

        print(
            f"{str(row['model']):<28} | "
            f"{row['passed']:>2}/{row['total']:<2} | "
            f"{row['total_time']:>10.2f} | "
            f"{row['avg_time']:>8.2f} | "
            f"{fastest:<28} | "
            f"{slowest:<28}"
        )


def main():
    engineer = load_results(ENGINEER_RESULTS)
    collaborator = load_results(COLLABORATOR_RESULTS)

    engineer_rows = [
        summarize(data)
        for data in engineer
        if data.get("model_name") or data.get("model")
    ]

    collaborator_rows = [
        summarize(data)
        for data in collaborator
        if data.get("model_name") or data.get("model")
    ]

    engineer_rows.sort(key=lambda x: x["model"])
    collaborator_rows.sort(key=lambda x: x["model"])

    print_table(
        "GAIA ENGINEER BENCHMARK",
        engineer_rows,
    )

    print_table(
        "GAIA COLLABORATOR BENCHMARK",
        collaborator_rows,
    )

    print()
    print("=" * 110)
    print("SUMMARY")
    print("=" * 110)

    print(
        f"Engineer results:     {len(engineer_rows)} models"
    )
    print(
        f"Collaborator results: {len(collaborator_rows)} models"
    )

    if collaborator_rows:
        passing = [
            row for row in collaborator_rows
            if row["passed"] == row["total"]
        ]

        print(
            f"Collaborator full-pass: "
            f"{len(passing)}/{len(collaborator_rows)}"
        )


if __name__ == "__main__":
    main()
