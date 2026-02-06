#!/usr/bin/env python3
"""Centralized secrets management for GAIA.

This module provides a unified interface for managing secrets across different
storage backends (environment variables, files, Bitwarden, encrypted stores).

Key features:
- Multiple secret providers with priority chain
- Safe secret rotation with backup
- Encryption at rest for local secrets
- AI agent-friendly interface
- Audit logging for secret access

Usage:
    from gaia.secrets import SecretsManager
    
    # Initialize with default providers
    sm = SecretsManager()
    
    # Get a secret
    token = sm.get('TELEGRAM_BOT_TOKEN')
    
    # Set a secret
    sm.set('API_KEY', 'value123', provider='encrypted_file')
    
    # Rotate a secret
    sm.rotate('TELEGRAM_BOT_TOKEN', new_value='new_token_value')
"""
import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime, timezone
import base64
from cryptography.fernet import Fernet


# Timestamp format constants
TIMESTAMP_ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # For audit logs
TIMESTAMP_COMPACT_FORMAT = '%Y%m%dT%H%M%SZ'  # For backup filenames


class SecretProvider:
    """Base class for secret providers."""
    
    def __init__(self, name: str, priority: int = 50):
        self.name = name
        self.priority = priority  # Lower number = higher priority
    
    def get(self, key: str) -> Optional[str]:
        """Get a secret value."""
        raise NotImplementedError
    
    def set(self, key: str, value: str) -> bool:
        """Set a secret value."""
        raise NotImplementedError
    
    def delete(self, key: str) -> bool:
        """Delete a secret."""
        raise NotImplementedError
    
    def list_keys(self) -> List[str]:
        """List available secret keys."""
        raise NotImplementedError


class EnvironmentProvider(SecretProvider):
    """Read secrets from environment variables."""
    
    def __init__(self):
        super().__init__("environment", priority=10)
    
    def get(self, key: str) -> Optional[str]:
        return os.environ.get(key)
    
    def set(self, key: str, value: str) -> bool:
        os.environ[key] = value
        return True
    
    def delete(self, key: str) -> bool:
        if key in os.environ:
            del os.environ[key]
            return True
        return False
    
    def list_keys(self) -> List[str]:
        return list(os.environ.keys())


class EnvFileProvider(SecretProvider):
    """Read/write secrets from .env files."""
    
    def __init__(self, file_path: str = ".env", priority: int = 20):
        super().__init__("env_file", priority=priority)
        self.file_path = Path(file_path)
    
    def _read_env(self) -> Dict[str, str]:
        """Parse .env file into dict."""
        env_vars = {}
        if not self.file_path.exists():
            return env_vars
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip().strip('"').strip("'")
        return env_vars
    
    def _write_env(self, env_vars: Dict[str, str]):
        """Write env vars to file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            for k, v in sorted(env_vars.items()):
                f.write(f'{k}={v}\n')
    
    def get(self, key: str) -> Optional[str]:
        env_vars = self._read_env()
        return env_vars.get(key)
    
    def set(self, key: str, value: str) -> bool:
        env_vars = self._read_env()
        env_vars[key] = value
        self._write_env(env_vars)
        return True
    
    def delete(self, key: str) -> bool:
        env_vars = self._read_env()
        if key in env_vars:
            del env_vars[key]
            self._write_env(env_vars)
            return True
        return False
    
    def list_keys(self) -> List[str]:
        return list(self._read_env().keys())


class EncryptedFileProvider(SecretProvider):
    """Store secrets in encrypted JSON file."""
    
    def __init__(self, file_path: str = ".private/secrets.enc", 
                 key_file: str = ".private/secrets.key", priority: int = 30):
        super().__init__("encrypted_file", priority=priority)
        self.file_path = Path(file_path)
        self.key_file = Path(key_file)
        self._ensure_key()
    
    def _ensure_key(self):
        """Ensure encryption key exists."""
        if not self.key_file.exists():
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            self.key_file.chmod(0o600)  # Read/write for owner only
    
    def _get_fernet(self) -> Fernet:
        """Get Fernet cipher."""
        key = self.key_file.read_bytes()
        return Fernet(key)
    
    def _read_secrets(self) -> Dict[str, str]:
        """Read and decrypt secrets file."""
        if not self.file_path.exists():
            return {}
        
        fernet = self._get_fernet()
        encrypted = self.file_path.read_bytes()
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode('utf-8'))
    
    def _write_secrets(self, secrets: Dict[str, str]):
        """Encrypt and write secrets file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        fernet = self._get_fernet()
        data = json.dumps(secrets, indent=2).encode('utf-8')
        encrypted = fernet.encrypt(data)
        self.file_path.write_bytes(encrypted)
        self.file_path.chmod(0o600)
    
    def get(self, key: str) -> Optional[str]:
        try:
            secrets = self._read_secrets()
            return secrets.get(key)
        except Exception:
            return None
    
    def set(self, key: str, value: str) -> bool:
        try:
            secrets = self._read_secrets()
            secrets[key] = value
            self._write_secrets(secrets)
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        try:
            secrets = self._read_secrets()
            if key in secrets:
                del secrets[key]
                self._write_secrets(secrets)
                return True
            return False
        except Exception:
            return False
    
    def list_keys(self) -> List[str]:
        try:
            return list(self._read_secrets().keys())
        except Exception:
            return []


