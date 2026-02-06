# detect-secrets & pre-commit (quick start)

This document describes how to run `detect-secrets` locally and install the `pre-commit` hooks used by CI.

Install (recommended in a virtualenv):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install pre-commit detect-secrets
```

Create baseline (first run - inspect results before committing):

```powershell
detect-secrets scan > .secrets.baseline
# review .secrets.baseline and edit to remove false positives
```

Install pre-commit hooks locally:

```powershell
pre-commit install
pre-commit run --all-files
```

Notes:
- The repository includes `.pre-commit-config.yaml` configured to run `detect-secrets` using the `.secrets.baseline` file. Update the baseline after validating findings.
- CI should run `pre-commit run --all-files` as part of checks to prevent secrets from being committed.
