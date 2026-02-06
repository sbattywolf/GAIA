# CHECKPOINT: Token Rotation (temporary admin -> least-privilege tokens)

Status: DRAFT — awaiting approval

Purpose
- Use a short-lived admin token to generate and install least-privilege tokens
- Store new tokens in the encrypted secrets store and update repo/CI secrets
- Revoke the temporary admin token after validation

Preconditions
- A short-lived admin token has been created and provided to the operator.
- Local environment is running in the GAIA repo root and Python venv is active.

Steps (operator)
1. Verify connectivity and that `gh` is available if repo secret updates are desired.
2. Run the helper to store the admin token locally (recommended):

   ROTATION_ADMIN_TOKEN=<token> python scripts/rotate_tokens_helper.py

3. Optionally update repository secret (owner/repo) via `gh`:

   ROTATION_ADMIN_TOKEN=<token> python scripts/rotate_tokens_helper.py --use-gh --repo myorg/GAIA

4. Generate least-privilege tokens in GitHub (manual step - use GitHub UI or fine-grained tokens), store them with the `SecretsManager` using the canonical name `GAIA_GITHUB_TOKEN` or per-role names.
5. Run validation of services that consume tokens (CI runs, agents requiring API access).
6. Revoke the short-lived admin token in GitHub and record the revocation in the audit log.

Approval
- Approver: ______________________
- Signature: ______________________
- Date: __________________________

Notes
- The `SecretsManager` has aliasing: `GAIA_GITHUB_TOKEN` falls back to `AUTOMATION_GITHUB_TOKEN` and `GITHUB_TOKEN` for compatibility.
- Use `scripts/rotate_tokens_helper.py` to persist the token to the encrypted store; the script will also mirror to legacy key names.
