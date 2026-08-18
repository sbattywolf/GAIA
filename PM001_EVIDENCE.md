# PM-001 Evidence

## Scenario

**PM-001 — Repeatable Bounded Domestic Resource Read**

Concrete Resource:

`home.light.living_room`

Provider reference used in deterministic fixtures:

`light.living_room`

Capability:

`Read Current Resource State`

Operation:

`Read`

Scope:

exactly one Resource.

No write/service execution is exercised or introduced.

## Run identity

- Engineer validation run: `PM001-ENGINEER-CONTROLLED-001`
- Repository baseline: `459861de04f90f64dec9287619a3f3a8340b1750`
- Execution mode: deterministic reconstructed baseline harness
- Validation timestamp: `2026-08-18T19:21:37+00:00`
- Human Owner local checkout execution: **not performed by Engineer**

## Test execution

The Engineer reconstructed the relevant W3 implementation from the exact
baseline commit and executed the W3 predecessor test family together with
the new PM-001 P01–P14 suite.

Command:

```text
PYTHONPATH=src pytest -q tests/test_w3_single_home_read.py tests/test_pm001_repeatable_bounded_read.py
```

Result:

```text
24 passed
```

Breakdown:

- W3 T01–T10: **10/10 PASS**
- PM-001 P01–P14: **14/14 PASS**
- Combined: **24/24 PASS**

This is Engineer-workspace validation against a reconstructed snapshot of
the specified baseline. It is **not** a substitute for the Human Owner's
authoritative local validation.

## P01–P14

| ID | Requirement | Result | Boundary evidence |
|---|---|---|---|
| P01 | Valid Light read | PASS | one Resource, one Capability call, one provider call |
| P02 | Repeated valid reads | PASS | 5 controlled runs; 5 Capability calls; 5 provider calls |
| P03 | Resource not found/unresolvable | PASS | explicit `ResourceNotFound`; zero provider calls |
| P04 | Malformed Resource Reference | PASS | explicit `InvalidResourceReference`; zero external transport calls |
| P05 | Home Assistant unavailable | PASS | explicit `SourceUnavailable` |
| P06 | Unexpected/malformed response | PASS | explicit `ExecutionFailure` |
| P07 | Stale/inconsistent response | PASS | explicit `InformationStale` |
| P08 | Policy Denied | PASS | zero Capability calls; zero provider calls |
| P09 | Policy Indeterminate | PASS | zero Capability calls; zero provider calls |
| P10 | Approval Required, not granted | PASS | zero Capability calls; zero provider calls |
| P11 | Approval Required, granted | PASS | exactly one Capability call; exactly one provider call |
| P12 | Write attempt | PASS | `Unsupported`; zero provider calls |
| P13 | Out-of-scope request | PASS | `Unsupported`; zero provider calls |
| P14 | Evidence reconstruction | PASS | required sanitized fields represented and serializable |

## Repeatability evidence

Five controlled permitted reads of the same request produced:

```text
Resource: home.light.living_room
Capability: Read Current Resource State
Policy: Allowed
Approval: Not Required
Capability calls: 1, 1, 1, 1, 1
Provider calls: 1, 1, 1, 1, 1
```

No persistent architectural state was introduced to support repetition.

## Policy / Approval evidence

```text
Allowed + Not Required
    → exactly one Capability/provider execution

Denied
    → zero Capability/provider execution

Indeterminate
    → zero Capability/provider execution

Required + Not Granted
    → zero Capability/provider execution

Required + Granted
    → exactly one Capability/provider execution
```

The existing W3 Core gate remains the enforcement boundary. PM-001 does not
move Policy/Approval semantics into the Capability.

## Resource / provider boundary

Resource identity remains:

`home.light.living_room`

Provider reference remains:

`light.living_room`

The PM-001 changes do not introduce discovery, registry, provider routing,
or a second Resource.

Light state semantics remain source-grounded:

`ON`, `OFF`, `UNAVAILABLE`, `STALE`.

No ON/OFF → OPEN/CLOSED conversion exists in the PM-001 change.

## Evidence sanitization

No credentials, tokens, private endpoints, raw Home Assistant payloads,
household secrets, or unnecessary personal information are included.

## Architectural classification

**SUPPORTED**

Rationale: the controlled PM-001 evidence demonstrates that the existing
W3 bounded Core → Collaborator → Capability → one Resource → bounded Home
execution path remains repeatable and reconstructable under deterministic
conditions without adding architectural state or broadening the scenario.

This classification is based on the evidence above, not merely on test
pass status.

## Protected architecture

- ADR-0001: **not modified**
- ADR-0003: **not modified**
- Proposed documents: **not promoted**
- New Capability: **none**
- New Resource type: **none**
- Generic Provider framework: **none**
- Generic Policy/Approval framework: **none**
- Registry: **none**
- Planner/Memory/Event Bus/Workflow/Plugin: **none**
- Multi-Resource orchestration: **none**
- Multi-Domain orchestration: **none**
- Write/service operation: **none**

## Authoritative Human Owner local validation

The Human Owner applied the PM-001 implementation package to the
authoritative local checkout based on repository baseline:

`459861de04f90f64dec9287619a3f3a8340b1750`

Human Owner local validation:

```text
PM-001 P01–P14: PASS (14/14)
W3 T01–T10: PASS (10/10)
Combined: PASS (24/24)
