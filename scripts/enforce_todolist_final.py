#!/usr/bin/env python3
"""Validate and optionally finalize managed .current todo lists.

Checks that the last non-empty task in each `.tmp/todolists/*.current` file
contains an explicit finalization marker (case-insensitive) such as
`MANDATORY`, `FINAL`, or `finalization`. Optionally create a `.finalized`
marker file to signal enforcement to operators.

Usage:
  python scripts/enforce_todolist_final.py --validate
  python scripts/enforce_todolist_final.py --finalize
"""
import argparse
import glob
import os
import sys


def check_file(path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # If file is JSON-like (dict with tasks), parse and extract last task title
    try:
        obj = json.loads(text)
        tasks = obj.get("tasks") if isinstance(obj, dict) else None
        if tasks and isinstance(tasks, list) and len(tasks) > 0:
            last_task = tasks[-1]
            last = last_task.get("title") or last_task.get("id") or str(last_task)
        else:
            # fall back to text scan
            raise ValueError("no-json-tasks")
    except Exception:
        lines = [l.rstrip() for l in text.splitlines()]
        # find last non-empty, non-code fence line
        for ln in reversed(lines):
            if not ln:
                continue
            if ln.strip().startswith("```"):
                continue
            # consider task lines starting with -, *, or a digit
            if ln.strip().startswith(('-', '*')) or (ln.strip() and ln.strip()[0].isdigit()):
                last = ln.strip()
                break
            last = ln.strip()
            break
        else:
            return False, "no-content"

    marker_words = ["MANDATORY", "FINAL", "FINALIZATION"]
    up = (last or "").upper()
    for m in marker_words:
        if m in up:
            return True, last
    return False, last


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--validate", action="store_true")
    p.add_argument("--finalize", action="store_true")
    args = p.parse_args(argv)

    base = os.path.join(".tmp", "todolists")
    files = glob.glob(os.path.join(base, "*.current"))
    if not files:
        print("no .current todo lists found under .tmp/todolists", file=sys.stderr)
        return 2

    ok_all = True
    for path in files:
        ok, last = check_file(path)
        print(f"{os.path.relpath(path)}: last='{last}' -> {'OK' if ok else 'MISSING'}")
        if not ok:
            ok_all = False
        if ok and args.finalize:
            marker = path + ".finalized"
            try:
                with open(marker, "w", encoding="utf-8") as f:
                    f.write("finalized\n")
                print(f"created: {os.path.relpath(marker)}")
            except Exception as e:
                print(f"failed creating marker {marker}: {e}", file=sys.stderr)
                ok_all = False

    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
