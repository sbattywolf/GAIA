import re
import os

if not os.path.exists('.gitmodules'):
    print('No .gitmodules file')
    raise SystemExit(0)

content = open('.gitmodules', 'r', encoding='utf-8').read()
sections = re.findall(r'\[submodule "([^"]+)"\]([\s\S]*?)(?=\n\[|\Z)', content)
out = []
removed = []
for name, body in sections:
    if re.search(r'\burl\s*=\s*.+', body):
        out.append(f'[submodule "{name}"]' + body)
    else:
        removed.append(name)
if removed:
    open('.gitmodules', 'w', encoding='utf-8').write('\n'.join(out) + ('\n' if out else ''))
    for n in removed:
        os.system(f"git config -f .git/config --remove-section submodule.{n} 2>/dev/null || true")
    print('Removed broken submodule entries:', removed)
else:
    print('No broken submodule entries found')
