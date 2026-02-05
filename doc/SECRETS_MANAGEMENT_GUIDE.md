# GAIA Secrets Management - User Guide

## Overview

GAIA provides a comprehensive secrets management system that simplifies handling of tokens, passwords, API keys, and other sensitive information. The system supports multiple storage backends, automatic rotation, encryption at rest, and is designed to work seamlessly with both human operators and AI agents.

## Why Use GAIA Secrets Management?

### Problems It Solves

1. **Scattered Secret Storage** - No more hunting through multiple `.env` files, environment variables, or password managers
2. **Security Risks** - Encrypted storage prevents accidental exposure of secrets in plaintext
3. **Token Rotation Complexity** - Automated rotation with backup makes updates safe and trackable
4. **AI Agent Integration** - Simple API for agents to securely access credentials
5. **Audit Requirements** - Built-in audit logging tracks all secret access
6. **Team Collaboration** - Consistent interface across local development and CI/CD

### Key Features

- ✅ **Multiple Storage Providers**: Environment variables, `.env` files, encrypted files, Bitwarden CLI
- ✅ **Priority Chain**: Automatically checks providers in order (environment → files → encrypted → Bitwarden)
- ✅ **Encryption at Rest**: AES-256 encryption via Fernet for local secret files
- ✅ **Automatic Rotation**: Rotate secrets with automatic backup of old values
- ✅ **Audit Logging**: Track all secret access with timestamps
- ✅ **CLI Interface**: Simple command-line tool for all operations
- ✅ **Python API**: Clean programmatic interface for agents and scripts
- ✅ **Safe by Default**: Encrypted storage as default, audit logging always on

## Quick Start

### Installation

```bash
# Install requirements (includes cryptography)
pip install -r requirements.txt
```

### Basic Usage

```bash
# Set a secret (stored encrypted by default)
python scripts/secrets_cli.py set API_KEY my_secret_value

# Get a secret
python scripts/secrets_cli.py get API_KEY

# Rotate a secret (old value backed up automatically)
python scripts/secrets_cli.py rotate API_KEY new_secret_value

# List all secrets
python scripts/secrets_cli.py list

# Validate a secret exists
python scripts/secrets_cli.py validate API_KEY

# Generate a secure random token
python scripts/secrets_cli.py generate --length 32
```

## Storage Providers

### 1. Environment Variables
**Priority: Highest (10)**
- Fast, volatile, good for active sessions
- Set with: `export KEY=value` or `$env:KEY="value"` (PowerShell)
- Retrieved automatically by all providers

