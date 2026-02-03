#!/usr/bin/env python3
"""Render an NDJSON todo archive into a simple SESSION_TODOS.md.

Usage:
  python scripts/session_todo.py --ndjson path\to\todo-archive.ndjson --out docs/SESSION_TODOS.md

If `--ndjson` is omitted and `Gaia/doc/todo-archive.ndjson` exists, it will be used.
"""
import argparse
import json
import os


def ndjson_to_md(ndjson_path, out_path):
    lines = []
    if not os.path.exists(ndjson_path):
        print('NDJSON archive not found:', ndjson_path)
        return
    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            try:
                obj = json.loads(l)
                title = obj.get('title') or obj.get('task') or obj.get('added_by')
                lines.append('- ' + (title if title else json.dumps(obj)))
            except Exception:
                lines.append('- ' + l)

    content = '# Session Todos\n\n' + '\n'.join(lines) + '\n'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Wrote', out_path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ndjson', help='Path to todo-archive.ndjson')
    p.add_argument('--out', default='docs/SESSION_TODOS.md')
    args = p.parse_args()

    ndjson = args.ndjson or os.path.join('Gaia', 'doc', 'todo-archive.ndjson')
    ndjson_to_md(ndjson, args.out)


if __name__ == '__main__':
    main()
