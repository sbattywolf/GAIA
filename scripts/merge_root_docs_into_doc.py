import os
import shutil
import zipfile
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOC_TARGET = os.path.join(ROOT, 'doc')
BACKUP_DIR = os.path.join(ROOT, '.backup')

# Candidate top-level doc filenames (common patterns)
CANDIDATES = [
    'README.md', 'README_RUNBOOK.md', 'README_SESSION.md', 'README_SESSION_CHECKLIST.md',
    'RELEASE_NOTE.md', 'PLAN.md', 'PLAN_AGENT_MODE.md', 'TODO.md', 'SCHEDULER_AUDIT.md',
    'CHECKPOINT_1.md', 'CHECKPOINT_2.md'
]

os.makedirs(BACKUP_DIR, exist_ok=True)

found = []
for f in CANDIDATES:
    p = os.path.join(ROOT, f)
    if os.path.exists(p):
        found.append(f)

if not found:
    print('No top-level candidate docs found; nothing to do.')
    raise SystemExit(0)

timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
zip_name = os.path.join(BACKUP_DIR, f'root_docs_backup_{timestamp}.zip')

# Create zip backup of found files
with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for f in found:
        full = os.path.join(ROOT, f)
        arcname = os.path.relpath(full, ROOT)
        zf.write(full, arcname)
print('Backup created:', zip_name)

moved = 0
appended = 0
errors = 0
os.makedirs(DOC_TARGET, exist_ok=True)

for fname in found:
    src = os.path.join(ROOT, fname)
    target = os.path.join(DOC_TARGET, fname)
    try:
        with open(src, 'rb') as sf:
            data = sf.read()
        try:
            text = data.decode('utf-8')
            is_text = True
        except Exception:
            is_text = False

        if os.path.exists(target):
            if is_text:
                with open(target, 'a', encoding='utf-8', errors='replace') as tf:
                    tf.write('\n\n---\n\n')
                    tf.write(f'<!-- Merged from root/{fname} on {timestamp} UTC -->\n\n')
                    tf.write(text)
                appended += 1
                print('appended into doc/:', fname)
            else:
                alt = target + '.from-root'
                with open(alt, 'wb') as tf:
                    tf.write(data)
                moved += 1
                print('copied binary as:', alt)
        else:
            with open(target, 'wb') as tf:
                tf.write(data)
            try:
                shutil.copystat(src, target, follow_symlinks=True)
            except Exception:
                pass
            moved += 1
            print('moved to doc/:', fname)
    except Exception as e:
        print('error processing', fname, e)
        errors += 1

# Remove originals
for fname in found:
    try:
        os.remove(os.path.join(ROOT, fname))
        print('removed original:', fname)
    except Exception as e:
        print('failed to remove', fname, e)

print('\nSummary:')
print('  backup:', zip_name)
print('  moved (new in doc/):', moved)
print('  appended to existing:', appended)
print('  errors:', errors)

if errors:
    raise SystemExit(2)
else:
    raise SystemExit(0)
