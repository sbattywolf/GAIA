# GitHub 2FA and Token Management Guide

## Overview
GitHub now requires two-factor authentication (2FA) by March 22, 2026. This guide explains how GAIA's secrets management system helps you work securely with 2FA enabled.

## Impact on Your Workflow

### What Changes With 2FA Enabled

1. **Git Operations (HTTPS)**
   - ❌ Can no longer use username/password
   - ✅ Must use Personal Access Token (PAT) instead
   
2. **GitHub CLI (`gh`)**
   - ✅ Still works, but requires initial authentication
   - ✅ Tokens managed by `gh auth` or via environment variables
   
3. **API Access**
   - ✅ Requires PAT for authentication
   - ✅ Agents use tokens from secrets manager

## Setup Steps After Enabling 2FA

### Step 1: Enable 2FA on GitHub
1. Go to https://github.com/settings/security
2. Click "Enable two-factor authentication"
3. Follow the setup wizard (use authenticator app or SMS)

### Step 2: Create Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)" or use fine-grained tokens
3. Select scopes needed:
   - `repo` - for repository access
   - `workflow` - for GitHub Actions
   - `read:org` - if working with organizations
4. Copy the token immediately (you won't see it again!)

### Step 3: Store Token Securely with GAIA

**Option A: Encrypted Storage (Recommended)**
```powershell
# Store your GitHub PAT securely
python scripts/secrets_cli.py set GITHUB_TOKEN <your-pat-here>

# Verify it's stored
python scripts/secrets_cli.py validate GITHUB_TOKEN
```

**Option B: Environment Variable**
```powershell
# Add to .private/.env (never commit this file!)
echo "GITHUB_TOKEN=<your-pat>" >> .private/.env
```

### Step 4: Configure Git to Use Token
```bash
# Set credential helper to use token
git config --global credential.helper store

# Or use GitHub CLI
gh auth login
```

### Step 5: Update CI/CD Secrets
```powershell
# Update repository secrets for Actions
gh secret set GITHUB_TOKEN --body "<your-pat>"
```

## Token Rotation with 2FA

### When to Rotate
- Every 90 days (recommended)
- Immediately if token is compromised
- Before token expiration date

### How to Rotate

```powershell
# 1. Generate new token on GitHub (same scopes as old)

# 2. Test new token works
$env:TEST_TOKEN = "<new-token>"
gh auth status

# 3. Rotate using GAIA secrets manager (keeps backup)
python scripts/secrets_cli.py rotate GITHUB_TOKEN <new-token>

# 4. Update CI/CD if needed
gh secret set GITHUB_TOKEN --body "<new-token>"

# 5. Revoke old token on GitHub
# Go to https://github.com/settings/tokens and delete old token
```

## Common Issues and Solutions

### Issue: "Authentication failed" after enabling 2FA
**Solution:** You're trying to use password instead of PAT
```powershell
# Use PAT for HTTPS git operations
git remote set-url origin https://<PAT>@github.com/owner/repo.git

# Or use SSH instead (2FA-friendly)
git remote set-url origin git@github.com:owner/repo.git
```

### Issue: GitHub CLI not working
**Solution:** Re-authenticate with `gh`
```powershell
gh auth login
# Choose: GitHub.com → HTTPS → Paste authentication token → <paste PAT>
```

### Issue: Actions failing after 2FA enabled
**Solution:** Verify repository secrets are set
```powershell
gh secret list
# If GITHUB_TOKEN missing:
gh secret set GITHUB_TOKEN --body "<your-pat>"
```

## Security Best Practices with 2FA

1. **Use Fine-Grained PATs When Possible**
   - More secure than classic PATs
   - Granular permissions per repository
   - Shorter expiration times

2. **Store Tokens Encrypted**
   ```powershell
   # Always use encrypted storage for PATs
   python scripts/secrets_cli.py set GITHUB_TOKEN <pat> --provider encrypted_file
   ```

3. **Enable Backup Codes**
   - Save recovery codes when setting up 2FA
   - Store them in password manager or encrypted file
   ```powershell
   python scripts/secrets_cli.py set GITHUB_2FA_BACKUP_CODES "<codes>"
   ```

4. **Use SSH for Git When Possible**
   - SSH keys work with 2FA
   - No need to embed tokens in URLs
   ```bash
   # Generate SSH key if needed
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Add to GitHub: https://github.com/settings/keys
   ```

5. **Audit Token Usage**
   ```powershell
   # Check which providers have your token
   python scripts/secrets_cli.py validate GITHUB_TOKEN
   
   # View audit log
   Get-Content .private/secrets_audit.log | Select-Object -Last 20
   ```

## For AI Agents and Automation

### Agents Using GitHub API
Update your agents to use the secrets manager:

```python
from gaia.secrets import get_secret

# Get GitHub token securely
github_token = get_secret('GITHUB_TOKEN')

# Use in API calls
headers = {'Authorization': f'Bearer {github_token}'}
```

### Scheduled Jobs
Ensure jobs can access tokens:

```powershell
# Run with environment loaded
python scripts/env_loader.py --env .private/.env -- python your_agent.py
```

## Migration Checklist

- [ ] Enable 2FA on GitHub account
- [ ] Save backup codes securely
- [ ] Generate new PAT with required scopes
- [ ] Store PAT using GAIA secrets manager
- [ ] Test Git operations with new PAT
- [ ] Update CI/CD secrets
- [ ] Update all scripts/agents to use secrets manager
- [ ] Configure credential helper or SSH
- [ ] Set calendar reminder for token rotation (90 days)
- [ ] Document token permissions for team

## Additional Resources

- GitHub 2FA Documentation: https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa
- Creating PATs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
- GAIA Secrets Management: See `gaia/secrets.py` and `scripts/secrets_cli.py`

## Questions?

If you encounter issues:
1. Check `gaia/secrets.py` module documentation
2. Run `python scripts/secrets_cli.py --help`
3. Review `.private/secrets_audit.log` for access patterns
