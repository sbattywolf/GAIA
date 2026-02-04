# Token Rotation Recommendations (future improvements)

This document collects free/open-source tools, recommended rotation patterns, and sample commands/workflows you can evaluate and adopt for rotating tokens, API keys, and passwords used by CI, agents, and deployments.

## Recommended OSS / Free Tools
- HashiCorp Vault (OSS): dynamic secrets, leases, automatic revocation. Good for DB/cloud creds and programmatic rotation.
- Bitwarden (self-hosted + CLI `bw`): team vault, credential generation, CLI automation for pushing secrets to CI.
- Mozilla SOPS + `age` / cloud KMS: encrypt secrets stored in git (GitOps-friendly).
- pass / gopass: lightweight password store for developer machines and CI runners.
- GitHub Actions Secrets + GH CLI (`gh secret set`): quick, free store for Actions workflows (rotate via script).
- Doppler (free tier): centralized secrets manager with integrations (easy onboarding).

## Rotation Patterns
- Prefer short-lived credentials (Vault leases, cloud IAM tokens, short-lived PATs) where possible.
- Automate: generate new secret → inject into runtime (CI or service) → smoke-test with new secret → revoke old secret.
- Treat rotation as a two-step swap: publish new, verify, then revoke old. Always have rollback steps and monitoring.

## Example commands (copyable)

Generate a cryptographically strong token locally:
```bash
openssl rand -base64 32
# or
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Push a token to GitHub Actions secrets with `gh`:
```bash
gh auth login
gh secret set MY_TOKEN --body "$(openssl rand -base64 32)"
```

Bitwarden CLI (generate + store):
```bash
bw login                        # interactive or use API key
TOKEN=$(bw generate --length 40 --symbols=false)
bw create item Login --name "ci-token" --password "$TOKEN"
```

SOPS encrypt/decrypt (age):
```bash
sops -e --age <AGE_KEY> secrets.yaml > secrets.enc.yaml
sops -d secrets.enc.yaml
```

Vault (example, high-level):
```bash
vault login <token>
vault read database/creds/myrole
# or write a new role/rotation policy and request creds on-demand
```

## GitHub Actions rotation job scaffold

This example job generates a new token, sets it as a repository secret, runs a smoke-check workflow, and (optionally) revokes the old token after verification. It assumes `GITHUB_TOKEN` or a service account with `secrets` permissions and `gh` is available in the runner.

```yaml
name: rotate-secret
on:
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * 0'  # weekly example

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - name: Generate token
        id: gen
        run: |
          NEW_TOKEN=$(openssl rand -base64 32)
          echo "NEW_TOKEN=$NEW_TOKEN" >> $GITHUB_ENV

      - name: Set secret (repo)
        run: gh secret set MY_TOKEN --body "$NEW_TOKEN"

      - name: Run smoke check
        run: |
          # run quick verification that the service accepts the new token
          ./scripts/smoke_check_with_token.sh "$NEW_TOKEN"

      - name: Revoke old token (manual / optional)
        if: success()
        run: |
          echo "Verification passed — revoke previous token manually or via API"

```

## Next steps to evaluate
- Pilot a simple `gh secret set` scheduled rotation for one non-production token and test the smoke-check flow.
- Evaluate Vault for dynamic secrets if production systems require automated, short-lived creds.
- Consider SOPS for encrypting repo-stored configuration that must remain in Git.

## Notes and safety
- Never store raw, filled secrets in git. Use the generated replace-text workflow for history-cleaning only after users rotate exposed tokens.
- Do not commit any filled `replace-text` files — keep those local and ephemeral.

---
Document created as a starting point for future evaluation and implementation.
