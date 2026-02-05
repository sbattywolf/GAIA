import os
import shutil
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOC = os.path.join(ROOT, 'doc')
ARCHIVE_ROOT = os.path.join(DOC, 'archive')

timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
ARCHIVE_DIR = os.path.join(ARCHIVE_ROOT, f'pre_restructure_{timestamp}')

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Move all files and top-level dirs inside doc/ except 'archive' and any already newly named directories
for entry in os.listdir(DOC):
    if entry in ('archive',):
        continue
    src = os.path.join(DOC, entry)
    dst = os.path.join(ARCHIVE_DIR, entry)
    try:
        shutil.move(src, dst)
        print('moved to archive:', entry)
    except Exception as e:
        print('skip/move-failed:', entry, e)

# Create new concise structure
new_dirs = [
    os.path.join(DOC, '01_onboarding'),
    os.path.join(DOC, '02_technical'),
    os.path.join(DOC, '03_procedural'),
    os.path.join(DOC, '04_reference'),
    os.path.join(DOC, '05_backlog'),
    os.path.join(DOC, '06_archives')
]
for d in new_dirs:
    os.makedirs(d, exist_ok=True)
    print('created dir', d)

# add a lightweight README placeholder
import os
import shutil
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOC = os.path.join(ROOT, 'doc')
ARCHIVE_ROOT = os.path.join(DOC, 'archive')

timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
ARCHIVE_DIR = os.path.join(ARCHIVE_ROOT, f'pre_restructure_{timestamp}')

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Move all files and top-level dirs inside doc/ except 'archive' and any already newly named directories
for entry in os.listdir(DOC):
    if entry in ('archive',):
        continue
    src = os.path.join(DOC, entry)
    dst = os.path.join(ARCHIVE_DIR, entry)
    try:
        shutil.move(src, dst)
        print('moved to archive:', entry)
    except Exception as e:
        print('skip/move-failed:', entry, e)

# Create new concise structure
new_dirs = [
    os.path.join(DOC, '01_onboarding'),
    os.path.join(DOC, '02_technical'),
    os.path.join(DOC, '03_procedural'),
    os.path.join(DOC, '04_reference'),
    os.path.join(DOC, '05_backlog'),
    os.path.join(DOC, '06_archives')
]
for d in new_dirs:
    os.makedirs(d, exist_ok=True)
    print('created dir', d)

# add a lightweight README placeholder
readme = os.path.join(DOC, 'MASTER_DOC_INDEX.md')
master_content = (
    '# MASTER_DOC_INDEX\n\n'
    'This document defines the new concise documentation structure, naming conventions and where archived material lives.\n\n'
    'Structure (top-level folders):\n\n'
    "- `01_onboarding` — what new contributors or agents need to get started. Minimal runnable steps.\n"
    "- `02_technical` — API specs, architecture, data models, design decisions.\n"
    "- `03_procedural` — runbooks, playbooks, operational procedures, approvals.\n"
    "- `04_reference` — configs, schemas, examples, CLI usage.\n"
    "- `05_backlog` — consolidated backlog and prioritized stories/tasks mapped to features.\n"
    "- `06_archives` — pointers to archived material (large/old docs) and historical notes.\n\n"
    'Naming convention (filename slug):\n\n'
    '`<category>-<feature-or-area>-<short-description>.md`\n\n'
    'Examples:\n\n'
    '- `technical-api-auth.md`\n'
    '- `procedural-deploy-release-checklist.md`\n'
    '- `onboarding-agent-quickstart.md`\n\n'
    'Archive policy:\n\n'
    '- All existing docs are moved to `doc/archive/pre_restructure_<timestamp>/` and left intact.\n'
    '- New documents should be concise, focused, and cross-referenced to archived originals when needed.\n\n'
    'Backlog approach:\n\n'
    '- The `05_backlog/MASTER_BACKLOG.md` will contain a single consolidated backlog grouped by feature, with links to archived detail documents and referenced GitHub issues.\n'
)
with open(readme, 'w', encoding='utf-8') as fh:
    fh.write(master_content)
print('created MASTER_DOC_INDEX.md')

# create an initial agent onboarding doc
onboard = os.path.join(DOC, '01_onboarding', 'AGENT_START.md')
agent_text = (
    '# Agent Start: Quick onboarding for a new agent\n\n'
    'This is the first document a new automated agent or human should read to start contributing.\n\n'
    '1. Environment\n'
    '   - Python 3.11 recommended. Use virtualenv: `python -m venv .venv` then activate.\n'
    '   - Install dev deps: `pip install -r requirements-dev.txt`.\n'
    '2. Repository layout\n'
    '   - `agents/` — agent scripts and CLI helpers.\n'
    '   - `doc/` — canonical docs (this folder). Archived originals are under `doc/archive/`.\n'
    '   - `orchestrator.py` & `gaia.db` — local audit DB used by agents for traceability.\n'
    '3. Quick run: discover backlog (dry-run)\n\n'
    '```powershell\n'
    'python agents/telegram_backlog_agent.py --dry-run --limit 20\n'
    '```\n\n'
    '4. Creating issues from NDJSON (manual step requires review)\n\n'
    '```powershell\n'
    'python .tmp/create_issues.py .tmp/issues.ndjson --confirm\n'
    '```\n\n'
    '5. Where to look for more detail\n'
    '   - Detailed playbooks and runbooks: `doc/03_procedural/` (or archived originals under `doc/archive/`)\n'
)
with open(onboard, 'w', encoding='utf-8') as fh:
    fh.write(agent_text)
print('created AGENT_START.md')

# create backlog placeholder
backlog = os.path.join(DOC, '05_backlog', 'MASTER_BACKLOG.md')
backlog_text = (
    '# MASTER_BACKLOG\n\n'
    'This is the consolidated backlog organized by feature area. Populate with high-level entries mapping to issues and archived documents.\n\n'
    '- Feature: CI reliability\n'
    '  - Task: Ensure artifacts always upload on failure (see archived: doc/archive/...)\n'
    '  - GitHub Issues: #54, #55\n\n'
    '- Feature: Agent onboarding\n'
    '  - Task: Finalize Telegram agent MVP and approval flow (see archived: doc/archive/TELEGRAM_SETUP.md)\n\n'
    '- Feature: Backlog automation\n'
    '  - Task: Convert NDJSON backlog discovery to issues and audit to `gaia.db`.\n\n'
    '(Use this file to record prioritized items; link to issues and archived docs.)\n'
)
with open(backlog, 'w', encoding='utf-8') as fh:
    fh.write(backlog_text)
print('created MASTER_BACKLOG.md')

print('\nDone: archival and scaffolding complete.')
