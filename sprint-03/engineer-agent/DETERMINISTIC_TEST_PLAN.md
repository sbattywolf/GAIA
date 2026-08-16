# DETERMINISTIC_TEST_PLAN

**Project:** GAIA Bootstrap POC  
**Scope:** Home read-only, single-resource bootstrap  
**Status:** Implemented and executed

## Purpose

Validate accepted GAIA boundaries before introducing real Home Assistant communication.

The test plan validates:

- Core boundary
- Domain responsibility allocation
- Capability model
- Adapter contract
- Structured outcomes
- Authority rules
- Replacement of Fake Adapter by another provider

## Determinism rules

All tests must be:

- reproducible;
- isolated;
- independent from network;
- independent from Home Assistant;
- independent from Telegram;
- independent from the current wall clock;
- driven by explicit fixture data.

## Components under validation

```text
RequestRouter
  -> ReadOpeningStateCapability
  -> HomeResourceResolver
  -> OpeningStateProvider
  -> FakeHomeAssistantAdapter
  -> Observation
  -> Outcome
```

## Fixed dataset

### Resource mappings

```text
kitchen window  -> home.window.kitchen       -> window_kitchen
bedroom window  -> home.window.bedroom.north -> window_bedroom_north
bedroom window  -> home.window.bedroom.south -> window_bedroom_south
office window   -> home.window.office        -> window_office
front door      -> home.door.front            -> front_door
garage door     -> home.door.garage           -> garage_door
```

### Provider states

```text
window_kitchen       = OPEN
window_bedroom_north = CLOSED
window_bedroom_south = CLOSED
window_office        = STALE
front_door           = CLOSED
garage_door          = UNAVAILABLE
```

### Test timestamp

Use one fixed timezone-aware timestamp for repeatability.

## Test suite A: happy path

### A1 Kitchen window open

**Request**

```text
operation = read_opening_state
resource_label = kitchen window
```

**Expected**

```text
Success
resource_id = home.window.kitchen
observation.state = OPEN
```

**Validates**

- explicit routing;
- Domain resolution;
- Capability delegation;
- source-grounded Observation.

### A2 Front door closed

**Expected**

```text
Success
resource_id = home.door.front
observation.state = CLOSED
```

## Test suite B: Domain resolution

### B1 Unknown label

**Input**

```text
moon window
```

**Expected**

```text
ClarificationRequired
provider calls = 0
```

### B2 Ambiguous label

**Input**

```text
bedroom window
```

**Expected**

```text
ResourceAmbiguous
candidate_ids = [
  home.window.bedroom.north,
  home.window.bedroom.south
]
provider calls = 0
```

This verifies that the Adapter does not choose semantic meaning.

## Test suite C: source conditions

### C1 Source unavailable

**Input**

```text
garage door
```

**Expected**

```text
SourceUnavailable
```

No current state is guessed and no last-known state is presented as current.

### C2 Information stale

**Input**

```text
office window
```

**Expected**

```text
InformationStale
observation.state = STALE
```

The bootstrap treats `STALE` as explicit deterministic fixture state. It does not yet define a real freshness policy.

## Test suite D: Adapter contract

### D1 Repeatable Observation

Two reads of the same reference return equal observations and the same fixed timestamp.

### D2 Missing external reference

A direct Fake Adapter call for a missing reference raises an Adapter-level lookup error. Through the Capability boundary, provider exceptions become structured `Failure`.

### D3 Time-awareness

Fake Adapter rejects a naive timestamp. Fixture timestamps are timezone-aware.

## Test suite E: Adapter robustness

### E1 Malformed provider response

A provider returning a dictionary instead of `Observation` produces:

```text
Failure(reason = provider returned malformed observation)
```

### E2 Provider exception

A simulated timeout produces a structured failure without leaking the exception message:

```text
Failure(reason = provider failure: TimeoutError)
```

### E3 Mismatched reference

If a provider returns an Observation for another external reference, the Capability returns `Failure`.

### E4 Invalid state type

If a provider returns an Observation with a state outside `ObservationState`, the Capability returns `Failure`.

## Test suite F: authority rules

### F1 Source wins

A separate inferred value says `CLOSED`, while the provider observation says `OPEN`.

**Expected:** returned outcome carries `OPEN`.

### F2 No last-known fallback

A separate last-known value says `OPEN`, while source is `UNAVAILABLE`.

**Expected:** `SourceUnavailable`.

## Test suite G: routing and scope

### G1 Unsupported operation

**Input**

```text
operation = open_door
```

**Expected**

```text
Unsupported
```

The read Capability is not executed.

## Test suite H: replaceability

### H1 Alternative provider

Replace `FakeHomeAssistantAdapter` with an independent class implementing `OpeningStateProvider`.

**Expected:** the same `RequestRouter`, `HomeResourceResolver`, `ReadOpeningStateCapability`, and outcome model work without modification.

## Deferred tests

The approved scenario vocabulary includes multi-Resource and Policy outcomes. They are not executed in the single-resource bootstrap:

- `PartialSuccess` from multi-Resource aggregation;
- `Denied`;
- `Indeterminate` Policy Result.

They must be introduced only with an approved flow that needs them.

## Architectural assertions

The plan succeeds only if:

```text
Core contains no Home-specific meaning.
Domain contains Home meaning.
Adapter contains external-state access only.
Capability is not an API client.
Entity IDs remain external references.
Telegram is absent.
Memory is absent.
```

## Execution result

The generated bootstrap package executed its deterministic suite successfully:

```text
15 passed
exit_code = 0
```

## Exit criteria

- Deterministic suite passes.
- Provider can be replaced.
- Router remains unchanged.
- Resolver remains unchanged.
- Capability remains unchanged.
- Outcomes remain unchanged.

## Next reviewed artefact

`BOOTSTRAP_DOMAIN_MODEL.md`
