#!/usr/bin/env python3
"""Migration script: Move secrets from .env to encrypted storage.

This script helps users migrate their existing secrets from plaintext .env
files to encrypted storage managed by the GAIA secrets manager.

Usage:
    python scripts/migrate_to_encrypted_secrets.py [--source .env] [--dry-run]

The script will:
1. Read secrets from source file
2. Optionally validate them
3. Store in encrypted storage
4. Create a backup of the original file
5. Optionally remove sensitive keys from original file

Safety features:
- Dry-run mode shows what would happen without making changes
- Automatic backup of original file
- Only migrates recognized secret patterns
- Preserves non-sensitive config in .env
"""
import argparse
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gaia.secrets import SecretsManager


# Keys that should be encrypted (sensitive)
SENSITIVE_KEYS = {
    'AUTOMATION_GITHUB_TOKEN',
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_CHAT_ID',
    'API_KEY',
    'API_SECRET',
    'BOT_TOKEN',
    'ACCESS_TOKEN',
    'SECRET_KEY',
    'DATABASE_PASSWORD',
    'DB_PASSWORD',
    'PASSWORD',
    'PRIVATE_KEY',
    'WEBHOOK_SECRET',
    'JWT_SECRET',
    'ENCRYPTION_KEY',
}

# Keys that can stay in .env (non-sensitive config)
NON_SENSITIVE_KEYS = {
    'LOG_LEVEL',
    'DEBUG',
    'DEFAULT_PRIORITY',
    'GAIA_DATA_DIR',
    'PATH_APPEND',
    'ALLOW_COMMAND_EXECUTION',
    'ENVIRONMENT',
}


def is_sensitive(key: str) -> bool:
    """Check if a key is sensitive and should be encrypted."""
    key_upper = key.upper()
    
    # Exact match
    if key_upper in SENSITIVE_KEYS:
        return True
    
    # Pattern match
    sensitive_patterns = ['TOKEN', 'SECRET', 'PASSWORD', 'KEY', 'PASS', 'PWD', 'API', 'PRIVATE']
    for pattern in sensitive_patterns:
        if pattern in key_upper:
            return True
    
    # Known non-sensitive
    if key_upper in NON_SENSITIVE_KEYS:
        return False
    
    # Default: treat as sensitive if unsure
    return True


def parse_env_file(path: Path) -> dict:
    """Parse .env file into dict of key-value pairs."""
    if not path.exists():
        return {}
    
    secrets = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            
            if value:  # Only include non-empty values
                secrets[key] = value
    
    return secrets


def create_backup(source: Path) -> Path:
    """Create backup of source file."""
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup_path = source.with_suffix(f'.backup_{timestamp}')
    shutil.copy2(source, backup_path)
    return backup_path


def write_env_file(path: Path, secrets: dict):
    """Write secrets back to .env file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# GAIA Environment Configuration\n")
        f.write("# Sensitive secrets migrated to encrypted storage\n")
        f.write("# Use: python scripts/secrets_cli.py get <KEY>\n\n")
        
        for key, value in sorted(secrets.items()):
            f.write(f'{key}={value}\n')


def main():
    parser = argparse.ArgumentParser(
        description='Migrate secrets from .env to encrypted storage',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--source', default='.env',
                        help='Source .env file (default: .env)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    parser.add_argument('--keep-sensitive', action='store_true',
                        help='Keep sensitive keys in .env after migration (not recommended)')
    
    args = parser.parse_args()
    
    source = Path(args.source)
    
    print("=" * 70)
    print("GAIA Secrets Migration Tool")
    print("=" * 70)
    print()
    
    # Check if source exists
    if not source.exists():
        print(f"❌ Source file not found: {source}")
        print(f"   Create it or specify different source with --source")
        return 1
    
    print(f"Source: {source}")
    print(f"Mode: {'DRY RUN (no changes)' if args.dry_run else 'LIVE (will make changes)'}")
    print()
    
    # Parse source file
    print("Reading source file...")
    secrets = parse_env_file(source)
    
    if not secrets:
        print("No secrets found in source file.")
        return 0
    
    # Categorize secrets
    sensitive = {}
    non_sensitive = {}
    
    for key, value in secrets.items():
        if is_sensitive(key):
            sensitive[key] = value
        else:
            non_sensitive[key] = value
    
    print(f"Found {len(secrets)} total entries:")
    print(f"  - {len(sensitive)} sensitive (will encrypt)")
    print(f"  - {len(non_sensitive)} non-sensitive (will keep in .env)")
    print()
    
    # Show what will be migrated
    if sensitive:
        print("Sensitive secrets to encrypt:")
        for key in sorted(sensitive.keys()):
            value = sensitive[key]
            preview = f"{value[:10]}..." if len(value) > 10 else value
            print(f"  ✓ {key} = {preview}")
        print()
    
    if non_sensitive:
        print("Non-sensitive config to keep in .env:")
        for key in sorted(non_sensitive.keys()):
            print(f"  • {key} = {non_sensitive[key]}")
        print()
    
    # Dry run - stop here
    if args.dry_run:
        print("=" * 70)
        print("DRY RUN COMPLETE - No changes made")
        print("=" * 70)
        print("To perform migration, run without --dry-run:")
        print(f"  python scripts/migrate_to_encrypted_secrets.py --source {source}")
        return 0
    
    # Confirm migration
    print("=" * 70)
    response = input("Proceed with migration? [y/N]: ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return 0
    
    print()
    print("Starting migration...")
    
    # Create backup
    print("Creating backup...")
    backup_path = create_backup(source)
    print(f"  ✓ Backup created: {backup_path}")
    
    # Initialize secrets manager
    manager = SecretsManager()
    
    # Migrate sensitive secrets to encrypted storage
    print("Migrating sensitive secrets to encrypted storage...")
    migrated = 0
    failed = []
    
    for key, value in sensitive.items():
        try:
            success = manager.set(key, value, provider='encrypted_file')
            if success:
                print(f"  ✓ {key}")
                migrated += 1
            else:
                print(f"  ✗ {key} - Failed")
                failed.append(key)
        except Exception as e:
            print(f"  ✗ {key} - Error: {e}")
            failed.append(key)
    
    print()
    print(f"Migrated {migrated} of {len(sensitive)} sensitive secrets")
    
    if failed:
        print(f"Failed to migrate: {', '.join(failed)}")
        print("Aborting - no changes to source file")
        return 1
    
    # Update source file
    print()
    
    if args.keep_sensitive:
        print("Keeping sensitive keys in .env (--keep-sensitive was specified)")
        print("⚠️  Warning: This is less secure!")
    else:
        print("Updating source file (removing sensitive keys)...")
        write_env_file(source, non_sensitive)
        print(f"  ✓ Updated {source}")
    
    # Summary
    print()
    print("=" * 70)
    print("MIGRATION COMPLETE")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Verify secrets are accessible:")
    print("   python scripts/secrets_cli.py list --provider encrypted_file")
    print()
    print("2. Test retrieving a secret:")
    for key in list(sensitive.keys())[:1]:
        print(f"   python scripts/secrets_cli.py get {key}")
    print()
    print("3. Update your scripts to use:")
    print("   from gaia.secrets import get_secret")
    print("   value = get_secret('KEY_NAME')")
    print()
    print(f"4. Backup files:")
    print(f"   - Original: {backup_path}")
    print(f"   - Encryption key: .private/secrets.key (IMPORTANT: backup this!)")
    print(f"   - Encrypted secrets: .private/secrets.enc")
    print()
    print("Documentation: doc/SECRETS_MANAGEMENT_GUIDE.md")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
