#!/usr/bin/env python3
"""Generate per-feature/story .current.json and .draft.json files from doc/EPC_Telegram.current

Files created under `doc/` named like: EPC_Telegram.F-featureid.STORY_storykey.current.json
and corresponding `.draft.json` (copy of tasks; drafts used to record runtime errors/impediments).
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
EPIC = ROOT / 'doc' / 'EPC_Telegram.current'
OUT_DIR = ROOT / 'doc'


def extract_json_block(text: str) -> str:
    # split on a line containing only '---' (common separator)
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == '---':
            return '\n'.join(lines[:idx])
    # fallback: find first brace and try to balance braces
    start = text.find('{')
    if start == -1:
        raise ValueError('no JSON start')
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    raise ValueError('could not find JSON block')


def safe_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-\.]+", '_', s)


def main():
    text = EPIC.read_text(encoding='utf-8')
    # tolerant feature extraction via regex (handles malformed JSON)
    import re
    id_re = re.compile(r'"id"\s*:\s*"(F-[^"\s]+)"')
    name_re = re.compile(r'"name"\s*:\s*"([^"\n]+)"')
    ids = id_re.findall(text)
    names = name_re.findall(text)
    # pair ids -> names by first-appearance order
    features = []
    for i, fid in enumerate(ids):
        fname = names[i] if i < len(names) else fid
        features.append({'id': fid, 'name': fname})

    created = 0
    for f in features:
        fid = f.get('id')
        fname = f.get('name')
        # create a default story scaffold
        sk = 'stoy_auto'
        out_current = OUT_DIR / f'EPC_Telegram.{fid}.{sk}.current.json'
        out_draft = OUT_DIR / f'EPC_Telegram.{fid}.{sk}.draft.json'
        payload = {
            'epic': 'EPC_Telegram',
            'feature_id': fid,
            'feature_name': fname,
            'story_key': sk,
            'agent': 'assistant',
            'tasks': [],
        }
        out_current.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
        payload_draft = dict(payload)
        payload_draft['impediments'] = []
        out_draft.write_text(json.dumps(payload_draft, indent=2, ensure_ascii=False), encoding='utf-8')
        created += 2
    print(f'created {created} files (features discovered: {len(features)})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
