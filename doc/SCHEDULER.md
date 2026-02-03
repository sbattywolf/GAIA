Scheduler (draft)

Purpose
- Provide a simple mechanism to start/stop GAIA services on a schedule or on-demand.

How it works
- `scripts/scheduler.py` reads `.tmp/schedule.json` and starts services by invoking `.tmp/*.ps1` files.
- To request an immediate start, set `"start_immediately": true` for a service and the scheduler will run the corresponding script once and clear the flag.

Example
```json
[
  {"service":"monitor","action":"start","start_immediately":true},
  {"service":"telegram_bridge","action":"start","start_immediately":true}
]
```

Services
- `monitor` → `.tmp/start_monitor.ps1`
- `telegram_bridge` → `.tmp/telegram_bridge_job.ps1`
- `approval_listener` → `.tmp/approval_job.ps1`
- `periodic_runner` → `.tmp/periodic_job.ps1`

Future
- Integrate with Windows Task Scheduler or systemd for production scheduling.
- Add stop commands and health-check-based restarts.
