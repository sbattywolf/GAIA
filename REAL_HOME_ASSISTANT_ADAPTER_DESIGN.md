# Real Home Assistant Adapter Design

**Status:** Design proposal; no implementation decision
**Scope:** Replacement of FakeHomeAssistantAdapter for the existing single-resource, read-only bootstrap POC
**Out of scope:** Client implementation, Home Assistant connection, Telegram, credentials, actions, inventory import, provider selection, Memory, Registry, Planner, Event Bus and ADR changes.

## 1. Purpose and Authority

This document describes only the next external Adapter needed to provide a real opening-state Observation through the existing OpeningStateProvider seam. It does not decide Home Assistant's final architectural role, alter the POC contract, or promote legacy design to GAIA architecture. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md), [gaia-bootstrap-poc/src/gaia/adapters/contracts.py](gaia-bootstrap-poc/src/gaia/adapters/contracts.py), [adr/ADR-0004-HomeAssistant-Boundary.md](adr/ADR-0004-HomeAssistant-Boundary.md)

Authority for the design is, in order: accepted ADRs where their status is reliable, current GAIA reference material, the first Home validation brief, POC code and tests, then sanitised legacy technical evidence. Legacy remains reference-only. [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md), [reference/ARCHITECTURE_CONVERGENCE_v0.2.md](reference/ARCHITECTURE_CONVERGENCE_v0.2.md)

## 2. ADR Status Contradictions

The repository contains unresolved status conflicts:

- adr/README and ADR_CANDIDATES state that all seven ADRs are Proposed/candidates. [adr/README.md](adr/README.md), [adr/ADR_CANDIDATES.md](adr/ADR_CANDIDATES.md)
- ADR-0001 declares itself Accepted. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md)
- ADR-0003 has a Proposed file and a separate Accepted file with the same decision content. [adr/ADR-0003-Capability-Model.md](adr/ADR-0003-Capability-Model.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md)
- ADR-0004, the specific Home Assistant boundary decision, remains Proposed and explicitly not decided. [adr/ADR-0004-HomeAssistant-Boundary.md](adr/ADR-0004-HomeAssistant-Boundary.md)
- The v0.2 reference documents remain Proposed and still describe ADR-0001/0003 as pre-prototype work. [reference/NEXT_STEPS_v0.2.md](reference/NEXT_STEPS_v0.2.md)

This design does not resolve those conflicts. Where it relies on ADR-0001 or the accepted copy of ADR-0003, it records that reliance explicitly; any boundary change requires Human Owner/Architect confirmation.

## 3. Existing Seam and Intended Placement

The existing provider contract accepts one HomeResourceReference and returns one Observation. It has no Home Assistant SDK type, entity schema, transport detail, credential or channel dependency. [gaia-bootstrap-poc/src/gaia/adapters/contracts.py](gaia-bootstrap-poc/src/gaia/adapters/contracts.py), [gaia-bootstrap-poc/src/gaia/home/models.py](gaia-bootstrap-poc/src/gaia/home/models.py)

The RealHomeAssistantAdapter should implement that seam at the external boundary:

HomeResourceReference → Home Assistant request/response translation → validated source-grounded Observation.

