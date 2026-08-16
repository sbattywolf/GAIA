# BOOTSTRAP_DOMAIN_MODEL

**Status:** Approved minimal model  
**Scope:** GAIA Home read-only, single-resource bootstrap

## Purpose

Define the smallest shared language used by Core, Home Domain, Capability, Adapter, and deterministic tests.

This is not a universal model for all future Domains. New concepts require evidence from tests or real Domain pressure.

## Design principles

### GAIA owns canonical identity

`ResourceId` identifies the GAIA Resource. A Home Assistant identifier is an external reference and must not replace canonical identity.

### Observation is source-grounded

An `Observation` represents state returned through the provider boundary. Model inference or fluent explanation does not override it.

### Uncertainty remains visible

Ambiguity, unavailability, stale information, and conflict are not silently flattened.

### Structures stay small

A concept remains an enum or immutable data structure until a real case proves a subsystem is necessary.

## `ResourceId`

Canonical GAIA identity.

```python
@dataclass(frozen=True)
class ResourceId:
    value: str
```

Properties:

- stable within GAIA;
- independent of the external system;
- contains no execution behaviour.

Example:

```text
home.window.kitchen
```

## `HomeResourceReference`

External reference understood by a Home state provider.

```python
@dataclass(frozen=True)
class HomeResourceReference:
    value: str
```

Properties:

- Adapter-facing;
- not canonical GAIA identity;
- replaceable when integration mapping changes;
- contains no external-call behaviour.

Example fake value:

```text
window_kitchen
```

## `ObservationState`

```python
class ObservationState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    UNAVAILABLE = "UNAVAILABLE"
    STALE = "STALE"
```

### Meaning

- `OPEN`: provider reports open.
- `CLOSED`: provider reports closed.
- `UNAVAILABLE`: provider reports no current usable state.
- `STALE`: deterministic bootstrap state used to validate visible stale information.

The real Adapter design must re-evaluate how stale state is detected. The Fake does not establish a production freshness policy.

## `Observation`

```python
@dataclass(frozen=True)
class Observation:
    resource_reference: HomeResourceReference
    state: ObservationState
    observed_at: datetime
```

### Field responsibilities

- `resource_reference`: identifies the external subject read by the provider.
- `state`: source-grounded state translated into the bootstrap vocabulary.
- `observed_at`: timezone-aware observation timestamp.

### Explicitly absent

- confidence score;
- metadata bag;
- provider registry key;
- authority hierarchy;
- persistence identity;
- raw response payload;
- natural-language explanation.

## Resolution model

### `ResolvedResource`

Pairs canonical identity with its external reference:

```python
@dataclass(frozen=True)
class ResolvedResource:
    resource_id: ResourceId
    external_reference: HomeResourceReference
```

### `UnknownResource`

Represents no match for a Home label.

### `AmbiguousResource`

Represents multiple candidate Resources for the same label.

Resolution is a Home Domain concern. The Adapter never receives unresolved user text.

## Outcome model

### Active bootstrap outcomes

```text
Success
ClarificationRequired
ResourceAmbiguous
SourceUnavailable
InformationStale
Unsupported
Failure
```

### Vocabulary reserved for later approved flows

```text
PartialSuccess
Denied
Indeterminate
```

### Payloads

```text
Success
  resource_id
  observation

ClarificationRequired
  label

ResourceAmbiguous
  label
  candidate_ids

SourceUnavailable
  resource_id

InformationStale
  resource_id
  observation

Unsupported
  operation

Failure
  reason
```

Outcome payloads contain enough information for tests and later Channel formatting without putting formatting inside Domain or Core.

## Provider contract

```python
class OpeningStateProvider(Protocol):
    def get_opening_state(
        self,
        resource_reference: HomeResourceReference,
    ) -> Observation:
        ...
```

The contract is single-resource. No batch contract is approved for this bootstrap.

## Invariants

1. `ResourceId` and `HomeResourceReference` are not interchangeable.
2. Provider receives an external reference, never a user label.
3. Provider returns `Observation`, never natural-language text.
4. Fake timestamps are timezone-aware and deterministic.
5. Unknown and ambiguous labels are handled before provider invocation.
6. Source unavailable does not become a guessed current state.
7. Capability validates the provider response before producing success.

## Explicitly deferred

- Batch provider
- Multi-Resource aggregation model
- Freshness policy subsystem
- Provenance subsystem
- Confidence model
- Authority service
- General Memory
- Policy engine
- Registry
- Event model
- Planner
- Provider abstraction
- Audit platform
- Persistence

## Change rule

A new field, type, or subsystem enters only when at least one of the following exists:

- a deterministic test cannot be expressed correctly without it;
- a real Adapter case cannot be translated safely without it;
- a second validated Domain demonstrates a shared concern;
- accepted architecture is formally revised.

## Next reviewed artefact

`IMPLEMENTATION_SKELETON.md`
