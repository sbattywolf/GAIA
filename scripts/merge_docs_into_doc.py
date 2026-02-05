import os
import shutil
import zipfile
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS_SRC = os.path.join(ROOT, 'docs')
DOC_TARGET = os.path.join(ROOT, 'doc')
BACKUP_DIR = os.path.join(ROOT, '.backup')

os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
zip_name = os.path.join(BACKUP_DIR, f'docs_backup_{timestamp}.zip')

if not os.path.exists(DOCS_SRC):
    print('No docs/ folder found; nothing to do.')
    raise SystemExit(0)

# Create zip backup
with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(DOCS_SRC):
        for f in files:
            full = os.path.join(root, f)
            arcname = os.path.relpath(full, ROOT)
            zf.write(full, arcname)
print('Backup created:', zip_name)

moved = 0
appended = 0
errors = 0

for root, dirs, files in os.walk(DOCS_SRC):
    rel_root = os.path.relpath(root, DOCS_SRC)
    if rel_root == '.':
        rel_root = ''
    for fname in files:
        src_path = os.path.join(root, fname)
        relative_subpath = os.path.join(rel_root, fname) if rel_root else fname
        target_dir = os.path.join(DOC_TARGET, rel_root) if rel_root else DOC_TARGET
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, fname)
        try:
            # Try text copy/merge
            with open(src_path, 'rb') as f:
                data = f.read()
            try:
                text = data.decode('utf-8')
                is_text = True
            except Exception:
                is_text = False

            if os.path.exists(target_path):
                if is_text:
                    with open(target_path, 'a', encoding='utf-8', errors='replace') as tf:
                        tf.write('\n\n---\n\n')
                        tf.write(f'<!-- Merged from docs/{relative_subpath} on {timestamp} UTC -->\n\n')
                        tf.write(text)
                    appended += 1
                    print('appended:', relative_subpath)
                else:
                    # For binary, keep both by writing with suffix
                    alt_target = target_path + '.from-docs'
                    with open(alt_target, 'wb') as tf:
                        tf.write(data)
                    moved += 1
                    print('copied-binary-as:', alt_target)
            else:
                # create new target (preserve metadata)
                with open(target_path, 'wb') as tf:
                    tf.write(data)
                try:
                    shutil.copystat(src_path, target_path, follow_symlinks=True)
                except Exception:
                    pass
                moved += 1
                print('moved:', relative_subpath)
        except Exception as e:
            print('error processing', src_path, e)
            errors += 1

# Remove original docs folder if everything processed
try:
    shutil.rmtree(DOCS_SRC)
    print('Removed original docs/ folder')
except Exception as e:
    print('Failed to remove docs/:', e)

print('\nSummary:')
print('  backup:', zip_name)
print('  files moved (new):', moved)
print('  files appended to existing:', appended)
print('  errors:', errors)

if errors:
    raise SystemExit(2)
else:
    raise SystemExit(0)