It must not resolve natural-language labels, rooms, areas, groups, ambiguity, Capability intent, Policy, Approval or channel formatting. Those responsibilities belong outside the Adapter. [reference/ARCHITECTURE_TO_CODE_v0.1.md](reference/ARCHITECTURE_TO_CODE_v0.1.md), [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

## 4. Adapter Responsibilities

The RealHomeAssistantAdapter is responsible for:

1. accepting a bounded, already-resolved HomeResourceReference;
2. using that reference only as an external Home Assistant lookup target;
3. performing the bounded read through a chosen HA client/transport;
4. validating the external response shape before producing an Observation;
5. translating verified external source state into the existing ObservationState vocabulary;
6. preserving a timezone-aware observed_at value based on evidence available from the source/transport;
7. exposing technical failures through the provider boundary so the existing Capability maps them to Failure;
8. keeping authentication, endpoint configuration and secrets at the integration boundary;
9. producing sanitised diagnostic evidence proportional to this read-only scenario.

It must not become an inventory importer, cache, semantic resolver, state store, generic HA client, action executor or source of GAIA Resource identity. [gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py](gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py), [gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md](gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md), [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md)

## 5. Contract and Mapping Boundary

The current method shape remains:

OpeningStateProvider.get_opening_state(HomeResourceReference) → Observation.

Observation carries the same external reference, an ObservationState and a timezone-aware observed_at. The Capability already rejects malformed observations, mismatched references and invalid state types; it maps provider exceptions to Failure, UNAVAILABLE to SourceUnavailable and STALE to InformationStale. [gaia-bootstrap-poc/src/gaia/adapters/contracts.py](gaia-bootstrap-poc/src/gaia/adapters/contracts.py), [gaia-bootstrap-poc/src/gaia/home/models.py](gaia-bootstrap-poc/src/gaia/home/models.py), [gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py](gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py)

HomeResourceReference is an external reference, not a GAIA ResourceId. The existing resolver maps the canonical ResourceId to that reference before the provider is called. The real Adapter must consume the reference; it must not derive it from labels or promote an HA entity identifier to canonical identity. [gaia-bootstrap-poc/src/gaia/home/resource_resolver.py](gaia-bootstrap-poc/src/gaia/home/resource_resolver.py), [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md)

The exact mapping from real HA source values to OPEN, CLOSED, UNAVAILABLE and STALE is **decisione non ancora determinata**. The project history specifically records this as an open question. The implementation phase must first collect a sanitised state catalogue for the selected, bounded opening Resources; unrecognised or structurally invalid source values must not be represented as confirmed OPEN/CLOSED. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

## 6. Unknown, Unavailable, Stale, Timeout and Errors

| Condition | Design treatment | Status |
|---|---|---|
| Unknown user label / ambiguous label | Must remain Home Domain resolution outcomes before any provider call. | Already exercised by POC. [gaia-bootstrap-poc/tests/test_domain_resolution.py](gaia-bootstrap-poc/tests/test_domain_resolution.py) |
| Missing or unknown HA entity for a resolved reference | SourceUnavailable or Failure is **decisione non ancora determinata**. It is an explicit open question. | Requires evidence and Architect/Human Owner decision. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md) |
| HA reports unavailable state | Translate only after verified state mapping; do not use cache/last-known state as current. | Required behaviour; concrete mapping requires evidence. [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md), [gaia-bootstrap-poc/tests/test_authority_rules.py](gaia-bootstrap-poc/tests/test_authority_rules.py) |
| Stale observation | Freshness rule ownership is ambiguous: the validation brief assigns freshness interpretation to Home Domain, while the POC provider vocabulary includes STALE. The threshold, timestamp source and final allocation are **decisione non ancora determinata**. | Requires evidence and architecture decision. [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md), [gaia-bootstrap-poc/src/gaia/home/models.py](gaia-bootstrap-poc/src/gaia/home/models.py) |
| Timeout or transport failure | Adapter must not fabricate state; it should expose a classified provider failure to existing Capability handling. Retry/backoff policy is **decisione non ancora determinata**. | Existing Capability produces Failure for provider exceptions. [gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py](gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py) |
| Authentication/authorization failure | Remain an Adapter-bound technical failure, with no secret in outcomes or logs. Whether it needs a distinct GAIA outcome is **decisione non ancora determinata**. | Requires evidence; Tool Trust is still Proposed. [adr/ADR-0006-Tool-Trust.md](adr/ADR-0006-Tool-Trust.md) |
| Malformed response or reference mismatch | Do not produce Observation. Raise/return a provider-level failure so existing Capability produces Failure; test both malformed shape and mismatched reference. | Existing guardrail. [gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py](gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py) |

The legacy HA client is evidence that HTTP responses, timeouts, authentication headers and entity identifiers occur at this external boundary. It does not determine protocol, timeout, response mapping or GAIA error semantics. [oldRepoReferences/AI-HOME/1070/app/ha_client.py](oldRepoReferences/AI-HOME/1070/app/ha_client.py), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

## 7. Authentication, Secrets and Sanitised Evidence

