#!/usr/bin/env python3
"""Count todo tasks in `doc/EPC_Telegram.current` (t* ids) and estimate which need external/manual interaction."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
EPIC = ROOT / 'doc' / 'EPC_Telegram.current'
text = EPIC.read_text(encoding='utf-8')

# find task ids and titles
task_re = re.compile(r'\{\s*"id"\s*:\s*"(t\w+)"\s*,\s*"title"\s*:\s*"([^"]+)"', re.I)
tasks = task_re.findall(text)

# fallback: find any "id": "t..." occurrences
if not tasks:
    id_re = re.compile(r'"id"\s*:\s*"(t[^"]+)"')
    tasks = [(m.group(1), '') for m in id_re.finditer(text)]

total = len(tasks)

external_keywords = ['gh', 'github', 'git', 'rotate', 'token', 'CI', 'ci', 'approve', 'manual', 'ui', 'integration', 'mocked', 'telegram', 'secrets', 'vault', 'bw', 'bitwarden']
needs_manual = 0
manual_list = []
for tid, title in tasks:
    combined = (tid + ' ' + title).lower()
    if any(k.lower() in combined for k in external_keywords):
        needs_manual += 1
        manual_list.append((tid, title))

print(total)
print(needs_manual)
for t in manual_list[:50]:
    print(t[0], '-', t[1])
