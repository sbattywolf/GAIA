SECRETS ROTATION & REMOVAL
=========================

Immediate actions if a secret/token may be exposed (recommended order)

1) Revoke the token now (do this first)

- Web UI (personal access tokens):
  - Open: https://github.com/settings/tokens
  - Revoke the token that appears to have been leaked.

- If it's a repository Actions secret (or other repo secret):
  - Open: Repository -> Settings -> Secrets and variables -> Actions
  - Remove the secret entry (e.g. `MY_TOKEN`) and replace with a new one.

2) Remove the secret from local files (safe local cleanup)

PowerShell (recommended on Windows):

```powershell
# Option A: blank the variable line in place
(Get-Content .private/.env) -replace 'GITHUB_TOKEN=.*','GITHUB_TOKEN=' | Set-Content .private/.env

# Option B: securely remove the file if you don't need it locally
Remove-Item -Path .private/.env -Force
```

POSIX (Git Bash / WSL):

```bash
# blank the variable
sed -i 's/^GITHUB_TOKEN=.*/GITHUB_TOKEN=/' .private/.env
# or remove the file
rm -f .private/.env
```

3) Rotate the token (create a new one with least privilege)

- Personal access token (if applicable): create a new PAT in GitHub at https://github.com/settings/tokens
  - Scope: grant the minimum scopes required (avoid full `repo` if not needed). Prefer `repo:public_repo` or narrow Actions scopes.

- Update CI / repo secrets: use the GitHub web UI or `gh` CLI.

Using `gh` CLI to set/remove repo secrets:

```bash
# Remove an existing secret
gh secret remove MY_TOKEN -R owner/repo

# Add a new secret from stdin
echo "NEW_TOKEN_VALUE" | gh secret set MY_TOKEN -R owner/repo
```

Note: Replace `owner/repo` with your repository path.

4) Confirm no accidental commits contain the secret

- Quick local checks:

```bash
# search working tree
git grep -n "ghp_" || true

# search recent commits for text
git log -S"ghp_" --pretty=format:"%h %ad %s" --date=iso -n 50 || true
```

If the token appears in any past commit that was pushed, proceed to history cleanup (next section).

5) (Optional / only if pushed) Remove secret from Git history safely

High-level safe process (requires coordination because history rewrite forces collaborators to rebase):

- Create a backup mirror of the repo (do not skip):

```bash
# make a bare mirror backup
git clone --mirror https://github.com/OWNER/REPO.git repo-backup.git
cd repo-backup.git
git remote add backup /path/to/local/backup.git || true
git push --mirror backup
```

- Recommended tool: `git filter-repo` (very fast and reliable). Install it first.
  - pip install --user git-filter-repo

- Example: replace exact token occurrences using a replacements file.

Create `replacements.txt` with the following content (replace the token string):

```
replace-text
# replace the leaked token with [REDACTED]
literal:[REDACTED_GITHUB_TOKEN]==>[REDACTED]
```

Then run in a fresh clone (NOT your main working copy):

```bash
git clone --mirror https://github.com/OWNER/REPO.git repo-filter.git
cd repo-filter.git
# run filter-repo replacement
git filter-repo --replace-text ../replacements.txt

# inspect refs and verify replacements occurred
git log --all --grep='ghp_D8oxId' || true

# push to origin (force) — DO NOT DO THIS UNTIL TEAM AGREES
git push --force --mirror origin
```

Important: coordinate with all collaborators before pushing rewritten history. Provide instructions for everyone to reclone or rebase.

Alternative tool: BFG repo cleaner (simpler UI) — uses `bfg --replace-text` similarly.

6) Run detect-secrets and pre-commit checks

- Run local scan with `detect-secrets` if configured:

```bash
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

- Run `pre-commit` locally to ensure hooks catch accidental secrets:

```bash
pip install pre-commit
pre-commit run --all-files
```

7) Post-rotation verification

- Verify new token works only for intended flows (CI jobs, CLI) and that old token is revoked.
- Check GitHub Actions runs that use the token; if you rotated a PAT used by Actions, update the repo secret and re-run workflows.

8) Emergency contact & communication

- Inform your team and maintain a short incident note describing what was rotated, what remains to do (history rewrite), and when a forced push will occur (if planned).

Appendix: Quick checklist

- [ ] Revoke leaked token in GitHub settings
- [ ] Remove token from local files (`.private/.env`) or delete file
- [ ] Create new token with least privilege
- [ ] Update Actions/Secrets via web UI or `gh secret set`
- [ ] Search commits; if leaked in pushed commits, prepare history rewrite (backup, test, force-push)
- [ ] Run `detect-secrets` and `pre-commit` hooks
- [ ] Notify team and coordinate any forced history rewrite

If you want, I can:

- Generate the exact `replacements.txt` for `git filter-repo` using the token value you supplied (I will not run the rewrite without explicit confirmation).
- Prepare a PowerShell one-liner to blank/remove `.private/.env` on your machine and run local detect-secrets.
- Prepare the `gh` commands to remove and re-create repository secrets for your repo (I will need the `owner/repo` name).

