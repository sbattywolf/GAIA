# Migrazione e rollback

## Uso dell'archivio

Questo ZIP non deve essere estratto direttamente sopra il repository senza controllo.

```bash
unzip zeus-project-blueprint-2026-07-30.zip -d /tmp/zeus-blueprint
diff -ruN ~/github_repos/home_assistant_framework /tmp/zeus-blueprint/zeus-project-blueprint-2026-07-30
```

Copiare una sola milestone alla volta.

## Branch

```bash
git switch -c feature/zeus-inventory-provider
git status --short
```

## Test e commit

```bash
python -m pytest -q
python -m py_compile 1070/app/*.py
git diff --check
git diff --stat
```

## Rollback

Prima del commit:

```bash
git restore -- 1070/app/<file>
```

Dopo il commit locale:

```bash
git revert <commit>
```

Non usare reset hard quando esistono file importanti non tracciati.