### 2. `.env` Files
**Priority: Medium (20)**
- Plain text files (ensure they're in `.gitignore`)
- Good for development environments
- Locations checked: `.private/.env`, `.env`

### 3. Encrypted Files
**Priority: Medium-Low (30)**
- **Recommended for sensitive data**
- Uses AES-256 encryption (Fernet)
- Stored in: `.private/secrets.enc`
- Encryption key in: `.private/secrets.key`
- Both files have 0600 permissions (owner read/write only)

### 4. Bitwarden CLI
**Priority: Lowest (40)**
- Integrates with Bitwarden password manager
- Requires `bw` CLI installed and logged in
- Read-only through this interface

## CLI Reference

### secrets_cli.py Commands

#### get
Retrieve a secret value.

```bash
python scripts/secrets_cli.py get SECRET_KEY

# JSON output
python scripts/secrets_cli.py get SECRET_KEY --json

# Quiet mode (value only)
python scripts/secrets_cli.py get SECRET_KEY --quiet
```

#### set
Store a secret value.

```bash
# Set to encrypted storage (default)
python scripts/secrets_cli.py set SECRET_KEY myvalue

# Set to specific provider
python scripts/secrets_cli.py set SECRET_KEY myvalue --provider env_file

# Read from stdin
echo "myvalue" | python scripts/secrets_cli.py set SECRET_KEY -
```

#### delete
Remove a secret.

```bash
# Delete from all providers
python scripts/secrets_cli.py delete SECRET_KEY

# Delete from specific provider
python scripts/secrets_cli.py delete SECRET_KEY --provider encrypted_file
```

#### rotate
Rotate a secret with backup.

```bash
# Rotate with automatic backup
python scripts/secrets_cli.py rotate SECRET_KEY newvalue

# Rotate without backup
python scripts/secrets_cli.py rotate SECRET_KEY newvalue --no-backup

# Read new value from stdin
echo "newvalue" | python scripts/secrets_cli.py rotate SECRET_KEY -
```

#### list
List all available secrets.

```bash
# List all secrets by provider
python scripts/secrets_cli.py list

# List from specific provider
python scripts/secrets_cli.py list --provider encrypted_file

# Quiet mode (keys only)
python scripts/secrets_cli.py list --quiet
```

#### validate
Check if a secret exists and get metadata.

```bash
python scripts/secrets_cli.py validate SECRET_KEY
# Output:
# Key: SECRET_KEY
# Found: Yes
# Length: 32
# Available in providers: environment, encrypted_file
```

#### generate
Generate a secure random token.

```bash
# Generate URL-safe token (default)
python scripts/secrets_cli.py generate --length 32

# Generate hex token
python scripts/secrets_cli.py generate --length 32 --hex

# Generate and store
python scripts/secrets_cli.py generate --length 32 | python scripts/secrets_cli.py set API_KEY -
```

## Python API

### For Scripts and Agents

```python
from gaia.secrets import get_secret, set_secret, rotate_secret

# Get a secret
api_key = get_secret('API_KEY')
if api_key is None:
    print("API_KEY not configured")

# Get with default
db_password = get_secret('DB_PASSWORD', default='default_pass')

# Set a secret
set_secret('NEW_KEY', 'value123')

# Rotate a secret
rotate_secret('TELEGRAM_BOT_TOKEN', 'new_token_value')
```

### Advanced Usage

```python
from gaia.secrets import SecretsManager

# Initialize manager
manager = SecretsManager()

# Set to specific provider
manager.set('SECRET', 'value', provider='encrypted_file')

# Delete from all providers
manager.delete('OLD_SECRET')

# Validate secret
info = manager.validate('API_KEY')
print(f"Found: {info['found']}")
print(f"Providers: {info['providers']}")

# List all secrets
secrets_map = manager.list_secrets()
for provider, keys in secrets_map.items():
    print(f"{provider}: {len(keys)} secrets")
```

## Common Workflows

### Initial Setup

```bash
# 1. Create .private directory (automatically done by secrets manager)
# 2. Add to .gitignore (already present in GAIA)

# 3. Store your first secret
python scripts/secrets_cli.py set GITHUB_TOKEN ghp_yourtokenhere

# 4. Verify it works
python scripts/secrets_cli.py validate GITHUB_TOKEN
```

### Migrating Existing Secrets

```bash
# If you have secrets in .env, migrate to encrypted storage

# 1. Read current .env
cat .env

# 2. For each secret, store in encrypted storage
python scripts/secrets_cli.py set SECRET_NAME "value_from_env"

# 3. Verify migration
python scripts/secrets_cli.py list --provider encrypted_file

# 4. Optional: Remove from .env
# (Keep .env for non-sensitive config like DEFAULT_PRIORITY)
```

### Token Rotation Workflow

```bash
# 1. Generate new token (or get from service)
NEW_TOKEN=$(python scripts/secrets_cli.py generate --length 32)

# 2. Test new token (service-specific)
# e.g., curl -H "Authorization: Bearer $NEW_TOKEN" https://api.example.com/test

# 3. Rotate (keeps backup)
python scripts/secrets_cli.py rotate API_TOKEN "$NEW_TOKEN"

# 4. Verify new token is active
python scripts/secrets_cli.py get API_TOKEN

# 5. Revoke old token at service provider
# (Old value is in .private/secrets.enc with _backup_<timestamp> suffix)
```

### Team Onboarding

**For new team member:**

```bash
# 1. Clone repository
git clone https://github.com/yourusername/GAIA.git
cd GAIA

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get secrets from team lead or secret vault
# Option A: Team lead exports from their encrypted storage
python scripts/secrets_cli.py get GITHUB_TOKEN --quiet > /tmp/token.txt

# Option B: Team lead provides via secure channel

# 4. Store secrets locally
python scripts/secrets_cli.py set GITHUB_TOKEN <value>
python scripts/secrets_cli.py set TELEGRAM_BOT_TOKEN <value>

# 5. Verify setup
python scripts/validate_secrets.py
```

## Security Best Practices

### 1. File Permissions

The secrets manager automatically sets secure permissions:
- `.private/secrets.enc`: 0600 (owner read/write only)
- `.private/secrets.key`: 0600 (owner read/write only)

Verify manually if needed:
```bash
ls -la .private/
# Should show: -rw------- (600)
```

### 2. Never Commit Secrets

Ensure these are in `.gitignore` (already configured in GAIA):
```
.private/
.env
.env.*
.tmp/
```

Verify:
```bash
git status .private/
# Should show: nothing to commit
```

### 3. Use Encrypted Storage

Always use encrypted storage for sensitive secrets:
```bash
# Good: Uses encrypted storage
python scripts/secrets_cli.py set API_KEY value

# Okay: For non-sensitive config
python scripts/secrets_cli.py set DEFAULT_LOG_LEVEL info --provider env_file

# Avoid: Storing sensitive data in plain .env
```

### 4. Regular Rotation

Set calendar reminders for token rotation:
- Critical tokens: Every 30 days
- API keys: Every 90 days
- Passwords: Every 180 days

### 5. Audit Trail

Review audit logs regularly:
```bash
# View recent secret access
tail -20 .private/secrets_audit.log

# Search for specific key
grep "GITHUB_TOKEN" .private/secrets_audit.log
```

### 6. Backup Encryption Keys

**Important:** Backup your encryption key securely!

```bash
# Backup key to encrypted USB or password manager
cp .private/secrets.key /secure/backup/location/

# Or use Bitwarden
bw create item secure-note --name "GAIA-secrets-key" \
  --notes "$(cat .private/secrets.key | base64)"
```

**Without the key, encrypted secrets cannot be recovered!**

## Integration with Existing Scripts

### Update Legacy Scripts

**Before (old way):**
```python
import os
github_token = os.environ.get('GITHUB_TOKEN')
```

**After (new way):**
```python
from gaia.secrets import get_secret
github_token = get_secret('GITHUB_TOKEN')
```

### Environment Loader Compatibility

The secrets manager works with existing `env_loader.py`:

```bash
# Old approach still works
python scripts/env_loader.py --env .private/.env -- python your_script.py

# New approach: Scripts use secrets manager directly
python your_script.py  # Automatically checks all providers
```

## Troubleshooting

### Secret Not Found

```bash
# Check which providers have the secret
python scripts/secrets_cli.py validate SECRET_NAME

# List all available secrets
python scripts/secrets_cli.py list

# Check audit log
grep "SECRET_NAME" .private/secrets_audit.log
```

### Encryption Key Lost

If `.private/secrets.key` is deleted, encrypted secrets **cannot be recovered**.

Prevention:
1. Backup `.private/secrets.key` securely
2. Store critical secrets in multiple locations (e.g., Bitwarden + encrypted file)
3. Document secret values in team password manager

Recovery:
1. Generate new secrets at service providers
2. Create new encryption key (happens automatically)
3. Store new secrets

### Permission Denied

```bash
# Fix file permissions
chmod 600 .private/secrets.enc
chmod 600 .private/secrets.key
chmod 700 .private/
```

### Import Error

```bash
# Ensure cryptography is installed
pip install cryptography

# Or reinstall all requirements
pip install -r requirements.txt
```

## For AI Agents

### Simple Secret Access

```python
from gaia.secrets import get_secret

# Get secret with fallback
token = get_secret('GITHUB_TOKEN', default='')
if not token:
    raise ValueError("GITHUB_TOKEN not configured")

# Use in API calls
import requests
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.github.com/user', headers=headers)
```

### Rotation by Agent

```python
from gaia.secrets import rotate_secret, get_secret
import requests

# Generate new token via API
old_token = get_secret('API_TOKEN')
response = requests.post('https://api.service.com/tokens/rotate', 
                         headers={'Authorization': f'Bearer {old_token}'})
new_token = response.json()['token']

# Rotate locally (automatic backup)
rotate_secret('API_TOKEN', new_token)

# Verify new token works
verify_response = requests.get('https://api.service.com/verify',
                               headers={'Authorization': f'Bearer {new_token}'})
assert verify_response.ok, "New token verification failed"
```

### Audit Logging

All secret access by agents is automatically logged:
- Which secret was accessed
- When it was accessed  
- Which provider provided it
- Whether access succeeded

Review agent activity:
```bash
# See what secrets agents accessed today
grep "$(date +%Y-%m-%d)" .private/secrets_audit.log
```

## Advanced Topics

### Custom Provider Priority

```python
from gaia.secrets import SecretsManager, EnvFileProvider

# Create manager with custom provider order
manager = SecretsManager()

# Add custom .env file location
custom_provider = EnvFileProvider('/path/to/custom.env', priority=5)
manager.providers.append(custom_provider)
manager.providers.sort(key=lambda p: p.priority)

# Now will check custom location first
value = manager.get('CUSTOM_SECRET')
```

### Backup Management

```python
from gaia.secrets import SecretsManager
from datetime import datetime, timedelta

manager = SecretsManager()

# List all secrets including backups
secrets = manager.list_secrets(provider='encrypted_file')
backups = [k for k in secrets.get('encrypted_file', []) if '_backup_' in k]

# Clean old backups (older than 90 days)
cutoff = datetime.utcnow() - timedelta(days=90)
for backup_key in backups:
    # Extract timestamp from key: KEY_backup_20260205T120000Z
    timestamp_str = backup_key.split('_backup_')[1]
    timestamp = datetime.strptime(timestamp_str, '%Y%m%dT%H%M%SZ')
    
    if timestamp < cutoff:
        manager.delete(backup_key, provider='encrypted_file')
        print(f"Deleted old backup: {backup_key}")
```

## Comparison with Other Solutions

| Feature | GAIA Secrets | .env Files | Bitwarden | HashiCorp Vault |
|---------|--------------|------------|-----------|-----------------|
| Encryption at rest | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Local-first | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| No external service | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Audit logging | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Rotation support | ✅ Yes | ❌ No | ⚠️ Manual | ✅ Yes |
| AI agent friendly | ✅ Yes | ⚠️ Limited | ❌ No | ⚠️ Complex |
| Zero setup cost | ✅ Yes | ✅ Yes | ❌ Requires account | ❌ Infrastructure |
| Team sharing | ⚠️ Manual | ⚠️ Manual | ✅ Yes | ✅ Yes |

## FAQ

**Q: Where are secrets stored physically?**
A: In `.private/secrets.enc` (encrypted) and `.private/secrets.key` (encryption key). Both have 0600 permissions.

**Q: Can I use this in CI/CD?**
A: Yes. Set secrets as environment variables in CI, or use the encrypted file approach with key in CI secrets.

**Q: What happens if I lose the encryption key?**
A: Encrypted secrets cannot be recovered. Always backup `.private/secrets.key` securely.

**Q: How does priority work?**
A: Lower number = higher priority. Environment (10) checked first, then env_file (20), encrypted_file (30), Bitwarden (40).

**Q: Is this secure enough for production?**
A: Yes for local/dev. For production, consider HashiCorp Vault or cloud secret managers (AWS Secrets Manager, Azure Key Vault).

**Q: Can multiple team members share encrypted secrets?**
A: Not directly. Each person has their own encryption key. Use Bitwarden or team password manager for sharing.

**Q: Does this work on Windows?**
A: Yes! All features work on Windows, Linux, and macOS.

**Q: How do I migrate to a different secrets manager?**
A: Export using `secrets_cli.py get`, then import to new system. Or write a migration script using the Python API.

## Next Steps

1. ✅ [Set up your first secret](#quick-start)
2. ✅ [Migrate existing `.env` secrets](#migrating-existing-secrets)
3. ✅ [Enable 2FA and store GitHub PAT](GITHUB_2FA_GUIDE.md)
4. ✅ [Set up token rotation schedule](#token-rotation-workflow)
5. ✅ [Update scripts to use secrets API](#integration-with-existing-scripts)
6. ✅ [Review audit logs monthly](#audit-trail)

## Support

- Module documentation: `gaia/secrets.py`
- CLI help: `python scripts/secrets_cli.py --help`
- Tests: `tests/test_secrets.py`
- GitHub 2FA: `doc/GITHUB_2FA_GUIDE.md`
