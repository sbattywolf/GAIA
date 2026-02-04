Using the provided git hook scripts

1. Make Git use the `.githooks` directory for hooks (recommended once per repo):

   ```sh
   git config core.hooksPath .githooks
   ```

2. The `pre-commit` hook runs `scripts/check_staged_secrets.py` and will block commits that stage `.private` or `.tmp` env files containing tokens.

3. On Windows, use PowerShell hook `pre-commit.ps1` which is included; set `core.hooksPath` similarly.

If you prefer a global solution, install a pre-commit framework and call `scripts/check_staged_secrets.py` from your pre-commit config.
