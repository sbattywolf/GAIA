GAIA Controller — Deployment & MyNAS Checklist

Purpose
- Guide to deploy the lightweight `agents/controller_agent.py` on a low-resource MyNAS or similar Linux box.

Prerequisites
- Python 3.10+ installed on MyNAS
- Git or a copy of this repository on the device
- A system user to run the service (recommended: `gaia`)
- Optional: `venv` available for an isolated environment

Quick install (recommended)
1. SSH to MyNAS and create a working directory (example):

```sh
mkdir -p /opt/gaia
cd /opt/gaia
git clone <your-repo-url> .
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a small wrapper script to run the controller (example provided in `scripts/run_controller.sh`).

3. Copy the systemd unit template `doc/gaia-controller.service` to `/etc/systemd/system/gaia-controller.service` and edit the `User=` and `WorkingDirectory=` fields as appropriate.

Systemd unit example (already provided) — then enable and start:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now gaia-controller.service
sudo journalctl -u gaia-controller -f
```

Controller runtime configuration
- Environment variables supported:
  - `CONTROLLER_POLL` (seconds, default 5)
  - `CONTROLLER_BATCH` (how many todos to assign per cycle)
  - `CONTROLLER_SIMULATE` (1 = simulate mode)
  - `GAIA_MONITOR_API_KEY` (if using monitor endpoints)
- You can create a small `.env` or export these variables in the unit file or the wrapper script.

Testing steps (safe)
1. Run locally on MyNAS in simulate mode to verify behavior:

```sh
/opt/gaia/.venv/bin/python agents/controller_agent.py --once --simulate
# or for continuous
/opt/gaia/.venv/bin/python agents/controller_agent.py --poll 10 --simulate
```

2. Create a sequence in the repo (or via the monitor) that triggers proposal creation and ensure `.tmp/active_task.json` and `.tmp/sequence_todos.json` appear.
3. Run the controller in `--simulate` for 10–30 minutes while monitoring CPU and memory:

```sh
top -b -n 1 | head -n 20
# or use `ps`/`htop` if available
```

4. If stable, run without `--simulate` and monitor logs:

```sh
sudo systemctl restart gaia-controller
sudo journalctl -u gaia-controller -f
```

Log locations and troubleshooting
- Unit logs: `journalctl -u gaia-controller` or configured log file (you can adapt the unit file to redirect logs)
- Local state files: `.tmp/active_task.json`, `.tmp/sequence_todos.json`, `doc/SEQUENCE_PROPOSALS.md`, `doc/SEQUENCE_ARCHIVE.md` (for merged proposals)

Notes and resource tuning
- Default poll interval is conservative; increase `CONTROLLER_POLL` to reduce wakeups on constrained devices.
- Keep `CONTROLLER_BATCH` small (1–3) on low-memory devices to limit concurrent work.
- The controller is intentionally lightweight (pure Python, no extra DB) — tune polling and use `--simulate` for safe validation.

Service unit and wrapper
- The repo provides `doc/gaia-controller.service` (template) and `scripts/run_controller.sh` (simple launcher) to assist deployment.

If you'd like, I can generate a systemd unit pre-filled for your MyNAS user and path — tell me the `User` and `WorkingDirectory` to use.
