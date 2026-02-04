# Secrets Scanning

This project uses `detect-secrets` to detect accidental secret commits and prevent regressions.

Quick notes:

- Baseline file: `.secrets.baseline` (committed).
- CI job: `.github/workflows/secret-scan.yml` runs `detect-secrets scan --all-files --json` and fails if the scan finds files not present in the baseline.

To update the baseline locally (only when you have vetted the findings):

```bash
python -m pip install detect-secrets
detect-secrets scan > .secrets.baseline
git add .secrets.baseline && git commit -m "chore: update detect-secrets baseline"
```

If the CI job flags new files, review them carefully; do not add real secrets to the baseline. Instead rotate and remove any leaked credentials.
