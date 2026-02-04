# Secrets Handling and Safe Storage

Goal: avoid losing secrets while keeping them secure and recoverable when you "switch on" a development environment.

Recommended approaches (ordered by security + convenience):

1) GitHub Secrets & Environments (recommended)
   - Store runtime secrets in GitHub: `Settings → Secrets` (repository or Environment-level).
   - Use `scripts/set_repo_secrets.ps1` to automate setting secrets with `gh secret set`.
   - CI and Actions will read secrets from `secrets.*` automatically; never commit raw values.

2) Encrypted secrets in-repo (auditable, safe to commit)
   - Use `sops` (Mozilla SOPS) with a KMS or `age` key to encrypt YAML/JSON files and commit the ciphertext to the repo.
   - Only the people/CI with the key can decrypt; great for infra/ops secrets that must be versioned.

3) Local-only secrets (developer convenience)
   - Keep an untracked `.env` file locally (we provide `.env.template` in repo).
   - Add `.env` to `.gitignore` to prevent accidental commits.

Local workflows we added to this repo
- `scripts/set_repo_secrets.ps1` — helper to set GitHub repo secrets via `gh` (already present).
- `scripts/load_env.ps1` — convenience helper to populate a local `.env` from environment variables or a protected store.
- `.secrets.baseline` + `docs/SECRETS.md` + `secret-scan.yml` — detect-secrets baseline and CI job to catch accidental secrets.

Quick setup (recommended):

1. Store production secrets in GitHub Secrets / Environments.
2. For developer-local secrets, copy the template:

```powershell
copy .env.template .env
# edit .env locally with your values
```

3. Prevent accidental commits: run `pre-commit install` (we added a `pre-commit` config to run `detect-secrets`).

If you want to keep encrypted secrets in the repo (SOPS):

1. Encrypt a file:

```bash
sops --encrypt --age <age-key> secrets.yaml > secrets.yaml.enc
git add secrets.yaml.enc
```

2. In CI, decrypt with the key made available to the runner.

If you'd like, I can implement a SOPS workflow or enable `git-crypt` for the repository — tell me which you prefer.
