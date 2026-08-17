# Live Home Assistant Read Evidence

## Status

`validated`

The GAIA experimental Home Assistant read path has completed its first
successful live integration test against the configured Home Assistant
instance.

## Scope

The validation used one already-selected Home Assistant resource:

`binary_sensor.sensore_porta_ingresso_opening`

The test exercised the real runtime path:

```text
HomeResourceReference
        |
        v
ExperimentalHomeAssistantAdapter
        |
        v
HomeAssistantHTTPTransport
        |
        v
Home Assistant /api/states/<entity_id>
        |
        v
Observation
```

## Result

The live integration test completed successfully:

`1 passed`

The test assertions established that:

- the configured entity reference was returned consistently;
- a timezone-aware `last_updated` value was present;
- the returned state mapped to an allowed `ObservationState`;
- the request used the real `HomeAssistantHTTPTransport`;
- runtime configuration was supplied outside the repository.

## Credential and privacy boundary

No Home Assistant token, private URL, or raw Home Assistant response is
recorded in this document.

Runtime configuration is supplied through files outside the repository:

```text
~/.config/gaia/home_assistant.env
~/.config/gaia/.secrets.env
```

The repository therefore contains no live credential material.

## Interpretation

This evidence validates the first end-to-end read-only integration path.

It does **not** establish:

- complete Home Assistant entity coverage;
- semantic entity discovery;
- friendly-name resolution;
- write/action support;
- multi-entity behavior;
- production readiness;
- equivalence with all behavior of the legacy 1070 agent.

The legacy 1070 agent remains operational during this validation phase.

## Next validation target

The next runtime validation should use a second already-known opening/contact
entity from the legacy evidence, without introducing discovery or write
operations.

This preserves the current narrow proof boundary while demonstrating that the
adapter behavior is not specific to one entity.
