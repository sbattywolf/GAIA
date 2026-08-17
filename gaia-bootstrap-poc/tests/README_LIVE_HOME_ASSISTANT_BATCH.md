# Live Home Assistant batch validation

This validation extends the successful single-entity smoke test to a
controlled batch of already-known entities.

The entity list is supplied at runtime through:

```text
GAIA_HA_ENTITY_IDS
```

as a comma-separated list. The existing `GAIA_HA_ENTITY_ID` remains supported
as a single-entity fallback.

The batch test does not perform Home Assistant discovery. Every entity must
therefore be explicitly selected before the run.

Recommended first batch, based on entity IDs already observed in the
sanitised legacy repository evidence:

```text
binary_sensor.finestra_1
binary_sensor.finestra_2
binary_sensor.finestra_letto_dx_porta
binary_sensor.porta_1
binary_sensor.sensore_porta_ingresso_opening
binary_sensor.sensore_porta_ripostiglio_contact
binary_sensor.sensore_porta_sgabuzzino_contact
binary_sensor.sensore_porta_wc_opening
```

The test performs one read per configured entity and reports the complete
failure list if any read fails.

It asserts, for every successful read:

- returned entity reference matches the requested entity;
- `last_updated` is timezone-aware;
- state maps to the current opening-state contract.

It does not store raw Home Assistant responses, credentials, or private URLs.

Runtime configuration remains outside the repository:

```text
~/.config/gaia/home_assistant.env
~/.config/gaia/.secrets.env
```
