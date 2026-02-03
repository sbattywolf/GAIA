# GAIA Monitor — Runbook

Quick start
- Install dependencies: `pip install -r monitor/requirements.txt` (or add `Flask` to your venv).
- Run the monitor: `python monitor/app.py` and open http://127.0.0.1:5000/ in your browser.

What the UI shows
- Overview: high-level notes and quick actions (Start/Stop agents).
- Events: tail of `events.ndjson` (auto-refresh).
- Agents: shows `out/status.json` if present (place producer output at `out/status.json` or `out/status/status.json`).
- Capabilities: scans the repository for JSON files that match the Alby capability schema and shows a summarized list (name, version, channels, skills).
- Logs: placeholder for `.tmp/logs` listings and rotation guidance.

Where to place capability files
- Recommended directory: `agents/capabilities/` or `out/capabilities/` for development samples.
- The monitor scans the repository; a capability JSON should include at least `name` and `skills` or `channels` to be detected.

Mapping to Alby 0.2 prototypes
- Alby 0.2 dev UIs in the old repo ran on ports `8000` (prototype) and `8001` (improved). Use this monitor as a lightweight, incremental replacement:
  - `Events` tab == prototype event tailer
  - `Capabilities` tab == summarized capability files (publisher output)
  - `Agents` tab == `out/status.json` produced by the Alby publisher

Start/Stop actions and safety
- The Start button runs `scripts/start_agents.ps1`; Stop runs `scripts/stop_agents.ps1` via PowerShell (`pwsh` preferred). Ensure PowerShell is on PATH.
- The monitor will show an error if PowerShell is not available. Use the UI carefully; Stop asks for confirmation in-browser.

Extending the dashboard
- Next steps: wire capability details (skill descriptions), show agent health (CPU/memory via `psutil`), add auth, or provide a small API for publisher actions.

Security
- This is a development tool. Do not expose it publicly without authentication and TLS.
