#!/usr/bin/env python3
"""CLI tool for managing secrets in GAIA.

This tool provides a simple command-line interface for secret operations:
- get: Retrieve a secret value
- set: Store a secret value
- delete: Remove a secret
- rotate: Rotate a secret with backup
- list: List available secrets
- validate: Check if a secret exists and where

Examples:
    # Get a secret
    python scripts/secrets_cli.py get TELEGRAM_BOT_TOKEN
    
    # Set a secret (defaults to encrypted storage)
    python scripts/secrets_cli.py set API_KEY myvalue123
    
    # Set to specific provider
    python scripts/secrets_cli.py set API_KEY myvalue123 --provider env_file
    
    # Rotate a secret with backup
    python scripts/secrets_cli.py rotate TELEGRAM_BOT_TOKEN new_token_value
    
    # List all secrets
    python scripts/secrets_cli.py list
    
    # Validate a secret
    python scripts/secrets_cli.py validate TELEGRAM_BOT_TOKEN
    
    # Generate a secure token
    python scripts/secrets_cli.py generate --length 32
"""
import argparse
import sys
import json
import secrets
from pathlib import Path

# Defer importing heavy dependencies (like cryptography) until needed.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def cmd_get(args, manager):
    """Get a secret value."""
    value = manager.get(args.key)
    if value is None:
        print(f"Secret '{args.key}' not found", file=sys.stderr)
        return 1
    
    if args.json:
        print(json.dumps({'key': args.key, 'value': value}))
    else:
        if args.quiet:
            print(value)
        else:
            print(f"{args.key}={value}")
    return 0


def cmd_set(args, manager):
    """Set a secret value."""
    value = args.value
    
    # Read from stdin if value is '-'
    if value == '-':
        value = sys.stdin.read().strip()
    
    success = manager.set(args.key, value, provider=args.provider)
    
    if args.json:
        print(json.dumps({'key': args.key, 'success': success}))
    elif not args.quiet:
        if success:
            provider = args.provider or 'encrypted_file'
            print(f"Secret '{args.key}' set successfully in {provider}")
        else:
            print(f"Failed to set secret '{args.key}'", file=sys.stderr)
    
    return 0 if success else 1


def cmd_delete(args, manager):
    """Delete a secret."""
    success = manager.delete(args.key, provider=args.provider)
    
    if args.json:
        print(json.dumps({'key': args.key, 'deleted': success}))
    elif not args.quiet:
        if success:
            print(f"Secret '{args.key}' deleted")
        else:
            print(f"Secret '{args.key}' not found", file=sys.stderr)
    
    return 0 if success else 1


def cmd_rotate(args, manager):
    """Rotate a secret with backup."""
    value = args.new_value
    
    # Read from stdin if value is '-'
    if value == '-':
        value = sys.stdin.read().strip()
    
    success = manager.rotate(args.key, value, backup=not args.no_backup)
    
    if args.json:
        print(json.dumps({'key': args.key, 'success': success}))
    elif not args.quiet:
        if success:
            print(f"Secret '{args.key}' rotated successfully")
            if not args.no_backup:
                print("  (old value backed up)")
        else:
            print(f"Failed to rotate secret '{args.key}'", file=sys.stderr)
    
    return 0 if success else 1


def cmd_list(args, manager):
    """List available secrets."""
    secrets_map = manager.list_secrets(provider=args.provider)
    
    if args.json:
        print(json.dumps(secrets_map, indent=2))
    else:
        for provider, keys in secrets_map.items():
            if not args.quiet:
                print(f"\n{provider}:")
            for key in sorted(keys):
                if args.quiet:
                    print(key)
                else:
                    print(f"  - {key}")
    
    return 0


def cmd_validate(args, manager):
    """Validate a secret."""
    result = manager.validate(args.key)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Key: {result['key']}")
        print(f"Found: {'Yes' if result['found'] else 'No'}")
        if result['found']:
            print(f"Length: {result['length']}")
            print(f"Available in providers: {', '.join(result['providers'])}")
    
    return 0 if result['found'] else 1


