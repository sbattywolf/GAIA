# PROTOTYPE_BOOTSTRAP_PROPOSAL

**Status:** Approved bootstrap proposal  
**Scope:** Minimal GAIA Home read-only prototype

## Purpose

Translate accepted GAIA architecture into the smallest implementation proposal capable of testing one real behaviour without integrating a real external system.

The prototype validates boundaries. It is not a production Home Assistant integration and does not include Telegram.

## Target behaviour

```text
Read current opening state
for one bounded home entry Resource.
```

Initial examples:

```text
Is the kitchen window open?
Is the front door open?
```

## Design principles

- One process
- Explicit wiring
- One read Capability
- One Resource per provider call
- Fake Adapter first
- Deterministic tests
- Structured outcomes
- No platform infrastructure before evidence

## Architectural flow

```text
Request
  -> RequestRouter
  -> ReadOpeningStateCapability
  -> HomeResourceResolver
  -> OpeningStateProvider
  -> FakeHomeAssistantAdapter
  -> Observation
  -> Structured Outcome
```

## Proposed components

### `RequestRouter`

**Responsibility:** deterministic routing of a bounded request to the correct Capability.

**Must not:** interpret Home labels, contain entity IDs, call Home Assistant, or format Telegram responses.

### `HomeResourceResolver`

**Responsibility:** convert bounded Home labels into canonical GAIA `ResourceId` plus an external `HomeResourceReference`.

**Must not:** call an Adapter or decide source state.

### `ReadOpeningStateCapability`

**Responsibility:** coordinate one read use case against explicit Resource scope and produce a structured outcome.

**Dependencies:** `HomeResourceResolver`, `OpeningStateProvider`.

**Must not:** become a concrete Home Assistant client.

### `OpeningStateProvider`

**Responsibility:** define the single-resource read boundary.

Conceptual operation:

```python
def get_opening_state(
    resource_reference: HomeResourceReference,
) -> Observation:
    ...
```

No batch operation is included in the bootstrap.

### `FakeHomeAssistantAdapter`

**Responsibility:** return deterministic source-like `Observation` values from an in-memory fixture.

**Must not:** perform network calls, resolve labels, aggregate groups, use secrets, cache state, or add background behaviour.

### Domain model

Minimum shared language:

```text
ResourceId
HomeResourceReference
ObservationState
Observation
Outcome
```

## Proposed Resource scope

The fixture may include:

```text
home.window.kitchen       -> window_kitchen
home.window.bedroom.north -> window_bedroom_north
home.window.bedroom.south -> window_bedroom_south
home.window.office        -> window_office
home.door.front           -> front_door
home.door.garage          -> garage_door
```

This is test data, not Home Assistant inventory discovery.

## Proposed deterministic states

```text
window_kitchen       = OPEN
window_bedroom_north = CLOSED
window_bedroom_south = CLOSED
window_office        = STALE
door_front           = CLOSED
door_garage          = UNAVAILABLE
```

## Outcomes in vocabulary

```text
Success
PartialSuccess
ClarificationRequired
ResourceAmbiguous
SourceUnavailable
InformationStale
Denied
Indeterminate
Unsupported
Failure
```

The single-resource bootstrap actively exercises only outcomes required by its flow. `PartialSuccess`, `Denied`, and `Indeterminate` remain vocabulary for later approved flows and are not manufactured artificially.

## Expected validations

### Core boundary

Core routes and returns outcomes. It does not interpret Home or call an external system.

### Domain boundary

Home semantics and ambiguity are resolved before provider invocation.

### Capability model

The read Capability stays implementation-neutral and depends on a provider contract.

### Adapter boundary

Fake Adapter only supplies external-state observations.

### Replaceability

An alternative `OpeningStateProvider` can replace the Fake Adapter without changing Core, resolver, Capability, or outcome model.

## Repository proposal

```text
src/
└── gaia/
    ├── bootstrap.py
    ├── core/
    │   └── request_router.py
    ├── home/
    │   ├── models.py
    │   ├── outcomes.py
    │   ├── resource_resolver.py
    │   └── read_opening_state_capability.py
    └── adapters/
        ├── contracts.py
        └── fake_home_assistant_adapter.py

tests/
├── conftest.py
├── test_happy_path.py
├── test_domain_resolution.py
├── test_source_failures.py
├── test_adapter_contract.py
├── test_adapter_robustness.py
├── test_authority_rules.py
├── test_router.py
└── test_replaceability.py
```

This physical layout is a bootstrap convenience, not canonical architecture.

## Explicit exclusions

- Batch reads
- Multi-Resource aggregation implementation
- Real Home Assistant communication
- Telegram transport or formatting
- Cache or last-known-state fallback
- Planner
- Registry
- Event Bus
- Workflow engine
- Plugin system
- General Memory
- Graph or vector storage
- Microservices
- Provider abstraction or provider selection
- Distributed coordination
- Broad inventory import

## Risks and controls

| Risk | Control |
|---|---|
| Home logic leaks into Core | Router accepts operation and label but delegates interpretation. |
| Adapter resolves labels | Resolver produces external reference before provider call. |
| Entity ID becomes canonical identity | Separate `ResourceId` and `HomeResourceReference`. |
| Fake hides failures | Fixtures include `UNAVAILABLE`, `STALE`, missing reference, and malformed provider. |
| Natural-language inference overrides state | Outcome carries the source-grounded `Observation`. |
| Test nondeterminism | Fixed data and fixed timezone-aware timestamps. |
| Premature architecture | New concepts require a failing test or real-domain evidence. |

## Decisions validated

- Provider is single-resource for the bootstrap.
- Observation remains minimal.
- Wiring remains explicit.
- Fake data is deterministic and in memory.
- No Telegram or real Home Assistant integration enters this stage.
- Shared subsystems are deferred until multiple real cases demonstrate a need.

## Exit criteria

The proposal is validated when:

1. Happy-path and failure tests pass deterministically.
2. Unknown and ambiguous labels do not invoke the provider.
3. Unavailable and stale states remain explicit.
4. Malformed provider responses become structured failure.
5. Unsupported operations do not execute the read Capability.
6. An alternative provider replaces the Fake without modifying Core or Domain flow.

## Next reviewed artefact

`DETERMINISTIC_TEST_PLAN.md`
