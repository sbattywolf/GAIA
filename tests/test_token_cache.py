import json
import datetime
from unittest.mock import MagicMock, patch
from pathlib import Path

from gaia.token_cache import TokenCache


def test_token_cache_fetch_and_cache(tmp_path):
    # Prepare fake helper JSON output with token and expiry
    token = "install-token-123"
    expires_at = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)).isoformat().replace('+00:00', 'Z')
    helper_output = json.dumps({'token': token, 'expires_at': expires_at})

    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_proc.stdout = helper_output
    mock_proc.stderr = ''

    # Ensure key file exists (helper reads it in real runs)
    key_file = tmp_path / 'app.pem'
    key_file.write_text('FAKE-KEY')

    with patch('subprocess.run', return_value=mock_proc) as run_mock:
        tc = TokenCache(app_id='1', key_path=str(key_file), installation_id='10', helper_python='python')

        t1 = tc.get()
        assert t1 == token

        # second call should use cached token (subprocess.run called only once)
        t2 = tc.get()
        assert t2 == token
        assert run_mock.call_count == 1
