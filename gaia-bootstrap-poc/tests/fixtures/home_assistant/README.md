# Home Assistant State Fixtures

These fixtures are sanitised, deterministic examples shaped around the
Home Assistant state fields observed in the legacy `ha_client.py` integration:

- `entity_id`
- `state`
- `last_updated`
- `attributes.device_class`
- `attributes.friendly_name`

They are **not captured production responses** and contain no household,
endpoint, credential, or private entity data.

The `on` / `off` / `unavailable` mappings are experimental test assumptions
for the current Adapter experiment. They are not an accepted GAIA Home
Assistant state policy.

The fixtures exist to prove response parsing and explicit mapping without
introducing network access.
