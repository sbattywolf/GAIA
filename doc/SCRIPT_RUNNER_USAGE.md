**Script Runner Usage**

Purpose: provide a standard, safe way for agents and scripts to execute other
scripts (of various languages) without accidentally sending shell commands
into a Python REPL or mis-invoking interpreters.

Location: `scripts/run_script.py`

Basic usage (from shell):

```powershell
python scripts/run_script.py scripts/my_script.py arg1 arg2
python scripts/run_script.py scripts/myscript.ps1 --option value
```

From Python (agent code):

```python
from agents.agent_utils import run_script
res = run_script('scripts/my_script.py', args=['arg1','arg2'])
if res.get('rc') != 0:
    # handle error; res['stderr'] contains details
    pass
```

Guidelines for agents:
- Prefer invoking `agents.agent_utils.run_script()` when running local script
  files. This ensures the project's venv Python is used for `.py` files and
  selects PowerShell, bash, java, or node for other extensions.
- Only fall back to shell execution for dynamic commands that are not script
  files (e.g. inline shell command). Use cautious timeouts and capture output.

Examples:

- Worker handler example (uses `run_script` when payload points to a file):

```python
from agents.agent_utils import run_script
res = run_script('scripts/some_task.py', args=['--smoke'])
```

- Export helper example (CLI driver calling the runner):

```bash
python -m scripts.run_script scripts/export_external_env.py --force
```

Logging:
- Runs are logged to `.private/script_runner.log` with timestamp and exit
  status. Check that file when diagnosing unexpected interpreter errors.

Security notes:
- `run_script.py` intentionally does not change environment variables when
  selecting interpreters; agents should use the `SecretsManager` to provide
  credentials securely (not plaintext env files) whenever possible.

REPL vs Shell — common pitfall
-----------------------------

Be careful not to type shell commands (for example, `git ...` or PowerShell
invocations like `& .\.venv\Scripts\python.exe -c "..."`) at a Python
REPL prompt (the `>>>` prompt). Those are invalid Python and will raise
`SyntaxError`.

Correct ways to run the commands:

- From PowerShell (exit the REPL first if you see `>>>`):

```powershell
& .\.venv\Scripts\python.exe -c "from gaia.secrets import SecretsManager; sm=SecretsManager(); print('FOUND' if sm.get('AUTOMATION_GITHUB_TOKEN') else 'MISSING')"
git add doc/SCRIPT_RUNNER_USAGE.md
git commit -m "docs: add script runner usage examples"
```

- From inside the Python REPL use valid Python instead of shell syntax:

```python
import importlib
m = importlib.import_module('gaia.secrets')
sm = m.SecretsManager()
print('FOUND' if sm.get('AUTOMATION_GITHUB_TOKEN') else 'MISSING')
```

- In IPython you can run shell commands with a leading `!`, e.g. `!git status`.

Adding this short note should reduce accidental `SyntaxError` occurrences when
operators switch between shells and the Python prompt.
