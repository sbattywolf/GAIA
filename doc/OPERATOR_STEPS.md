Operator Steps — finalize rotation and CI updates

1) Persist tokens to encrypted store
- Use `scripts/rotate_tokens_helper.py` with `ROTATION_ADMIN_TOKEN` set in your shell.
- Verify `.private/secrets.enc` is updated and that `gaia.secrets.SecretsManager.get('GAIA_GITHUB_TOKEN')` returns the new token.

2) Mirror secrets to repository (optional)
- Use `gh secret set GAIA_GITHUB_TOKEN --body '<token>' --repo owner/repo` to add repo-level secret.

3) Update workflows (if needed)
- Search `.github/workflows` for any references to old variable names and replace them with `secrets.GAIA_GITHUB_TOKEN`.

4) Revoke temporary admin PAT
- Remove the PAT at https://github.com/settings/tokens once rotation is confirmed.

5) Run final validator
- Locally run `scripts/validate_consumers.py` without `GAIA_TEST_MODE` to ensure the token-cache and consumers work end-to-end.

6) Merge CHECKPOINT PR
- Create and merge a PR that documents these steps and includes the code changes in this branch.
