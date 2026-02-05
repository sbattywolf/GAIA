#!/usr/bin/env python3
"""Example: Migrating an existing agent to use GAIA secrets manager.

This example shows how to update an existing script that uses environment
variables or .env files to use the centralized secrets manager.

BEFORE (old pattern):
    import os
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
AFTER (new pattern):
    from gaia.secrets import get_secret
    token = get_secret('TELEGRAM_BOT_TOKEN')
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gaia.secrets import get_secret, SecretsManager


def example_basic_migration():
    """Basic migration example."""
    print("=" * 60)
    print("Example 1: Basic Secret Access")
    print("=" * 60)
    
    # Old way (still works but checks only environment)
    import os
    old_way = os.environ.get('TELEGRAM_BOT_TOKEN')
    print(f"Old way (env only): {old_way is not None}")
    
    # New way (checks all providers)
    new_way = get_secret('TELEGRAM_BOT_TOKEN')
    print(f"New way (all providers): {new_way is not None}")
    
    if new_way:
        print(f"Token length: {len(new_way)}")
        print(f"Token preview: {new_way[:10]}...")
    else:
        print("Token not configured in any provider")


def example_with_defaults():
    """Example with default values."""
    print("\n" + "=" * 60)
    print("Example 2: Using Default Values")
    print("=" * 60)
    
    # Get with default for non-critical settings
    log_level = get_secret('LOG_LEVEL', default='INFO')
    print(f"Log level: {log_level}")
    
    # Get required secret
    api_key = get_secret('CRITICAL_API_KEY')
    if not api_key:
        print("ERROR: CRITICAL_API_KEY must be configured!")
        return False
    
    return True


def example_github_integration():
    """Example: Using GitHub token for API calls."""
    print("\n" + "=" * 60)
    print("Example 3: GitHub API Integration")
    print("=" * 60)
    
    github_token = get_secret('GITHUB_TOKEN')
    if not github_token:
        print("GITHUB_TOKEN not configured")
        print("Set it with: python scripts/secrets_cli.py set GITHUB_TOKEN <your-pat>")
        return
    
    # Simulate API call (don't actually call in example)
    print(f"Would call GitHub API with token: {github_token[:10]}...")
    print("Example usage:")
    print("  import requests")
    print("  headers = {'Authorization': f'Bearer {github_token}'}")
    print("  response = requests.get('https://api.github.com/user', headers=headers)")


def example_telegram_bot():
    """Example: Telegram bot with secrets manager."""
    print("\n" + "=" * 60)
    print("Example 4: Telegram Bot Integration")
    print("=" * 60)
    
    # Get required secrets
    bot_token = get_secret('TELEGRAM_BOT_TOKEN')
    chat_id = get_secret('TELEGRAM_CHAT_ID')
    
    if not bot_token:
        print("TELEGRAM_BOT_TOKEN not configured")
        print("Set it with: python scripts/secrets_cli.py set TELEGRAM_BOT_TOKEN <token>")
        return
    
    if not chat_id:
        print("TELEGRAM_CHAT_ID not configured")
        print("Set it with: python scripts/secrets_cli.py set TELEGRAM_CHAT_ID <chat-id>")
        return
    
    print(f"Bot token: {bot_token[:15]}...")
    print(f"Chat ID: {chat_id}")
    print("Ready to send messages!")
    
    # Example: Send message
    print("\nExample code:")
    print("  import requests")
    print("  url = f'https://api.telegram.org/bot{bot_token}/sendMessage'")
    print("  data = {'chat_id': chat_id, 'text': 'Hello from GAIA!'}")
    print("  response = requests.post(url, json=data)")


def example_advanced_usage():
    """Example: Advanced usage with SecretsManager."""
    print("\n" + "=" * 60)
    print("Example 5: Advanced SecretsManager Usage")
    print("=" * 60)
    
    manager = SecretsManager()
    
    # Validate multiple secrets
    required_secrets = ['TELEGRAM_BOT_TOKEN', 'GITHUB_TOKEN', 'API_KEY']
    missing = []
    
    for key in required_secrets:
        info = manager.validate(key)
        if info['found']:
            print(f"✓ {key}: Found (length={info['length']}, providers={','.join(info['providers'])})")
        else:
            print(f"✗ {key}: Missing")
            missing.append(key)
    
    if missing:
        print(f"\nMissing secrets: {', '.join(missing)}")
        print("Set them with:")
        for key in missing:
            print(f"  python scripts/secrets_cli.py set {key} <value>")


def example_rotation_in_agent():
    """Example: Automated token rotation in an agent."""
    print("\n" + "=" * 60)
    print("Example 6: Token Rotation in Agent")
    print("=" * 60)
    
    from gaia.secrets import rotate_secret
    
    print("Example: Rotate a token after generating new one")
    print("""
def rotate_api_token():
    from gaia.secrets import get_secret, rotate_secret
    import requests
    
    # Get current token
    old_token = get_secret('API_TOKEN')
    
    # Request new token from service
    response = requests.post('https://api.service.com/tokens/rotate',
                            headers={'Authorization': f'Bearer {old_token}'})
    new_token = response.json()['token']
    
    # Rotate locally (old value backed up automatically)
    rotate_secret('API_TOKEN', new_token)
    
    # Verify new token works
    verify = requests.get('https://api.service.com/verify',
                         headers={'Authorization': f'Bearer {new_token}'})
    
    if verify.ok:
        print('Token rotated successfully!')
        # Optionally revoke old token at service
    else:
        print('New token verification failed!')
        # Rollback if needed
    """)


def example_for_ai_agents():
    """Example: Patterns optimized for AI agents."""
    print("\n" + "=" * 60)
    print("Example 7: AI Agent-Friendly Patterns")
    print("=" * 60)
    
    print("""
# Pattern 1: Simple access with clear error messages
from gaia.secrets import get_secret

def get_github_token():
    token = get_secret('GITHUB_TOKEN')
    if not token:
        raise ValueError(
            "GITHUB_TOKEN not configured. "
            "Set it with: python scripts/secrets_cli.py set GITHUB_TOKEN <token>"
        )
    return token

# Pattern 2: Batch validation
from gaia.secrets import SecretsManager

def validate_required_secrets(required_keys):
    manager = SecretsManager()
    missing = []
    
    for key in required_keys:
        if not manager.get(key):
            missing.append(key)
    
    if missing:
        raise ValueError(
            f"Missing required secrets: {', '.join(missing)}. "
            f"Set with: python scripts/secrets_cli.py set <KEY> <value>"
        )

# Pattern 3: Safe multi-provider access
from gaia.secrets import get_secret

# Try environment first (for CI), then encrypted storage (for local)
def get_token_safe(key):
    token = get_secret(key)
    if token:
        # Mask in logs
        print(f"Using {key}: {token[:10]}...")
        return token
    else:
        print(f"Warning: {key} not found in any provider")
        return None
    """)


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print(" GAIA Secrets Manager - Migration Examples")
    print("=" * 70)
    
    example_basic_migration()
    example_with_defaults()
    example_github_integration()
    example_telegram_bot()
    example_advanced_usage()
    example_rotation_in_agent()
    example_for_ai_agents()
    
    print("\n" + "=" * 70)
    print(" Examples Complete")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Set your secrets: python scripts/secrets_cli.py set <KEY> <value>")
    print("2. Validate setup: python scripts/secrets_cli.py list")
    print("3. Update your scripts to use: from gaia.secrets import get_secret")
    print("4. Test your integrations")
    print("\nDocumentation: doc/SECRETS_MANAGEMENT_GUIDE.md")


if __name__ == '__main__':
    main()
