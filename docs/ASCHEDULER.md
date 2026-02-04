# ascheduler

Lightweight scheduler for repository tasks.

Usage (from repo root):

```powershell
python scripts/ascheduler.py --config scripts/ascheduler_config.json

# Run a single task once:
python scripts/ascheduler.py --run-once telegram
```

Edit `scripts/ascheduler_config.json` to add tasks. Each task should include:

- `name`: string identifier
- `interval_minutes`: integer minutes between runs (0 or missing = run-once)
- `command`: array or string command to execute
- `env`: optional dict of environment variable overrides

Notes:

- The scheduler is intentionally minimal and runs tasks in background threads.
- Use repo secrets and `PROTOTYPE_USE_LOCAL_EVENTS` to control whether tasks actually send external notifications.
