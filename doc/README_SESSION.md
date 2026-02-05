# GAIA Session Runner — install notes

This document describes how to run `scripts/session_progress_runner.py` as a persistent background service on a Linux NAS (systemd) or via the included launcher.

Quick steps (systemd)

1. Copy the unit and edit paths:

```sh
sudo cp scripts/gaia_session.service /etc/systemd/system/gaia_session.service
sudo nano /etc/systemd/system/gaia_session.service
# Edit WorkingDirectory and EnvironmentFile to the GAIA repo path on your NAS
```

2. Reload and start:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now gaia_session.service
sudo systemctl status gaia_session.service
sudo journalctl -u gaia_session.service -f
```

Quick steps (launcher)

1. Ensure the launcher is executable and run it:

```sh
chmod +x scripts/run_session.sh
scripts/run_session.sh
```

2. The launcher writes logs to `.tmp/logs/session_progress.log` and a PID to `.tmp/session_progress.pid`.

````markdown
# GAIA Session Runner — install notes

This document describes how to run `scripts/session_progress_runner.py` as a persistent background service on a Linux NAS (systemd) or via the included launcher.

Quick steps (systemd)

1. Copy the unit and edit paths:

```sh
sudo cp scripts/gaia_session.service /etc/systemd/system/gaia_session.service
sudo nano /etc/systemd/system/gaia_session.service
# Edit WorkingDirectory and EnvironmentFile to the GAIA repo path on your NAS
```

2. Reload and start:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now gaia_session.service
sudo systemctl status gaia_session.service
sudo journalctl -u gaia_session.service -f
```

Quick steps (launcher)

1. Ensure the launcher is executable and run it:

```sh
chmod +x scripts/run_session.sh
scripts/run_session.sh
```

2. The launcher writes logs to `.tmp/logs/session_progress.log` and a PID to `.tmp/session_progress.pid`.

Notes & QNAP specifics

- Some QNAP devices use init systems other than systemd. If your NAS does not provide systemd, use the `run_session.sh` launcher and a cron @reboot entry or an available init mechanism on the device.
- Ensure your `.tmp/telegram.env` contains `TELEGRAM_BOT_TOKEN` and `CHAT_ID`.

Local test checklist

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

Enable protected real sends

- Follow `doc/GITHUB_ENV_SETUP.md` to create the `production` environment and add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as secrets.
- Use the workflow `real-send.yml` to dispatch manual approved sends from GitHub Actions.

````
