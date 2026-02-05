# Secrets Management for AI Agents - Quick Reference

## For AI Agents Working with GAIA

This is a **simplified guide** for AI agents (including GitHub Copilot, Claude, GPT-4, etc.) to securely handle tokens, passwords, and sensitive data in the GAIA project.

## ⚡ Quick Start (Most Common Operations)

### Get a Secret
```python
from gaia.secrets import get_secret

# Simple get
token = get_secret('GITHUB_TOKEN')

# With fallback
api_key = get_secret('API_KEY', default='')
if not api_key:
    raise ValueError("API_KEY not configured")
```

### Set a Secret (Encrypted by Default)
```bash
# Command line
python scripts/secrets_cli.py set API_KEY myvalue123

# Or in Python
from gaia.secrets import set_secret
set_secret('API_KEY', 'myvalue123')
```

### Generate Secure Token
```bash
python scripts/secrets_cli.py generate --length 32
```

### Rotate a Token (with automatic backup)
```python
from gaia.secrets import rotate_secret

# Old value backed up automatically
rotate_secret('TELEGRAM_BOT_TOKEN', new_token_value)
```

## 🎯 Common Patterns for AI Agents

### Pattern 1: Required Secret with Clear Error
```python
from gaia.secrets import get_secret

def get_required_secret(key: str) -> str:
    value = get_secret(key)
    if not value:
        raise ValueError(
            f"{key} not configured. "
            f"Set it with: python scripts/secrets_cli.py set {key} <value>"
        )
    return value

# Usage
github_token = get_required_secret('GITHUB_TOKEN')
```

### Pattern 2: Multiple Required Secrets
```python
from gaia.secrets import SecretsManager

def validate_secrets(required_keys: list) -> dict:
    manager = SecretsManager()
    secrets = {}
    missing = []
    
    for key in required_keys:
        value = manager.get(key)
        if value:
            secrets[key] = value
        else:
            missing.append(key)
    
    if missing:
        raise ValueError(
            f"Missing secrets: {', '.join(missing)}. "
            f"Set with: python scripts/secrets_cli.py set <KEY> <value>"
        )
    
    return secrets

# Usage
secrets = validate_secrets(['GITHUB_TOKEN', 'TELEGRAM_BOT_TOKEN'])
```

### Pattern 3: Safe API Call
```python
from gaia.secrets import get_secret
import requests

def call_github_api(endpoint: str):
    token = get_secret('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN not configured")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api.github.com{endpoint}', headers=headers)
    response.raise_for_status()
    return response.json()

# Usage
user_data = call_github_api('/user')
```

### Pattern 4: Token Rotation
```python
from gaia.secrets import get_secret, rotate_secret
import requests

def rotate_github_pat():
    """Example: Rotate GitHub Personal Access Token."""
    # 1. Get current token
    old_token = get_secret('GITHUB_TOKEN')
    
    # 2. Generate new token (manual step on GitHub)
    print("Generate a new PAT at: https://github.com/settings/tokens")
    new_token = input("Enter new token: ").strip()
    
    # 3. Test new token
    headers = {'Authorization': f'Bearer {new_token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    response.raise_for_status()  # Will raise if token invalid
    
    # 4. Rotate (old value automatically backed up)
    rotate_secret('GITHUB_TOKEN', new_token)
    
    # 5. Remind to revoke old token
    print("✓ New token stored")
    print("Don't forget to revoke the old token on GitHub!")
    
    return new_token
```

## 📋 Decision Tree: When to Use What

```
Need to ACCESS a secret?
├─ Use: get_secret('KEY')
└─ If missing, provide clear instructions to set it

Need to STORE a secret?
├─ Command line: python scripts/secrets_cli.py set KEY value
└─ In code: set_secret('KEY', 'value')

Need to UPDATE a secret?
├─ Simple update: set_secret('KEY', 'new_value')
└─ With backup: rotate_secret('KEY', 'new_value')

Need to CHECK if secret exists?
├─ Simple: if get_secret('KEY') is None
└─ Detailed: manager.validate('KEY')

Need to GENERATE a token?
└─ python scripts/secrets_cli.py generate --length 32
```

## 🔐 Security Best Practices for Agents

### DO ✅

1. **Always use encrypted storage for sensitive data**
   ```python
   set_secret('API_KEY', value)  # Defaults to encrypted
   ```

2. **Mask secrets in logs**
   ```python
   token = get_secret('GITHUB_TOKEN')
   print(f"Using token: {token[:10]}...")  # Only show prefix
   ```

3. **Validate secrets before use**
   ```python
   token = get_secret('GITHUB_TOKEN')
   if not token:
       raise ValueError("GITHUB_TOKEN required")
   ```

4. **Use default values for non-sensitive config**
   ```python
   log_level = get_secret('LOG_LEVEL', default='INFO')
   ```

### DON'T ❌

1. **Never print full secrets**
   ```python
   # BAD
   print(f"Token: {token}")
   
   # GOOD
   print(f"Token: {token[:10]}..." if token else "not set")
   ```

2. **Never commit secrets to git**
   - Files in `.private/` are automatically ignored
   - Use `secrets_cli.py` to store, not `.env` directly

3. **Never hardcode secrets**
   ```python
   # BAD
   token = "ghp_abc123..."
   
   # GOOD
   token = get_secret('GITHUB_TOKEN')
   ```

