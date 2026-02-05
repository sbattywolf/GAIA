#!/usr/bin/env python3
"""Tests for gaia.secrets module."""
import os
import tempfile
import shutil
from pathlib import Path
import pytest
import json

from gaia.secrets import (
    SecretsManager,
    EnvironmentProvider,
    EnvFileProvider,
    EncryptedFileProvider,
    get_secret,
    set_secret,
    rotate_secret
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture
def clean_env():
    """Clean environment for testing."""
    original_env = os.environ.copy()
    # Remove test keys if present
    test_keys = ['TEST_SECRET_1', 'TEST_SECRET_2', 'TEST_TOKEN']
    for key in test_keys:
        os.environ.pop(key, None)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestEnvironmentProvider:
    """Test EnvironmentProvider."""
    
    def test_get_existing(self, clean_env):
        provider = EnvironmentProvider()
        os.environ['TEST_SECRET_1'] = 'value1'
        assert provider.get('TEST_SECRET_1') == 'value1'
    
    def test_get_missing(self, clean_env):
        provider = EnvironmentProvider()
        assert provider.get('NONEXISTENT_KEY') is None
    
    def test_set(self, clean_env):
        provider = EnvironmentProvider()
        assert provider.set('TEST_SECRET_2', 'value2')
        assert os.environ['TEST_SECRET_2'] == 'value2'
    
    def test_delete(self, clean_env):
        provider = EnvironmentProvider()
        os.environ['TEST_SECRET_1'] = 'value1'
        assert provider.delete('TEST_SECRET_1')
        assert 'TEST_SECRET_1' not in os.environ
    
    def test_delete_missing(self, clean_env):
        provider = EnvironmentProvider()
        assert not provider.delete('NONEXISTENT_KEY')
    
    def test_list_keys(self, clean_env):
        provider = EnvironmentProvider()
        os.environ['TEST_KEY_1'] = 'val1'
        os.environ['TEST_KEY_2'] = 'val2'
        keys = provider.list_keys()
        assert 'TEST_KEY_1' in keys
        assert 'TEST_KEY_2' in keys


class TestEnvFileProvider:
    """Test EnvFileProvider."""
    
    def test_get_from_file(self, temp_dir):
        env_file = temp_dir / '.env'
        env_file.write_text('TEST_KEY=test_value\n')
        
        provider = EnvFileProvider(str(env_file))
        assert provider.get('TEST_KEY') == 'test_value'
    
    def test_get_missing_file(self, temp_dir):
        provider = EnvFileProvider(str(temp_dir / 'nonexistent.env'))
        assert provider.get('ANY_KEY') is None
    
    def test_set(self, temp_dir):
        env_file = temp_dir / '.env'
        provider = EnvFileProvider(str(env_file))
        
        assert provider.set('NEW_KEY', 'new_value')
        content = env_file.read_text()
        assert 'NEW_KEY=new_value' in content
    
    def test_delete(self, temp_dir):
        env_file = temp_dir / '.env'
        env_file.write_text('KEY1=val1\nKEY2=val2\n')
        
        provider = EnvFileProvider(str(env_file))
        assert provider.delete('KEY1')
        
        content = env_file.read_text()
        assert 'KEY1' not in content
        assert 'KEY2=val2' in content
    
    def test_list_keys(self, temp_dir):
        env_file = temp_dir / '.env'
        env_file.write_text('KEY1=val1\nKEY2=val2\n# Comment\n')
        
        provider = EnvFileProvider(str(env_file))
        keys = provider.list_keys()
        assert 'KEY1' in keys
        assert 'KEY2' in keys
        assert len(keys) == 2
    
    def test_handles_comments_and_blank_lines(self, temp_dir):
        env_file = temp_dir / '.env'
        env_file.write_text('# Comment\nKEY1=val1\n\nKEY2=val2\n')
        
        provider = EnvFileProvider(str(env_file))
        assert provider.get('KEY1') == 'val1'
        assert provider.get('KEY2') == 'val2'
    
    def test_handles_quotes(self, temp_dir):
        env_file = temp_dir / '.env'
        env_file.write_text('KEY1="quoted value"\nKEY2=\'single quoted\'\n')
        
        provider = EnvFileProvider(str(env_file))
        assert provider.get('KEY1') == 'quoted value'
        assert provider.get('KEY2') == 'single quoted'


class TestEncryptedFileProvider:
    """Test EncryptedFileProvider."""
    
    def test_encryption_key_creation(self, temp_dir):
        key_file = temp_dir / 'secrets.key'
        provider = EncryptedFileProvider(
            str(temp_dir / 'secrets.enc'),
            str(key_file)
        )
        
        assert key_file.exists()
        assert len(key_file.read_bytes()) > 0
    
    def test_set_and_get(self, temp_dir):
        provider = EncryptedFileProvider(
            str(temp_dir / 'secrets.enc'),
            str(temp_dir / 'secrets.key')
        )
        
        assert provider.set('SECRET_KEY', 'secret_value')
        assert provider.get('SECRET_KEY') == 'secret_value'
    
    def test_delete(self, temp_dir):
        provider = EncryptedFileProvider(
            str(temp_dir / 'secrets.enc'),
            str(temp_dir / 'secrets.key')
        )
        
        provider.set('KEY1', 'val1')
        provider.set('KEY2', 'val2')
        
        assert provider.delete('KEY1')
        assert provider.get('KEY1') is None
        assert provider.get('KEY2') == 'val2'
    
    def test_list_keys(self, temp_dir):
        provider = EncryptedFileProvider(
            str(temp_dir / 'secrets.enc'),
            str(temp_dir / 'secrets.key')
        )
        
        provider.set('KEY1', 'val1')
        provider.set('KEY2', 'val2')
        
        keys = provider.list_keys()
        assert set(keys) == {'KEY1', 'KEY2'}
    
    def test_persistence(self, temp_dir):
        """Test that secrets persist across provider instances."""
        enc_file = temp_dir / 'secrets.enc'
        key_file = temp_dir / 'secrets.key'
        
        provider1 = EncryptedFileProvider(str(enc_file), str(key_file))
        provider1.set('PERSIST_KEY', 'persist_value')
        
        # Create new provider instance with same files
        provider2 = EncryptedFileProvider(str(enc_file), str(key_file))
        assert provider2.get('PERSIST_KEY') == 'persist_value'


class TestSecretsManager:
    """Test SecretsManager."""
    
    def test_initialization(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        assert manager.root_dir == temp_dir
        assert len(manager.providers) > 0
    
    def test_get_from_environment(self, temp_dir, clean_env):
        os.environ['TEST_ENV_SECRET'] = 'env_value'
        manager = SecretsManager(root_dir=temp_dir)
        
        # Should get from environment (highest priority)
        assert manager.get('TEST_ENV_SECRET') == 'env_value'
    
    def test_get_from_file(self, temp_dir, clean_env):
        # Create .env file
        env_file = temp_dir / '.env'
        env_file.write_text('FILE_SECRET=file_value\n')
        
        manager = SecretsManager(root_dir=temp_dir)
        assert manager.get('FILE_SECRET') == 'file_value'
    
    def test_get_with_default(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        assert manager.get('NONEXISTENT', default='default_val') == 'default_val'
    
    def test_set_to_encrypted(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        assert manager.set('NEW_SECRET', 'new_value')
        
        # Should be retrievable
        assert manager.get('NEW_SECRET') == 'new_value'
    
    def test_rotate_with_backup(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        
        # Set initial value
        manager.set('ROTATE_KEY', 'old_value')
        
        # Rotate
        assert manager.rotate('ROTATE_KEY', 'new_value', backup=True)
        
        # Check new value
        assert manager.get('ROTATE_KEY') == 'new_value'
        
        # Check backup exists (with timestamp suffix)
        secrets = manager.list_secrets(provider='encrypted_file')
        backup_keys = [k for k in secrets.get('encrypted_file', []) 
                      if k.startswith('ROTATE_KEY_backup_')]
        assert len(backup_keys) == 1
    
    def test_rotate_without_backup(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        
        manager.set('NO_BACKUP_KEY', 'old_value')
        assert manager.rotate('NO_BACKUP_KEY', 'new_value', backup=False)
        assert manager.get('NO_BACKUP_KEY') == 'new_value'
        
        # No backup should exist
        secrets = manager.list_secrets(provider='encrypted_file')
        backup_keys = [k for k in secrets.get('encrypted_file', []) 
                      if k.startswith('NO_BACKUP_KEY_backup_')]
        assert len(backup_keys) == 0
    
    def test_delete(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        
        manager.set('DELETE_ME', 'value')
        assert manager.get('DELETE_ME') == 'value'
        
        assert manager.delete('DELETE_ME')
        assert manager.get('DELETE_ME') is None
    
    def test_validate_existing(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        manager.set('VALIDATE_KEY', 'validate_value')
        
        result = manager.validate('VALIDATE_KEY')
        assert result['found'] is True
        assert result['length'] == len('validate_value')
        assert len(result['providers']) > 0
    
    def test_validate_missing(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        
        result = manager.validate('NONEXISTENT_KEY')
        assert result['found'] is False
        assert result['length'] == 0
    
    def test_list_secrets(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        
        manager.set('LIST_KEY_1', 'val1')
        manager.set('LIST_KEY_2', 'val2')
        
        secrets = manager.list_secrets()
        assert 'encrypted_file' in secrets
        assert 'LIST_KEY_1' in secrets['encrypted_file']
        assert 'LIST_KEY_2' in secrets['encrypted_file']
    
    def test_audit_log_created(self, temp_dir):
        manager = SecretsManager(root_dir=temp_dir)
        
        manager.get('SOME_KEY')
        manager.set('AUDIT_KEY', 'audit_value')
        
        audit_file = temp_dir / '.private' / 'secrets_audit.log'
        assert audit_file.exists()
        
        # Check audit entries
        content = audit_file.read_text()
        assert 'SOME_KEY' in content or 'AUDIT_KEY' in content


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_get_secret(self, temp_dir, clean_env):
        os.environ['CONV_SECRET'] = 'conv_value'
        value = get_secret('CONV_SECRET')
        assert value == 'conv_value'
    
    def test_set_secret(self, temp_dir):
        # This will use the global singleton
        assert set_secret('CONV_SET_KEY', 'conv_set_value')
    
    def test_rotate_secret(self, temp_dir):
        set_secret('CONV_ROTATE_KEY', 'old')
        assert rotate_secret('CONV_ROTATE_KEY', 'new')
        assert get_secret('CONV_ROTATE_KEY') == 'new'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
