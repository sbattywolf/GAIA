import unittest
from unittest.mock import patch, MagicMock

import scripts.telegram_client as tc


class FakeResponse:
    def __init__(self, json_obj=None, status_code=200):
        self._json = json_obj or {'ok': True, 'result': {}}
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f'status {self.status_code}')


class TestTelegramClient(unittest.TestCase):
    @patch('scripts.telegram_client.requests.post')
    def test_send_message_success(self, mock_post):
        mock_post.return_value = FakeResponse({'ok': True, 'result': {'message_id': 1}})
        resp = tc.send_message('token', 123, 'hello')
        self.assertEqual(resp.get('ok'), True)

    @patch('scripts.telegram_client.requests.post')
    def test_send_message_retries(self, mock_post):
        # first two calls raise, third succeeds
        def side_effect(*a, **kw):
            if side_effect.count < 2:
                side_effect.count += 1
                raise Exception('conn')
            return FakeResponse({'ok': True})
        side_effect.count = 0
        mock_post.side_effect = side_effect
        resp = tc.send_message('token', 123, 'hello')
        self.assertTrue(resp.get('ok'))


if __name__ == '__main__':
    unittest.main()