4. **Never store secrets in plain .env for sensitive data**
   - Use encrypted storage: `set_secret()` (default)
   - Use `.env` only for non-sensitive config

## 🤖 Special Notes for AI Coding Agents

### When User Says: "Set up secrets"
1. Ask what secrets are needed
2. Generate secure tokens if needed:
   ```bash
   python scripts/secrets_cli.py generate --length 32
   ```
3. Store using encrypted storage:
   ```bash
   python scripts/secrets_cli.py set SECRET_NAME <value>
   ```
4. Validate:
   ```bash
   python scripts/secrets_cli.py validate SECRET_NAME
   ```

### When User Says: "Rotate my token"
1. Generate new token (or ask user to generate)
2. Test new token if possible
3. Rotate with backup:
   ```bash
   python scripts/secrets_cli.py rotate TOKEN_NAME <new-value>
   ```
4. Remind to revoke old token at service

### When User Says: "My secret isn't working"
1. Validate it exists:
   ```bash
   python scripts/secrets_cli.py validate SECRET_NAME
   ```
2. Check which providers have it:
   ```bash
   python scripts/secrets_cli.py list
   ```
3. Test by retrieving:
   ```bash
   python scripts/secrets_cli.py get SECRET_NAME --quiet
   ```

### When Implementing New Features
Always check if secrets are needed:
```python
# At the top of new scripts
from gaia.secrets import get_secret

# For any external service
def setup():
    required = ['GITHUB_TOKEN', 'API_KEY']
    for key in required:
        if not get_secret(key):
            print(f"Missing {key}. Set with: python scripts/secrets_cli.py set {key} <value>")
            return False
    return True
```

## 🔄 Priority Order (How Secrets are Found)

Secrets are checked in this order (lowest number = highest priority):

1. **Environment Variables** (priority 10) - Active session
2. **`.private/.env`** (priority 20) - Private config file
3. **`.env`** (priority 20) - Public config file
4. **Encrypted File** (priority 30) - `.private/secrets.enc`
5. **Bitwarden** (priority 40) - External password manager

First match wins. Example:
```bash
export GITHUB_TOKEN=env_value
# Also stored in encrypted: GITHUB_TOKEN=encrypted_value

python -c "from gaia.secrets import get_secret; print(get_secret('GITHUB_TOKEN'))"
# Output: env_value (environment wins)
```

## 📝 Complete Example: Building a New Agent

```python
#!/usr/bin/env python3
"""Example agent using secrets manager."""

from gaia.secrets import get_secret, SecretsManager
import requests
import sys

def validate_setup():
    """Validate all required secrets are configured."""
    required = {
        'GITHUB_TOKEN': 'GitHub Personal Access Token',
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot Token',
        'TELEGRAM_CHAT_ID': 'Telegram Chat ID'
    }
    
    manager = SecretsManager()
    missing = []
    
    for key, description in required.items():
        if not manager.get(key):
            missing.append(f"  {key}: {description}")
    
    if missing:
        print("Missing required secrets:")
        print('\n'.join(missing))
        print("\nSet them with:")
        print("  python scripts/secrets_cli.py set <KEY> <value>")
        return False
    
    return True

def send_github_stats():
    """Fetch GitHub stats and send to Telegram."""
    # Get secrets
    github_token = get_secret('GITHUB_TOKEN')
    bot_token = get_secret('TELEGRAM_BOT_TOKEN')
    chat_id = get_secret('TELEGRAM_CHAT_ID')
    
    # Call GitHub API
    headers = {'Authorization': f'Bearer {github_token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    response.raise_for_status()
    user_data = response.json()
    
    # Format message
    message = f"GitHub Stats:\n"
    message += f"User: {user_data['login']}\n"
    message += f"Public repos: {user_data['public_repos']}\n"
    
    # Send to Telegram
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, json=data)
    response.raise_for_status()
    
    print("✓ Stats sent to Telegram")

def main():
    if not validate_setup():
        return 1
    
    try:
        send_github_stats()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

## 📚 Additional Resources

- **Full Documentation**: `doc/SECRETS_MANAGEMENT_GUIDE.md`
- **GitHub 2FA Guide**: `doc/GITHUB_2FA_GUIDE.md`
- **Module Code**: `gaia/secrets.py`
- **CLI Tool**: `scripts/secrets_cli.py`
- **Tests**: `tests/test_secrets.py`
- **Examples**: `examples/secrets_migration_examples.py`

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "Secret not found" | `python scripts/secrets_cli.py list` to see what's available |
| "Permission denied" | Check `.private/` permissions: `chmod 700 .private/` |
| "Import error" | `pip install -r requirements.txt` |
| "Can't find module" | Add parent dir: `sys.path.insert(0, str(Path(__file__).parent.parent))` |
| "Want to change secret" | `python scripts/secrets_cli.py set KEY newvalue` |
| "Need to backup" | Use `rotate` instead of `set` for automatic backup |

## ✨ Summary: The Three Commands You Need

```bash
# 1. Set a secret (encrypted by default)
python scripts/secrets_cli.py set SECRET_NAME secret_value

# 2. Get a secret (in your code)
from gaia.secrets import get_secret
value = get_secret('SECRET_NAME')

# 3. Rotate a secret (with automatic backup)
python scripts/secrets_cli.py rotate SECRET_NAME new_value
```

That's it! These three operations cover 90% of secret management needs for AI agents working on GAIA.
