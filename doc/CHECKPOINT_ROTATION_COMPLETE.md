**Checkpoint: Token Rotation Ready**

Status: READY FOR OPERATOR ACTION

Summary:
- Code and helper scripts updated to use canonical `GAIA_GITHUB_TOKEN` with backward compatibility.
- Local validation and unit tests passed: `pytest` (116 passed, 1 skipped).
- Token-cache server validated in `GAIA_TEST_MODE` and returns `GAIA_GITHUB_TOKEN` when present.

Required manual operator steps (execute from repo root):

1) Persist new tokens to encrypted store

   - Prepare a short-lived admin token (do NOT paste it here).
   - Run the helper to write the token into the encrypted store (this mirrors legacy names):

     ```powershell
     # run locally in the repo; set ROTATION_ADMIN_TOKEN only in your shell
     $env:ROTATION_ADMIN_TOKEN = '<your-admin-token-local-only>'
     python scripts/rotate_tokens_helper.py --token '<new-GAIA_GITHUB_TOKEN-value>'
     ```

   - Alternatively, use the GitHub App flow (recommended) and call:

     ```powershell
     python scripts/github_app_token.py --app-id <APP_ID> --key-path .private/app.pem --installation-id <INSTALLATION_ID> --persist
     ```

2) (Optional) Update repository secrets via `gh` (if required):

   ```powershell
   gh secret set GAIA_GITHUB_TOKEN --body '<new-GAIA_GITHUB_TOKEN>' --repo <owner/repo>
   ```

3) Revoke temporary admin PAT

   - Revoke the temporary PAT used for rotation from https://github.com/settings/tokens or via `gh`:

     ```powershell
     # Example (requires gh authenticated as yourself):
     gh api --method DELETE /authorizations/<TOKEN_ID>
     ```

4) Update CI/workflows (if you want repository actions to read the new secret name):

   - Replace references to legacy secret names in `.github/workflows/*` with `secrets.GAIA_GITHUB_TOKEN` where appropriate.
   - Alternatively, mirror the secret in repository settings under the legacy name.

5) Create PR & merge

   - Create a PR with these repo changes and request review from the security owner.

Audit & verification
- After persisting tokens, run the validator locally:

  ```powershell
  $env:GAIA_TEST_MODE=1
  $env:GAIA_GITHUB_TOKEN='<new-GAIA_GITHUB_TOKEN-local-only>'
  python scripts/validate_consumers.py
  ```

Questions or issues: open an issue under `doc/ISSUES` or contact the repository owner.