class BitwardenProvider(SecretProvider):
    """Read secrets from Bitwarden CLI."""
    
    def __init__(self, priority: int = 40):
        super().__init__("bitwarden", priority=priority)
    
    def _run_bw(self, args: List[str]) -> Optional[str]:
        """Run bw command and return output."""
        try:
            result = subprocess.run(
                ['bw'] + args,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return None
    
    def get(self, key: str) -> Optional[str]:
        # Try to get password by item name
        return self._run_bw(['get', 'password', key])
    
    def set(self, key: str, value: str) -> bool:
        # Bitwarden set not implemented (use CLI interactively)
        return False
    
    def delete(self, key: str) -> bool:
        # Bitwarden delete not implemented (use CLI interactively)
        return False
    
    def list_keys(self) -> List[str]:
        # List items (names only)
        output = self._run_bw(['list', 'items'])
        if output:
            try:
                items = json.loads(output)
                return [item.get('name', '') for item in items if item.get('name')]
            except json.JSONDecodeError:
                pass
        return []


class SecretsManager:
    """Main secrets manager that coordinates multiple providers."""
    
    def __init__(self, root_dir: Optional[Path] = None):
        """Initialize secrets manager.
        
        Args:
            root_dir: Root directory for the project (defaults to GAIA root)
        """
        if root_dir is None:
            # Find project root (where .git is)
            root_dir = Path(__file__).resolve().parent.parent
        self.root_dir = Path(root_dir)
        
        # Initialize providers in priority order.
        # For encrypted-only workflow we prefer environment (process env) and
        # the encrypted file store. Env-file fallback is intentionally NOT
        # included here to avoid reading plaintext files from disk.
        self.providers: List[SecretProvider] = [
            EnvironmentProvider(),
            EncryptedFileProvider(
                str(self.root_dir / ".private" / "secrets.enc"),
                str(self.root_dir / ".private" / "secrets.key")
            ),
            BitwardenProvider(),
        ]
        
        # Sort by priority
        self.providers.sort(key=lambda p: p.priority)
        
        # Audit log
        self.audit_file = self.root_dir / ".private" / "secrets_audit.log"
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _log_audit(self, action: str, key: str, provider: str, success: bool):
        """Log secret access for audit."""
        timestamp = datetime.now(timezone.utc).strftime(TIMESTAMP_ISO_FORMAT)
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'key': key,
            'provider': provider,
            'success': success
        }
        try:
            with open(self.audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception:
            pass  # Don't fail if audit logging fails
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value from the highest priority provider that has it.
        
        Args:
            key: Secret key name
            default: Default value if secret not found
            
        Returns:
            Secret value or default
        """
        for provider in self.providers:
            try:
                value = provider.get(key)
                if value is not None:
                    self._log_audit('get', key, provider.name, True)
                    return value
            except Exception:
                continue
        
        self._log_audit('get', key, 'none', False)
        return default
    
    def set(self, key: str, value: str, provider: Optional[str] = None) -> bool:
        """Set a secret value.
        
        Args:
            key: Secret key name
            value: Secret value
            provider: Provider name to use (defaults to encrypted_file)
            
        Returns:
            True if successful
        """
        if provider is None:
            provider = "encrypted_file"
        
        for p in self.providers:
            if p.name == provider:
                try:
                    success = p.set(key, value)
                    self._log_audit('set', key, p.name, success)
                    return success
                except Exception:
                    self._log_audit('set', key, p.name, False)
                    return False
        
        self._log_audit('set', key, provider, False)
        return False
    
    def delete(self, key: str, provider: Optional[str] = None) -> bool:
        """Delete a secret.
        
        Args:
            key: Secret key name
            provider: Provider name (if None, deletes from all providers)
            
        Returns:
            True if deleted from at least one provider
        """
        deleted = False
        providers_to_check = self.providers if provider is None else [
            p for p in self.providers if p.name == provider
        ]
        
        for p in providers_to_check:
            try:
                if p.delete(key):
                    deleted = True
                    self._log_audit('delete', key, p.name, True)
            except Exception:
                self._log_audit('delete', key, p.name, False)
        
        return deleted
    
    def rotate(self, key: str, new_value: str, backup: bool = True) -> bool:
        """Rotate a secret with optional backup.
        
        Args:
            key: Secret key name
            new_value: New secret value
            backup: Whether to backup old value
            
        Returns:
            True if rotation successful
        """
        if backup:
            # Get old value
            old_value = self.get(key)
            if old_value:
                # Store backup with timestamp
                timestamp = datetime.now(timezone.utc).strftime(TIMESTAMP_COMPACT_FORMAT)
                backup_key = f"{key}_backup_{timestamp}"
                self.set(backup_key, old_value, provider='encrypted_file')
        
        # Set new value
        success = self.set(key, new_value, provider='encrypted_file')
        self._log_audit('rotate', key, 'encrypted_file', success)
        return success
    
    def list_secrets(self, provider: Optional[str] = None) -> Dict[str, List[str]]:
        """List available secret keys by provider.
        
        Args:
            provider: Provider name (if None, lists all providers)
            
        Returns:
            Dict mapping provider names to list of keys
        """
        result = {}
        providers_to_check = self.providers if provider is None else [
            p for p in self.providers if p.name == provider
        ]
        
        for p in providers_to_check:
            try:
                keys = p.list_keys()
                if keys:
                    result[p.name] = keys
            except Exception:
                pass
        
        return result
    
    def validate(self, key: str) -> Dict[str, Any]:
        """Validate a secret is accessible and return metadata.
        
        Args:
            key: Secret key name
            
        Returns:
            Dict with validation results
        """
        value = self.get(key)
        found_in = []
        
        for provider in self.providers:
            try:
                if provider.get(key) is not None:
                    found_in.append(provider.name)
            except Exception:
                pass
        
        return {
            'key': key,
            'found': value is not None,
            'providers': found_in,
            'length': len(value) if value else 0
        }


# Singleton instance for convenience
_default_manager: Optional[SecretsManager] = None


def get_manager() -> SecretsManager:
    """Get or create the default secrets manager singleton."""
    global _default_manager
    if _default_manager is None:
        _default_manager = SecretsManager()
    return _default_manager


def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Convenience function to get a secret."""
    return get_manager().get(key, default)


def set_secret(key: str, value: str, provider: Optional[str] = None) -> bool:
    """Convenience function to set a secret."""
    return get_manager().set(key, value, provider)


def rotate_secret(key: str, new_value: str, backup: bool = True) -> bool:
    """Convenience function to rotate a secret."""
    return get_manager().rotate(key, new_value, backup)
