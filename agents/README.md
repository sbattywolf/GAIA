Environment installer agent

This folder contains small agent scripts used by GAIA for local prototyping.

`environment_installer.py` -- Performs environment setup:
- Dry-run (default): prints the planned steps and appends an `install.dryrun` event to `events.ndjson`.
- Apply: creates a `./.venv` and runs `pip install -r requirements.txt` using the venv's python.

Examples:

Dry-run:

```powershell
python agents\environment_installer.py
```

Apply (creates venv and installs Python deps):

```powershell
python agents\environment_installer.py --apply
```

To allow system-level package installs (choco/winget), add `--allow-system` (NOT recommended without explicit approval).