def cmd_generate(args, manager):
    """Generate a secure random token."""
    if args.hex:
        token = secrets.token_hex(args.length)
    else:
        token = secrets.token_urlsafe(args.length)
    
    if args.json:
        print(json.dumps({'token': token, 'length': len(token)}))
    else:
        print(token)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='GAIA secrets management CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--json', action='store_true',
                        help='Output in JSON format')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    subparsers.required = True
    
    # get command
    get_parser = subparsers.add_parser('get', help='Get a secret value')
    get_parser.add_argument('key', help='Secret key name')
    get_parser.set_defaults(func=cmd_get)
    
    # set command
    set_parser = subparsers.add_parser('set', help='Set a secret value')
    set_parser.add_argument('key', help='Secret key name')
    set_parser.add_argument('value', help='Secret value (use - to read from stdin)')
    set_parser.add_argument('--provider', 
                            choices=['environment', 'env_file', 'encrypted_file'],
                            help='Provider to use (default: encrypted_file)')
    set_parser.set_defaults(func=cmd_set)
    
    # delete command
    del_parser = subparsers.add_parser('delete', help='Delete a secret')
    del_parser.add_argument('key', help='Secret key name')
    del_parser.add_argument('--provider', help='Provider to delete from (default: all)')
    del_parser.set_defaults(func=cmd_delete)
    
    # rotate command
    rot_parser = subparsers.add_parser('rotate', help='Rotate a secret')
    rot_parser.add_argument('key', help='Secret key name')
    rot_parser.add_argument('new_value', help='New secret value (use - to read from stdin)')
    rot_parser.add_argument('--no-backup', action='store_true',
                            help='Do not backup old value')
    rot_parser.set_defaults(func=cmd_rotate)
    
    # list command
    list_parser = subparsers.add_parser('list', help='List available secrets')
    list_parser.add_argument('--provider', help='Filter by provider')
    list_parser.set_defaults(func=cmd_list)
    
    # validate command
    val_parser = subparsers.add_parser('validate', help='Validate a secret')
    val_parser.add_argument('key', help='Secret key name')
    val_parser.set_defaults(func=cmd_validate)
    
    # generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a secure token')
    gen_parser.add_argument('--length', type=int, default=32,
                            help='Token length (default: 32)')
    gen_parser.add_argument('--hex', action='store_true',
                            help='Generate hex token instead of URL-safe')
    gen_parser.set_defaults(func=cmd_generate)

    # import-env command: import keys from an env file into encrypted store
    imp_parser = subparsers.add_parser('import-env', help='Import an env file into encrypted store')
    imp_parser.add_argument('--file', '-f', default=str(Path(__file__).resolve().parent.parent / '.secret' / '.env'),
                            help='Path to env file to import')
    imp_parser.add_argument('--dry-run', action='store_true', help='Dry run: list keys to import without storing')
    imp_parser.add_argument('--filter', help='Optional substring filter for keys (e.g. TOKEN, SECRET)')
    imp_parser.set_defaults(func=lambda args, mgr: cmd_import_env(args, mgr))
    
    args = parser.parse_args()
    
    # Initialize secrets manager unless running a dry-run import (which doesn't require crypto)
    manager = None
    if not (args.command == 'import-env' and getattr(args, 'dry_run', False)):
        try:
            from gaia.secrets import SecretsManager
            manager = SecretsManager()
        except Exception as e:
            print(f'Warning: failed to initialize SecretsManager: {e}', file=sys.stderr)
            # For commands that require manager, this will error later if manager is None
    
    # Execute command
    try:
        return args.func(args, manager)
    except Exception as e:
        if args.json:
            print(json.dumps({'error': str(e)}), file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_import_env(args, manager):
    """Import keys from an env file into the encrypted provider."""
    path = Path(args.file)
    if not path.exists():
        print(f"Env file not found: {path}", file=sys.stderr)
        return 2

    # Parse file
    env = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

    # Filter keys if requested
    keys = sorted(env.keys())
    if args.filter:
        keys = [k for k in keys if args.filter in k]

    if args.dry_run:
        print(f"DRY RUN: would import {len(keys)} keys into encrypted store:")
        for k in keys:
            print(' -', k)
        return 0

    # Perform import
    success_count = 0
    for k in keys:
        v = env[k]
        try:
            ok = manager.set(k, v, provider='encrypted_file')
            if ok:
                success_count += 1
            else:
                print(f"Failed to set {k}", file=sys.stderr)
        except Exception as e:
            print(f"Error setting {k}: {e}", file=sys.stderr)

    print(f"Imported {success_count}/{len(keys)} keys into encrypted store (values not shown).")
    return 0


if __name__ == '__main__':
    sys.exit(main())
