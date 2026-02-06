Script Runner Examples
======================

Purpose
-------
Short, copyable examples showing how agents and operators should use `scripts/run_script.py` and `agents.agent_utils.run_script()`.

CLI (safe):

PowerShell (use project's venv Python):

```powershell
# Run a Python script via the runner (ensures venv interpreter)
py -3 -m scripts.run_script scripts/my_script.py arg1 arg2

# Run a PowerShell script via the runner
py -3 -m scripts.run_script scripts/myscript.ps1 --option value
```

From an agent (preferred):

```python
from agents.agent_utils import run_script

res = run_script('scripts/my_script.py', args=['--task','sync'])
if res.get('rc') != 0:
    # log and handle error
    raise RuntimeError(f"script failed: {res.get('stderr')}")
```

Worker pattern (emit events and run script):

```python
from agents.agent_utils import run_script, build_event, append_event_atomic

res = run_script('scripts/package_build.py', args=['--out','dist'])
payload = {'cmd': 'package_build.py', 'rc': res.get('rc')}
append_event_atomic('events.ndjson', build_event('worker.run', 'package_fetcher', payload))
```

When to use the runner
- Use the runner for any local script file invocation to ensure the correct interpreter and venv are used.
- Use shell/subprocess only for dynamic shell commands that are not script files.

REPL note (quick reminder)
- Do not paste shell commands at a Python `>>>` prompt — they will raise `SyntaxError`.
- Exit the REPL (Ctrl+Z Enter on Windows) before running shell commands like `git` or `py -3 -c "..."`.

Logging & troubleshooting
- Runner logs to `.private/script_runner.log` with timestamp and exit status. Check it when an interpreter mismatch occurs.

Security
- Never pass secrets on the command line. Use `SecretsManager` and `scripts/secrets_cli.py` to set and retrieve credentials.

Related files
- `scripts/run_script.py` — the runner implementation
- `agents/agent_utils.py` — `run_script()` helper used by agents
