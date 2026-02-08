#!/usr/bin/env python3
import json
import os
import subprocess
import sys

def main():
    target_name = "Clawdis.app"
    minimum = 0.43

    report = json.loads(
        subprocess.check_output(
            ["xcrun", "xccov", "view", "--report", "--json", os.environ["RESULT_BUNDLE_PATH"]],
            text=True,
        )
    )

    target_coverage = None
    for target in report.get("targets", []):
        if target.get("name") == target_name:
            target_coverage = float(target["lineCoverage"])
            break

    if target_coverage is None:
        print(f"Could not find coverage for target: {target_name}")
        sys.exit(1)

    print(f"{target_name} line coverage: {target_coverage * 100:.2f}% (min {minimum * 100:.2f}%)")
    if target_coverage + 1e-12 < minimum:
        sys.exit(1)


if __name__ == '__main__':
    main()
