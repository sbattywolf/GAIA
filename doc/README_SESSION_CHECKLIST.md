# Local Test Checklist

Use this checklist for quick local testing and developer onboarding.

- Set `PYTHONPATH` for local tests and run the full suite:

```powershell
$env:PYTHONPATH='.'
pytest -q
```

- Initialize a private env (creates `.private/telegram.env` template):

```powershell
python scripts/init_private_env.py
```

- Run the integration test (uses the mock Telegram server):

```powershell
$env:PYTHONPATH='.'; pytest tests/test_integration_telegram_mock.py -q
```

- Enable protected real sends (GitHub Actions):

Follow `doc/GITHUB_ENV_SETUP.md` to create the `production` environment, add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as secrets, and configure required reviewers.
