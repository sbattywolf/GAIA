# PROJECT_HISTORY

## Purpose

Record validated project progression, artefacts, implemented components, observed limitations, and next reviewed steps. This file is historical evidence, not a replacement for accepted ADRs.

## Architecture foundation

### Completed before the current bootstrap implementation

- GAIA Foundation Model consolidated.
- ADR-0001 Core Boundary accepted.
- ADR-0003 Capability Model accepted.
- Architecture-to-Code responsibility mapping prepared.
- Concrete Home examples prepared.
- First Home read-only scenario approved for validation.
- Memory role validation defined, with “no Memory required yet” accepted as a valid result.
- Repository and roadmap guidance prepared.

## Current sprint: Home read-only Bootstrap POC

### Goal

Validate that GAIA can read one bounded home-entry state through a replaceable Adapter while keeping Core and Home Domain independent from a real external system.

### Scope

```text
Read current opening state
for one bounded home entry Resource.
```

### Artefacts produced

- `POC_REUSE_ASSESSMENT.md`
- `PROTOTYPE_BOOTSTRAP_PROPOSAL.md`
- `DETERMINISTIC_TEST_PLAN.md`
- `BOOTSTRAP_DOMAIN_MODEL.md`
- `IMPLEMENTATION_SKELETON.md`
- `PROJECT_HISTORY.md`

### Decisions validated

- Use one process.
- Use explicit wiring.
- Keep provider contract single-resource for the bootstrap.
- Keep Observation minimal.
- Separate canonical `ResourceId` from `HomeResourceReference`.
- Keep Home label resolution in Home Domain.
- Keep provider calls behind `OpeningStateProvider`.
- Use Fake Adapter before real integration.
- Use deterministic tests before natural-language quality.
- Keep Telegram outside the bootstrap.
- Introduce complexity only when tests or real cases justify it.

### Components implemented

- `ResourceId`
- `HomeResourceReference`
- `ObservationState`
- `Observation`
- Structured outcome classes
- `OpeningStateProvider`
- `HomeResourceResolver`
- `ReadOpeningStateCapability`
- `RequestRouter`
- `FakeHomeAssistantAdapter`
- Explicit bootstrap composition root

### Deterministic behaviours validated

- OPEN success
- CLOSED success
- Unknown label
- Ambiguous label
- Provider not called for unresolved label
- Source unavailable
- Information stale
- Malformed provider response
- Provider exception isolation
- Unsupported operation
- Source-grounded Observation wins over inference
- No last-known fallback when source is unavailable
- Repeatable Fake observation
- Missing Fake reference has no fallback
- Provider replaceability

### Test result

```text
15 passed
exit_code = 0
```

### Architectural result

The provision of state can be replaced without modifying:

```text
RequestRouter
HomeResourceResolver
ReadOpeningStateCapability
Outcome model
```

This validates the intended separation between Core, Home Domain, Capability, and Adapter for the bootstrap scope.

### Deliberately deferred

- Multi-Resource batch API
- Multi-Resource aggregation and `PartialSuccess`
- Real freshness policy
- Real Home Assistant communication
- Telegram integration
- Policy engine and active `Denied`/`Indeterminate` handling
- General Memory
- Registry
- Planner
- Event Bus
- Workflow engine
- Plugin system
- Provider abstraction
- Persistence and distributed coordination

### Known open questions for the real Adapter

1. How should a missing Home Assistant entity map: `SourceUnavailable` or `Failure`?
2. Which real Home Assistant timestamps or signals can safely establish freshness?
3. Which source states map to `OPEN`, `CLOSED`, `UNAVAILABLE`, or failure?
4. Which technical failures should remain a generic `Failure`, and which deserve explicit mapping?
5. Does the validated provider contract remain sufficient under real API behaviour?

These questions require evidence from a sanitised Reference Implementation or from controlled real Adapter tests. No answer is assumed in the bootstrap.

## Reference repository status

A legacy/reference repository named `AI-HOME` was identified by the Human Owner under `oldRepoReferences`. Its content was not retrievable through the available Microsoft 365 search connection during this sprint. It therefore has not yet influenced implementation decisions.

When accessible, it must be treated as Reference Implementation only and assessed using:

```text
Reuse directly
Reimplement using lessons learned
Reference only
Reject
```

Secrets, `.env`, `.secret`, tokens, private URLs, household logs, backups, keys, and VPN configuration must not be imported.

## Next reviewed step

Prepare and review:

```text
REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md
```

The design must preserve the existing `OpeningStateProvider` seam unless real evidence demonstrates a necessary change. Telegram remains later in the roadmap.

## ADR review status

No accepted ADR change is proposed by the Bootstrap POC. Revisit accepted boundaries only if real implementation pressure materially challenges them or after evidence from additional active Domains.
