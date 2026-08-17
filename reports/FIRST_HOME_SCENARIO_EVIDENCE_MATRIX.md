# First Home Scenario Evidence Matrix

## Status

`evidence review`

This document records the evidence currently present in the Bootstrap POC
against the planned first Home scenario.

It does not promote any Proposed ADR to Accepted status.

## Scope

The scenario is the bounded, read-only opening-state flow described by
`sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md`.

The repository records a successful Bootstrap test run:

- exit code: 0
- 15 tests passed
- runtime reported: 0.30s

This matrix treats those tests as implementation evidence for the specific
behaviours they exercise. It does not infer evidence for behaviours that are
not tested.

## Evidence matrix

| Validation concern | Current evidence | Status |
|---|---|---|
| Explicit read-only routing | `test_router.py` rejects `open_door` as `Unsupported` | demonstrated |
| Basic read success | `test_happy_path.py` verifies kitchen window and front door results | demonstrated |
| GAIA Resource identity | happy-path tests assert `ResourceId` values distinct from request labels | demonstrated |
| Unknown label | `test_domain_resolution.py` returns `ClarificationRequired` without provider execution | demonstrated |
| Ambiguous label | `test_domain_resolution.py` returns `ResourceAmbiguous` with candidates without provider execution | demonstrated |
| Source unavailable | `test_source_failures.py` returns `SourceUnavailable` | demonstrated |
| Stale information | `test_source_failures.py` returns `InformationStale` and preserves observation state | demonstrated |
| Malformed provider result | `test_adapter_robustness.py` maps malformed data to structured `Failure` | demonstrated |
| Provider exception | `test_adapter_robustness.py` maps a simulated timeout to structured `Failure` without exposing the technical message | demonstrated |
| Observation timestamp discipline | `test_adapter_contract.py` requires timezone-aware `observed_at` and checks repeatability | demonstrated for fake provider |
| Source authority | `test_authority_rules.py` verifies source state is returned and unavailable state is not replaced by last-known state | demonstrated |
| Provider replaceability | `test_replaceability.py` substitutes an alternative provider without changing Core/Domain flow | demonstrated |
| Real Home Assistant translation | no real HA response fixture or real integration test is present in this evidence set | not demonstrated |
| Real HA authentication/configuration | no concrete runtime evidence | not demonstrated |
| Real HA timeout/transport behaviour | only simulated provider exception is tested | not demonstrated |
| Policy Result `Allowed/Denied/Indeterminate` | scenario brief requires it, but the current tests do not establish an operational Policy layer | not demonstrated |
| Multi-resource aggregation / PartialSuccess | ambiguity over multiple candidates is tested, but successful multi-resource aggregation is not | not demonstrated |
| Channel-neutral end-to-end rendering | current evidence stops at structured Router/Capability outcomes | not demonstrated |
| Memory independence | current Bootstrap scope does not require persistent Memory | partially demonstrated by scope, not an explicit acceptance test |

## What the 15 passing tests prove

The existing suite gives strong evidence for the small read-path seam:

```text
Request
  -> explicit Router
  -> Home Resource resolution
  -> bounded Capability
  -> OpeningStateProvider
  -> structured outcome
```

It also proves that several uncertainty and source-failure cases are kept
inside structured outcomes instead of becoming inferred success.

The provider replaceability test is especially relevant to the architectural
boundary: an alternative provider can satisfy the provider contract without
changing the Router or Home Domain flow.

## What the 15 tests do not prove

The passing suite must not be interpreted as proof that the entire first Home
scenario is complete.

In particular it does not establish:

- the real Home Assistant protocol mapping;
- the final Home Assistant boundary decision;
- operational Policy enforcement;
- a real channel Adapter;
- multi-resource result aggregation;
- production authentication or timeout configuration.

## Decision gate

The current evidence is sufficient to preserve the Bootstrap Core/Domain/
provider seam as a valid validation result.

It is **not** sufficient to accept ADR-0004.

It is also **not** sufficient to claim that the first Home scenario has passed
its complete validation brief.

## Recommended next experiment

The next implementation experiment should be the smallest possible real
Home Assistant Adapter integration for the already-defined
`OpeningStateProvider` contract.

Before connecting it to a live environment, define sanitized fixtures for:

1. one representative successful response;
2. one unavailable source;
3. one malformed response;
4. one timeout/transport failure;
5. one observation timestamp case.

The experiment should not add a general HTTP framework, retry subsystem,
registry, discovery, persistence, or action support.

## Exit condition for the next experiment

The experiment succeeds if the real Adapter can replace the fake provider while
leaving the existing Router, Capability, Resource model and structured
outcomes unchanged.

If that requires changing the Core or Capability contract, stop and review
ADR-0004 rather than hiding the change inside the implementation.

## Current conclusion

**Bootstrap read-path boundary: sufficiently evidenced.**

**First Home scenario: partially validated.**

**Real Home Assistant boundary: still open.**

**Next work: bounded real-Adapter experiment, not platform construction.**
