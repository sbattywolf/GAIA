# Rotation Pilot — README

Purpose: quick pilot to exercise token rotation using the scaffolded `rotate-secret` workflow and verify new tokens with a smoke check.

Steps (local / dry-run):

1. Fill a non-production token in your environment or generate one locally:

```powershell
# PowerShell
[System.Convert]::ToBase64String((New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes(32))

# or use OpenSSL (WSL / Git Bash)
openssl rand -base64 32
```

2. Run the PowerShell smoke-check locally:

```powershell
.\scripts\smoke_check_with_token.ps1 -Token '<YOUR_TOKEN>'
```

3. To try the GitHub Actions pilot (no production impact):
- Ensure `gh` is configured and the account used by the runner has permission to set repo secrets (may need a PAT).
- Trigger the `rotate-secret` workflow manually from Actions → Workflows → rotate-secret → Run workflow.

Files added for the pilot:
- `/.github/workflows/rotate-secret.yml` — scaffolded rotation job.
- `/scripts/smoke_check_with_token.sh` — Bash smoke check (already added).
- `/scripts/smoke_check_with_token.ps1` — PowerShell smoke check (Windows users).
- `/doc/TOKEN_ROTATION_RECOMMENDATIONS.md` — longer recommendations and examples.

Security notes:
- Do not use the `rotate-secret` workflow with production secrets until you confirm runner permissions and review the revoke/rollback plan.
- Never commit filled replace-text files or raw tokens.

Next: run local smoke checks and, if successful, pilot the Actions job with a non-critical secret.
