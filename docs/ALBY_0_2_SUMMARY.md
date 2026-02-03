# Alby 0.2 — Extracted Tech Notes (summary)

Purpose
- Short, actionable summary of Alby 0.2 tech notes found in `AILocalModelLibrary` to inform Alby 0.3 design and GAIA integration.

Where to look
- `AILocalModelLibrary/AGENT_TASKS/agent_runtime/alby_0_2/` — main runtime, publisher, and capability examples.
- Key files: `AGENT_CAPABILITIES.md`, `AGENT_0_2_BUILD_GUIDE.md`, `internet_capable_agent.json`, `publish_to_data_store.py`, `runner.py`, `run_tests.py`.

Capability schema (essentials)
- Required top-level fields: `name`, `version`, `channels`.
- Common fields: `owner`, `channels`, `internet_access` (bool), `auth` (e.g., `{ "type":"env-token","token_env":"ALBY_INTERNET_TOKEN" }`), `skills` (array).
- Skill object: `id`, `description`, `instruction_template`, `parameters`.

Runtime & publisher flow
- `sample_config.json` references a `capabilities_file` (e.g., `internet_capable_agent.json`).
- `publish_to_data_store.py` reads `sample_config.json` and emits `data_store.json` (used by the prototype UI).
- Quick run:

  1. Ensure `out/status.json` exists for the agent.
  2. Run publisher: `python AGENT_TASKS/agent_runtime/alby_0_2/publish_to_data_store.py`.
  3. Start prototype UI: `python AGENT_TASKS/agent_runtime/monitoring_prototype/serve_prototype_with_data.py --port 8001` and open `http://localhost:8001/`.

Security & secrets
- Internet-capable agents need operator-provided secrets via env vars (recommended pattern: `token_env` in capability `auth`).
- Never embed secrets in capability files; include only metadata in emitted events.
- For web-facing skills (`fetch_url`, `web_search`) use allowlists and throttle/rate-limit.

Example capability (from repo)

```json
{ "name":"Alby 0.2 Internet", "version":"0.2", "channels":["plocal","online","private_peer"], "internet_access":true, "auth":{ "type":"env-token","token_env":"ALBY_INTERNET_TOKEN" }, "skills":[ {"id":"web_search","description":"Search web and summarize","instruction_template":"Search '{{query}}'","parameters":{"query":"string"}} ] }
```

Testing & CI pointers
- Add unit tests for the publisher to validate `data_store.json` contains `agents.<name>.capabilities` when capability file present.
- Recommended CI steps: run publisher with a canned `out/status.json`, validate schema, run minimal smoke UI tests (or `--dry-run`).

Notes for Alby 0.3
- Reuse capability schema and `auth` patterns (env-token) for secret handling.
- Implement `--dry-run` and local-only modes for safe development (GAIA already uses `PROTOTYPE_USE_LOCAL_EVENTS=1`/`DRY_RUN`).
- Provide a lightweight job runner for install/CI tasks (ThreadPoolExecutor), wrap external calls with timeouts and capture logs.
- Emit GAIA-style NDJSON events and write concise audit rows to `gaia.db` for any state-changing operations.

References (in-repo)
- `AILocalModelLibrary/AGENT_TASKS/agent_runtime/alby_0_2/AGENT_CAPABILITIES.md`
- `AILocalModelLibrary/AGENT_TASKS/agent_runtime/alby_0_2/AGENT_0_2_BUILD_GUIDE.md`
- `AILocalModelLibrary/AGENT_TASKS/agent_runtime/alby_0_2/internet_capable_agent.json`
