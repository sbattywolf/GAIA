import os
import tempfile
from pathlib import Path


def test_persist_token_encrypts_and_writes(tmp_path, monkeypatch):
    # generate a Fernet key for testing
    try:
        from cryptography.fernet import Fernet
    except Exception:
        pytest.skip('cryptography not installed')

    key = Fernet.generate_key().decode()
    monkeypatch.setenv('GAIA_FERNET_KEY', key)
    monkeypatch.setenv('GAIA_GITHUB_TOKEN', 'TESTTOKEN123')

    scripts_dir = Path(__file__).resolve().parent.parent / 'scripts'
    script_path = scripts_dir / 'persist_token.py'
    assert script_path.exists(), 'persist_token.py must exist'

    # run the script
    import runpy
    rc = runpy.run_path(str(script_path), run_name='__main__')

    out_file = Path(script_path).resolve().parent.parent / '.private' / 'gaia_github_token.enc'
    assert out_file.exists(), 'encrypted token file was not created'
