#!/usr/bin/env python3
"""Validate JSON structure of todolist files under .tmp/todolists.

Checks:
- Each JSON object must have `story`, `story_key`, `type`, and `tasks` (list).
- Each task must have `id`, `title`, `description`, `status`, `priority`.

The script is tolerant of files containing multiple JSON objects concatenated back-to-back.
"""
import json
import sys
from pathlib import Path


def extract_json_objects(text):
    objs = []
    stack = []
    start = None
    for i, ch in enumerate(text):
        if ch == '{':
            if not stack:
                start = i
            stack.append('{')
        elif ch == '}':
            if stack:
                stack.pop()
                if not stack and start is not None:
                    block = text[start:i+1]
                    objs.append(block)
                    start = None
    return objs


def validate_obj(obj, path):
    errors = []
    # allow canonical index objects to have a different schema
    if 'canonical_tasks' in obj:
        return errors
    required_top = ['story', 'story_key', 'type', 'tasks']
    for k in required_top:
        if k not in obj:
            errors.append(f"missing top-level key '{k}'")
    if 'tasks' in obj:
        if not isinstance(obj['tasks'], list):
            errors.append("'tasks' is not a list")
        else:
            for idx, t in enumerate(obj['tasks']):
                if not isinstance(t, dict):
                    errors.append(f"task[{idx}] is not an object")
                    continue
                for tk in ('id', 'title', 'description', 'status', 'priority'):
                    if tk not in t:
                        errors.append(f"task[{idx}] missing '{tk}'")
    return errors


def main():
    base = Path('.').resolve() / '.tmp' / 'todolists'
    if not base.exists():
        print(f"No todolists directory at {base}")
        return 1
    files = list(base.glob('*'))
    total = 0
    total_errors = 0
    for p in files:
        if p.is_file():
            text = p.read_text(encoding='utf-8')
            objs = []
            try:
                # try single JSON
                objs = [json.loads(text)]
            except Exception:
                # try extracting multiple JSON objects
                blocks = extract_json_objects(text)
                for b in blocks:
                    try:
                        objs.append(json.loads(b))
                    except Exception as e:
                        print(f"{p}: failed parse of block: {e}")
                        total_errors += 1
            for o in objs:
                total += 1
                errs = validate_obj(o, p)
                if errs:
                    total_errors += len(errs)
                    print(f"{p} -> object with story_key={o.get('story_key','<no-key>')} errors:")
                    for e in errs:
                        print(f"  - {e}")
    print(f"Scanned {len(files)} files, {total} JSON objects, {total_errors} validation errors")
    return 1 if total_errors else 0


if __name__ == '__main__':
    sys.exit(main())
