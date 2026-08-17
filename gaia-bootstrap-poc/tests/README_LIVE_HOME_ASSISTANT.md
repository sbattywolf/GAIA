# Optional Live Home Assistant Integration Test

This test is intentionally opt-in.

It never stores Home Assistant credentials, URLs, entity identifiers, or raw
responses in the repository. Values are supplied only through environment
variables at runtime.

Required variables:

```text
GAIA_HA_URL
GAIA_HA_TOKEN
GAIA_HA_ENTITY_ID
```

Example invocation:

```bash
GAIA_HA_URL="http://<sanitised-or-local-host>" GAIA_HA_TOKEN="<runtime-token>" GAIA_HA_ENTITY_ID="binary_sensor.<entity>" pytest -m integration gaia-bootstrap-poc/tests/test_real_home_assistant_integration.py
```

The test performs exactly one read of one already-selected entity.

It does not:

- discover entities;
- resolve friendly names;
- modify Home Assistant state;
- call conversation endpoints;
- store credentials;
- store raw Home Assistant responses;
- introduce retries or caching.

The test is skipped when the three environment variables are absent, so normal
Bootstrap test runs remain deterministic and offline.

## Evidence to record after a successful live run

Record only sanitised facts:

- HTTP read succeeded or failed;
- HTTP status class if available;
- source state category (`on`, `off`, `unavailable`, or another observed value);
- whether `last_updated` was present and timezone-aware;
- whether the returned `entity_id` matched the requested entity.

Do not commit:

- token values;
- private URLs;
- household names;
- private entity IDs;
- complete raw response payloads.
