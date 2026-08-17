# GAIA Home Assistant Adapter Evidence Catalogue

## Status

`evidence-catalogue`

This document records what is currently evidenced for the real Home Assistant
Adapter boundary. It does not implement the Adapter and does not decide ADR-0004.

## Scope

The target remains the existing bootstrap slice:

> read the current opening state for one bounded Home entry Resource.

The intended seam is:

`HomeResourceReference -> OpeningStateProvider -> Observation`

The existing design explicitly keeps Home Assistant transport, credentials,
entity identifiers and protocol details outside Core and outside the
Capability contract.

## Evidence already established by the Bootstrap POC

The repository already provides deterministic evidence for:

- `ResourceId` being distinct from `HomeResourceReference`;
- Home label resolution occurring before the provider call;
- a single-resource `OpeningStateProvider` contract;
- `Observation` carrying the external reference, state and timezone-aware
  observation time;
- structured outcomes for success and uncertainty/failure conditions;
- provider exceptions being isolated at the Capability boundary;
- source-unavailable and stale observations not being silently replaced by
  inferred or last-known state;
- provider replaceability without changing Router, Resolver, Capability or
  outcome model.

The Bootstrap project history records 15 deterministic tests passing and lists
real Home Assistant communication, real freshness policy and several real
Adapter semantics as deliberately deferred.

## Evidence available about the proposed real Adapter

`REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md` defines a bounded external Adapter that
would:

1. accept an already-resolved `HomeResourceReference`;
2. perform one bounded Home Assistant read;
3. validate the external response;
4. translate verified source state into the existing Observation vocabulary;
5. preserve a timezone-aware observation timestamp;
6. expose technical failures through the existing provider boundary;
7. keep authentication and secrets at the integration boundary;
8. emit only sanitised diagnostic evidence.

The design also explicitly prohibits turning the Adapter into an inventory
importer, semantic resolver, cache, state store, action executor or source of
GAIA Resource identity.

## What is NOT yet evidenced

The repository does not currently provide sufficient evidence to implement a
real Adapter without making architectural assumptions.

### 1. Real Home Assistant state catalogue

Not established:

- exact source values for the selected opening entities;
- which values mean OPEN;
- which values mean CLOSED;
- which values mean UNAVAILABLE;
- which values must be treated as invalid/unknown.

The current Fake Adapter already accepts `ObservationState` directly, so it
cannot establish the external mapping.

### 2. Missing-entity semantics

Still open whether a missing entity should become:

- `SourceUnavailable`; or
- generic `Failure`.

No current implementation evidence closes this decision.

### 3. Freshness semantics

Still open:

- which HA timestamp/signal is authoritative;
- whether the timestamp is source-observation time or transport time;
- the freshness threshold;
- which layer owns the freshness decision.

The POC contains `STALE`, but the existence of that vocabulary is not evidence
for a real HA freshness rule.

### 4. Transport and timeout behaviour

The Adapter design requires bounded failure behaviour, but the repository does
not establish a final real transport/client choice or retry/backoff policy.

Therefore no retry framework or generic HTTP infrastructure should be added as
part of this evidence step.

### 5. Authentication and secret handling

The design establishes the boundary rule: credentials must remain runtime
configuration and must never enter GAIA contracts, fixtures, logs or evidence.

It does not yet establish the concrete runtime configuration mechanism for a
real HA connection.

### 6. Real API response validation

The real response schema has not been evidenced sufficiently to justify a
production-like parser or mapping implementation.

Malformed body, missing required fields, invalid timestamps and reference
mismatch remain required deterministic tests once a real response contract is
known.

## Legacy/reference evidence

The current GAIA documentation refers to a legacy `AI-HOME` implementation as
reference-only technical evidence, including a historical `ha_client.py`.

However, the current repository checkout does not expose that referenced
`ha_client.py` as a tracked file, and repository search does not currently
return it.

Therefore this catalogue does **not** claim to have inspected the legacy
implementation itself.

The legacy references may establish where earlier engineering expected HTTP
responses, timeouts, authentication headers and entity identifiers, but those
references are not sufficient to infer the current Home Assistant protocol or
GAIA semantics.

No secret, private endpoint, household identifier, raw response or legacy
runtime artefact is imported by this catalogue.

## ADR-0004 status

`adr/ADR-0004-HomeAssistant-Boundary.md` remains:

- Status: `Proposed`
- Decision: `Not yet made`

This catalogue therefore does not promote the external-Adapter design into an
accepted Home Assistant architecture.

The evidence currently supports a bounded Adapter experiment, not a final
decision about Home Assistant's overall architectural role.

## Minimum evidence needed before implementation

Before implementing `RealHomeAssistantAdapter`, obtain a sanitised, bounded
evidence set containing:

1. one or more representative responses for the selected opening Resource;
2. the actual source state values and their observed meanings;
3. the available observation/freshness timestamp or signal;
4. missing-entity behaviour;
5. unavailable-state behaviour;
6. timeout/transport failure behaviour;
7. authentication/authorization failure behaviour;
8. malformed-response examples with secrets and private identifiers removed.

From that evidence, decide only the minimum semantics required by the
single-resource read scenario.

## Explicit non-goals

This evidence step does not introduce:

- a real HA client;
- an HTTP framework;
- retries/backoff;
- inventory discovery;
- caching;
- persistence;
- multi-resource aggregation;
- actions;
- Telegram;
- Planner;
- Event Bus;
- general Policy infrastructure.

## Current conclusion

**Architecture seam: sufficiently evidenced.**

**Real Home Assistant semantics: insufficiently evidenced.**

**ADR-0004: still open.**

The correct next increment is therefore evidence collection for one bounded
Home Assistant read, followed by an explicit review of the resulting mapping
and failure semantics. Implementation should begin only after that evidence
closes the minimum required questions.
