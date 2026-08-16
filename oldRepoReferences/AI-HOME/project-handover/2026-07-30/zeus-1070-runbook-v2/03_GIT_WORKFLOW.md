# Git workflow for Milestone 3

After the Plan is approved and the bootstrap branch is clean:

```bash
git switch feature/zeus-1070-bootstrap
git pull --ff-only
git switch -c feature/zeus-ha-inventory-readonly
```

After Agent implementation, before commit:

```bash
git status --short
git diff --check
PYTHONPATH=1070/app python -m unittest discover -s 1070/tests -p 'test_*.py' -v
python -m py_compile 1070/app/*.py
```

Stage only the explicitly reviewed files. Never use `git add .`.

Suggested first-tranche commit only after review and runtime-independent tests:

```bash
git commit -m "feat(inventory): add read-only Home Assistant registry client"
```

Do not merge until the feature branch is tested on the 1070.
