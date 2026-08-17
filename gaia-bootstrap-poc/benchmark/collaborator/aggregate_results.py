#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
RESULTS_DIR = BASE / "results"


def load_results() -> dict[str, dict[str, dict]]:
    """Return results grouped as domain -> model -> JSON document."""
    grouped: dict[str, dict[str, dict]] = {}

    if not RESULTS_DIR.exists():
        return grouped

    for domain_dir in sorted(RESULTS_DIR.iterdir()):
        if not domain_dir.is_dir():
            continue

        domain = domain_dir.name
        grouped[domain] = {}

        for path in sorted(domain_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                print(f"WARNING: cannot read {path}: {exc}")
                continue

            model = data.get("model_name")
            if model:
                grouped[domain][model] = data

    return grouped


def percentage(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value * 100:5.1f}%"


def average(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def build_model_rows(grouped: dict[str, dict[str, dict]]) -> list[dict]:
    models = sorted(
        {
            model
            for domain_results in grouped.values()
            for model in domain_results
        }
    )

    rows = []

    for model in models:
        golden_values = []
        legacy_values = []
        domain_scores = {}

        for domain in sorted(grouped):
            data = grouped[domain].get(model)

            if data is None:
                domain_scores[domain] = None
                continue

            golden = data.get("golden_score")
            legacy = data.get("score")

            domain_scores[domain] = golden

            if isinstance(golden, (int, float)):
                golden_values.append(float(golden))

            if isinstance(legacy, (int, float)):
                legacy_values.append(float(legacy))

        rows.append(
            {
                "model": model,
                "domains": domain_scores,
                "golden_overall": average(golden_values),
                "legacy_overall": average(legacy_values),
                "domain_count": len(golden_values),
            }
        )

    return rows


def print_table(grouped: dict[str, dict[str, dict]], rows: list[dict]) -> None:
    domains = sorted(grouped)

    print()
    print("=" * 120)
    print("GAIA COLLABORATOR BENCHMARK v2")
    print("=" * 120)

    header = f"{'MODEL':<28}"
    for domain in domains:
        header += f"{domain[:18]:>20}"
    header += f"{'GOLDEN OVERALL':>18}{'LEGACY OVERALL':>18}"
    print(header)
    print("-" * len(header))

    for row in rows:
        line = f"{row['model']:<28}"

        for domain in domains:
            line += f"{percentage(row['domains'].get(domain)):>20}"

        line += f"{percentage(row['golden_overall']):>18}"
        line += f"{percentage(row['legacy_overall']):>18}"
        print(line)


def main() -> None:
    grouped = load_results()

    if not grouped:
        print("No collaborator result files found.")
        return

    rows = build_model_rows(grouped)
    rows.sort(
        key=lambda row: (
            row["golden_overall"] is None,
            -(row["golden_overall"] or 0.0),
            row["model"],
        )
    )

    print_table(grouped, rows)

    print()
    print("=" * 120)
    print("DOMAIN SUMMARY")
    print("=" * 120)

    for domain in sorted(grouped):
        values = [
            float(data["golden_score"])
            for data in grouped[domain].values()
            if isinstance(data.get("golden_score"), (int, float))
        ]
        print(
            f"{domain:<20}"
            f"models={len(grouped[domain]):<4}"
            f"golden_avg={percentage(average(values))}"
        )

    print()
    print(
        "Official metric: golden_score. "
        "Legacy score is retained for regression comparison."
    )


if __name__ == "__main__":
    main()
