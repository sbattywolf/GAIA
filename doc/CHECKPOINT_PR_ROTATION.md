# CHECKPOINT: GitHub App creation & token rotation

This CHECKPOINT PR is a safety artifact to request operator approval before performing high-impact actions (creating App installs, persisting tokens, revoking PATs).

PR Title: CHECKPOINT: Create GitHub App for GAIA and rotate automation tokens

PR Description (paste):
```
This PR records the planned creation of a GitHub App (`GAIA-Automation`) and execution of the token rotation runbook.

Planned actions (operator will perform after approval):
1. Create GitHub App and download private key; record `APP_ID` and per-repo `INSTALLATION_ID`.
2. Install App on target repo(s) with minimal permissions as described in `doc/GITHUB_APP_CHECKLIST.md`.
3. Place private key at `.private/gaia_app.pem` on operator machine.
4. Run the rotation dry-run and validation:

   ```powershell
   # optional: set test mode
   $env:GAIA_TEST_MODE = '1'
   $env:GAIA_GITHUB_TOKEN = '<existing_or_test_token>'
   python scripts/rotate_and_persist_all.py --config rotation/consumers.json
   python scripts/validate_consumers.py
   ```

5. After successful validation, persist tokens (operator runs):

   ```powershell
   python scripts/rotate_and_persist_all.py --config rotation/consumers.json --key-path .private/gaia_app.pem --confirm
   ```

6. Update CI secrets and workflows to reference new canonical secrets (`GAIA_GITHUB_TOKEN`, `GAIA_CI_TOKEN`, etc.).
7. Revoke the temporary admin PAT used for the initial migration.

Audit: all token fetches and persistence will be recorded in `gaia.db` and `events.ndjson`.

Approval checklist (maintainer to verify):
- [ ] `rotation/consumers.json` contains correct installation IDs and secret names.
- [ ] Private key is stored securely and only accessible to operators performing rotation.
- [ ] Dry-run validation (`scripts/validate_consumers.py`) passed locally.
- [ ] CI change plan documented and rollback steps prepared.

If approved, the operator may merge and then perform the steps above; attach evidence (audit logs and `rotation/rotate_results.json`) to the PR before closing.
```

Safety notes:
- Do not commit real private keys. Use `.private/` local path and ensure it's in `.gitignore`.
- Create a `CHECKPOINT` PR and request at least one reviewer before running `--confirm` persistence.
