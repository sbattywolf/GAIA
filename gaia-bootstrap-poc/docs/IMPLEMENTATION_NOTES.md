# Implementation Notes

## Validated now

- One process and explicit wiring.
- One read capability.
- One-resource provider contract.
- Home label resolution outside the adapter.
- Canonical GAIA identity separated from the external resource reference.
- Deterministic fake observations.
- Explicit success, ambiguity, unavailability, stale, unsupported, and failure outcomes.
- Provider replacement through the same contract.

## Deliberately deferred

- Batch reads and `PartialSuccess` execution.
- Policy engine and emission of `Denied` or `Indeterminate`.
- Real Home Assistant communication.
- Telegram.
- Memory, Registry, Planner, Event Bus, workflow, plugins, persistence,
  provider selection, and distributed coordination.

`PartialSuccess`, `Denied`, and `Indeterminate` remain in the outcome vocabulary
because they are named by the approved scenario, but this single-resource
bootstrap does not manufacture flows that need them.