Authentication is an Adapter construction/transport concern, never part of HomeResourceReference, ResourceId, Capability definition, structured outcome or test fixture. The adapter should receive only a runtime-provided configuration/credential mechanism; no literal secret, private endpoint, household identifier or credential must enter source control, documentation, logs or exception messages. [AGENTS.md](AGENTS.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

Sanitised evidence may record: an opaque test reference, response-shape category, observed source-state category, timestamp presence/format category, failure class, timeout occurrence and expected GAIA outcome. It must not record tokens, URLs, private IPs, real entity identifiers, household names, raw response bodies, logs or backups. [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

## 8. Fake-versus-Real Adapter

| Aspect | FakeHomeAssistantAdapter | RealHomeAssistantAdapter design |
|---|---|---|
| State source | Deterministic in-memory map. | Bounded HA source read; transport/protocol is not yet selected. |
| Timestamp | Fixed timezone-aware value. | Source/transport-derived value; freshness meaning requires evidence. |
| Failures | Missing map key raises LookupError. | Missing entity, transport, timeout, authentication and malformed-response behaviour must be evidenced and mapped without fabricated state. |
| Secrets/network | None. | Boundary-local runtime configuration only; never exposed in GAIA contracts/evidence. |
| Mapping | Test fixture already uses ObservationState. | External state mapping must be explicitly evidenced before implementation. |
| Semantics | No external I/O. | Translate/validate external protocol only; no Domain interpretation. |

The Fake Adapter remains unchanged. [gaia-bootstrap-poc/src/gaia/adapters/fake_home_assistant_adapter.py](gaia-bootstrap-poc/src/gaia/adapters/fake_home_assistant_adapter.py)

## 9. Invariants Outside the Adapter

**Core:** Request routing and outcome handling remain unchanged; no HA types, HTTP, entity IDs, credentials or retries enter Core. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md), [gaia-bootstrap-poc/src/gaia/core/request_router.py](gaia-bootstrap-poc/src/gaia/core/request_router.py)

**Domain:** HomeResourceResolver continues to own label normalisation, known/unknown/ambiguous resolution and mapping from ResourceId to HomeResourceReference. It must not make HA calls. [gaia-bootstrap-poc/src/gaia/home/resource_resolver.py](gaia-bootstrap-poc/src/gaia/home/resource_resolver.py)

**Capability:** ReadOpeningStateCapability continues to coordinate one read through OpeningStateProvider and validate Observation shape/reference/state. It does not know the real HA client or protocol. [gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py](gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py)

## 10. Deterministic Test Design and Replaceability Evidence

Before any live integration test, use a deterministic transport/client double behind the prospective Adapter boundary. The test suite must cover:

1. a valid external response mapped to OPEN and to CLOSED, using synthetic references and timestamps;
2. a source unavailable response once its state mapping is evidenced;
3. stale data once the freshness rule, timestamp source and owner are decided;
4. missing entity behaviour after the SourceUnavailable-versus-Failure decision;
5. timeout and transport exceptions with no fallback state;
6. authentication/authorization errors without secret leakage;
7. malformed body, missing required fields, invalid timestamp and response/reference mismatch;
8. proof that the Adapter performs no label, area, group or ambiguity resolution;
9. the existing end-to-end POC outcomes with RealHomeAssistantAdapter substituted for FakeHomeAssistantAdapter.

Replaceability is demonstrated when the same RequestRouter, HomeResourceResolver, ReadOpeningStateCapability and outcome model pass their relevant tests with the real Adapter implementation; only composition wiring changes. This is the already-established seam and no new provider abstraction is introduced. [gaia-bootstrap-poc/tests/test_replaceability.py](gaia-bootstrap-poc/tests/test_replaceability.py), [sprint-03/engineer-agent/IMPLEMENTATION_SKELETON.md](sprint-03/engineer-agent/IMPLEMENTATION_SKELETON.md), [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md)

## 11. Conclusion and Minimum Next Increment

**Already supported by ADR/documentation:** a minimal in-process Core must delegate external work; Home semantics stay outside Core; Capability stays separate from execution binding; ResourceId differs from external reference; the first slice is one low-risk read with explicit uncertainty and a replaceable Adapter. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md), [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md)

**Requires evidence:** actual HA response shapes and source-state catalogue, timestamp/freshness signals, timeout/error behaviour, missing-entity semantics, and sanitised configuration/secret handling. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

**Requires Architect/Human Owner decision:** resolution of ADR status contradictions; the HA boundary decision in ADR-0004; missing-entity mapping; freshness ownership and threshold; retry policy; and whether authentication failures need a GAIA-specific outcome. [adr/ADR-0004-HomeAssistant-Boundary.md](adr/ADR-0004-HomeAssistant-Boundary.md), [adr/ADR-0006-Tool-Trust.md](adr/ADR-0006-Tool-Trust.md)

**Minimum incremental path to a real Adapter:** first obtain a sanitised, bounded evidence catalogue and the listed decisions; then implement one Adapter that satisfies the unchanged OpeningStateProvider contract, uses one direct read path for the selected references, and passes deterministic doubles plus the existing replacement test. Do not add Telegram, bulk inventory, actions, caching, general policy, provider selection or architectural infrastructure. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md), [gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md](gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md)
