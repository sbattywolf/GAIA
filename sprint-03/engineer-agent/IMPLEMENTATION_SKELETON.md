# IMPLEMENTATION_SKELETON

**Status:** Implemented  
**Project:** GAIA Bootstrap POC  
**Scope:** Home read-only, single-resource

## Purpose

Provide the smallest code structure capable of validating:

- Core boundary;
- Home Domain boundary;
- Capability model;
- Adapter replacement;
- deterministic tests.

No real Home Assistant integration, Telegram integration, Memory, Registry, or Planner is included.

## Repository structure

```text
gaia-bootstrap-poc/
├── pyproject.toml
├── README.md
├── TEST_RESULTS.txt
├── docs/
│   └── IMPLEMENTATION_NOTES.md
├── src/
│   └── gaia/
│       ├── __init__.py
│       ├── bootstrap.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── request_router.py
│       ├── home/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── outcomes.py
│       │   ├── resource_resolver.py
│       │   └── read_opening_state_capability.py
│       └── adapters/
│           ├── __init__.py
│           ├── contracts.py
│           └── fake_home_assistant_adapter.py
└── tests/
    ├── conftest.py
    ├── test_adapter_contract.py
    ├── test_adapter_robustness.py
    ├── test_authority_rules.py
    ├── test_domain_resolution.py
    ├── test_happy_path.py
    ├── test_replaceability.py
    ├── test_router.py
    └── test_source_failures.py
```

The tree is a practical starting shape, not canonical architecture.

## Module responsibilities

### `src/gaia/core/request_router.py`

Owns:

- bounded request shape;
- explicit operation routing;
- unsupported-operation outcome.

Does not own:

- Home label meaning;
- entity mapping;
- provider calls;
- Telegram formatting.

### `src/gaia/home/models.py`

Owns immutable domain values:

```text
ResourceId
HomeResourceReference
ObservationState
Observation
```

### `src/gaia/home/outcomes.py`

Owns structured outcome data types and type aliases.

### `src/gaia/home/resource_resolver.py`

Owns:

- minimal label normalisation;
- bounded mapping from Home label to resolved Resource;
- unknown Resource result;
- ambiguity result.

It never calls an external system.

### `src/gaia/home/read_opening_state_capability.py`

Owns:

- coordination of one read;
- provider invocation after successful resolution;
- validation of provider response;
- translation of unavailable/stale state to outcomes;
- isolation of technical provider exceptions.

It depends on `OpeningStateProvider`, not on the Fake class.

### `src/gaia/adapters/contracts.py`

Defines one `Protocol`:

```python
class OpeningStateProvider(Protocol):
    def get_opening_state(
        self,
        resource_reference: HomeResourceReference,
    ) -> Observation:
        ...
```

### `src/gaia/adapters/fake_home_assistant_adapter.py`

Owns deterministic in-memory state lookup.

It performs:

- no HTTP;
- no WebSocket;
- no authentication;
- no polling;
- no label resolution;
- no cache fallback;
- no random state changes.

### `src/gaia/bootstrap.py`

Composition root with explicit wiring:

```text
HomeResourceResolver
FakeHomeAssistantAdapter
ReadOpeningStateCapability
RequestRouter
```

No dependency injection container or Registry is used.

## Runtime flow

```text
Request(operation, resource_label)
  -> RequestRouter.handle
  -> ReadOpeningStateCapability.execute
  -> HomeResourceResolver.resolve
  -> OpeningStateProvider.get_opening_state
  -> Observation validation
  -> Structured Outcome
```

## Failure behaviour

- Unknown label -> `ClarificationRequired`
- Ambiguous label -> `ResourceAmbiguous`
- Provider `UNAVAILABLE` -> `SourceUnavailable`
- Provider `STALE` -> `InformationStale`
- Malformed value -> `Failure`
- Provider exception -> `Failure`
- Unsupported operation -> `Unsupported`

## Test progression implemented

### Phase 1

- kitchen window open;
- front door closed.

### Phase 2

- unknown Resource;
- ambiguous Resource;
- provider not called before successful resolution.

### Phase 3

- source unavailable;
- information stale;
- malformed response;
- provider exception.

### Phase 4

- source authority;
- no last-known fallback;
- unsupported operation;
- provider replaceability.

## Validation result

The generated package executed:

```text
15 passed
exit_code = 0
```

## Replacement criterion

The skeleton succeeds when another `OpeningStateProvider` can replace `FakeHomeAssistantAdapter` without changing:

```text
RequestRouter
HomeResourceResolver
ReadOpeningStateCapability
Outcome definitions
```

A deterministic test with an `AlternativeProvider` validates this seam.

## Deliberately deferred

- Real Home Assistant client
- Batch read
- `PartialSuccess` execution
- Policy engine
- `Denied` and `Indeterminate` execution
- Telegram
- Memory
- Registry
- Planner
- Event Bus
- Workflow or plugin system
- Persistence
- Provider selection
- Distributed coordination

## Next reviewed artefact

`REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md`
