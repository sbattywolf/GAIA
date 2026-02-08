#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys


def main():
    root = pathlib.Path(".github/workflows")
    bad: list[str] = []
    for path in sorted(root.rglob("*.yml")):
        if b"\t" in path.read_bytes():
            bad.append(str(path))

    for path in sorted(root.rglob("*.yaml")):
        if b"\t" in path.read_bytes():
            bad.append(str(path))

    if bad:
        print("Tabs found in workflow file(s):")
        for path in bad:
            print(f"- {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
