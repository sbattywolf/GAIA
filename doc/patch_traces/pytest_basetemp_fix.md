---
title: Pytest `basetemp` config fix
date: 2026-02-04T00:00:00Z
author: assistant
---

Summary
-------

Replaced the unsupported `basetemp` pytest INI key with a supported `addopts = --basetemp=.pytest_tmp` entry in `pytest.ini` to avoid runtime `PytestConfigWarning: Unknown config option: basetemp` on recent pytest versions.

Patch
-----

File: `pytest.ini`

Before:

```
[pytest]
testpaths = tests
norecursedirs = AILocalModelLibrary .venv dist build
python_files = test_*.py
# Use project-local basetemp to avoid system temp permission errors
basetemp = .pytest_tmp
```

After:

```
[pytest]
testpaths = tests
norecursedirs = AILocalModelLibrary .venv dist build
python_files = test_*.py
# Use project-local basetemp to avoid system temp permission errors
addopts = --basetemp=.pytest_tmp
```

Rationale
---------

- Some pytest versions do not accept `basetemp` as a config key in `pytest.ini` and will emit a warning. Using `addopts` ensures the CLI flag is applied when pytest runs via configuration.  
- This preserves the repo-local basetemp behavior (avoids system-temp permission issues on Windows) while removing the warning.

Trace / Next actions
--------------------

- Apply same change to any repository templates or CI job configurations that set `basetemp` directly in INI-like files. For GitHub Actions, the workflow already passes `--basetemp .tmp/pytest` on the CLI; no change required there.  
- Consider adding this patch to onboarding docs and any repo generator template so newly created projects include `addopts` instead of `basetemp`.

Audit
-----

- Local test run verifying fix: `python -m pytest -q` — 60 passed, warning cleared.
- Local dry-run: `python -m pytest -q --basetemp=.pytest_tmp` also works as expected.
