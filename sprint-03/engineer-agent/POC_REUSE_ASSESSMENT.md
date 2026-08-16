# POC_REUSE_ASSESSMENT

**Status:** Reviewed assessment  
**Scope:** GAIA Home read-only vertical slice  
**Assessment basis:** GAIA Source of Truth and the implementation path approved during the current sprint. The legacy reference repository was not available for direct source inspection when this assessment was completed.

## Purpose

Assess which parts of a legacy Home Assistant / Telegram PoC may be:

- **Reuse directly**
- **Reimplement using lessons learned**
- **Reference only**
- **Reject**

The working PoC must not silently become GAIA architecture. This assessment does not change accepted ADRs and does not approve production integration code.

## Scope

In scope:

> Read current opening state for a bounded set of home entry Resources.

The first implementation uses one process, explicit wiring, a small Resource set, one read Capability, a Fake Home Assistant Adapter, structured outcomes, and deterministic tests. A real Home Assistant Adapter comes later. Telegram integration comes only after the real Adapter stage.

Out of scope:

- Act operations
- Broad Home Assistant inventory import
- Telegram runtime integration
- General Planner, Registry, Event Bus, Workflow engine, Plugin system, Memory subsystem, graph database, vector store, microservices, provider abstraction, or distributed coordination

## Authority order used

1. Accepted ADRs
2. GAIA Foundation Model and glossary-level concepts
3. Context Model and World Model
4. Architecture to Code guidance and examples
5. First Home Scenario Validation
6. Memory Role Validation
7. Roadmap and Repository Guidance
8. Legacy PoC
9. Implementation preferences

If the PoC conflicts with a higher-authority GAIA source, GAIA wins.

## Facts

- Core is a small in-process coordination and enforcement boundary.
- Home-specific interpretation, Home Assistant details, and Telegram details do not belong in Core.
- A Capability describes what may be requested or performed against an explicit Resource scope. It is not the Adapter or Tool that executes it.
- Home Assistant entity IDs are external Resource references, not canonical GAIA Resource identities.
- Home Domain resolves labels and bounded Resource sets.
- Home Assistant Adapter reads external state and translates it into the provider contract.
- The approved first slice is Read, Low risk, and has no Approval by default.
- Ambiguity, stale information, unavailable sources, partial knowledge, and conflict remain visible.
- Work order is PoC assessment, bootstrap proposal, Fake Adapter, deterministic tests, real Home Assistant Adapter, then Telegram.

## Assumptions

These assumptions describe likely legacy content. They are not verified facts:

- The legacy PoC may contain Home Assistant client code, Telegram handlers, entity mappings, configuration, tests, Docker files, and error-handling lessons.
- Some legacy modules may couple channel handling, Home interpretation, application flow, and external API calls.
- Legacy configuration or logs may contain household-sensitive data or secret references.

No assumption authorises reuse. Every item must pass an evidence gate.

## Unknowns

Until a sanitised repository is inspected, the following remain unknown:

- Exact modules and responsibility boundaries
- Licence and third-party dependency constraints
- Test determinism and fixture safety
- Home Assistant API usage and error semantics
- Telegram polling or webhook design
- Secret handling
- Logging and household-data exposure
- Runtime and Docker coupling
- Whether individual utilities are independent of legacy architecture

## Classification rules

### Reuse directly

Allowed only when the item:

1. Is source-inspected and understood.
2. Has compatible licensing and dependencies.
3. Contains no secret, private URL, household identifier, or sensitive log.
4. Preserves GAIA responsibility boundaries.
5. Uses GAIA contracts and canonical Resource identity.
6. Is covered by deterministic tests.
7. Is smaller and clearer to reuse than to rewrite.

### Reimplement using lessons learned

Use when behaviour or operational knowledge is valuable, but original code shape conflicts with GAIA contracts, boundaries, sequencing, or testability.

### Reference only

Use to understand protocols, operational constraints, failure modes, naming, or user experience. Do not copy the implementation into the GAIA runtime.

### Reject

Use when an element violates accepted architecture, expands scope, weakens authority or uncertainty handling, exposes sensitive data, or introduces unapproved infrastructure.

## Assessment table

| PoC element or concern | Classification | Rationale | Evidence required |
|---|---|---|---|
| Pure, sanitised opening-state test data | Reuse directly, conditional | Potentially useful as deterministic fixtures if fully synthetic. | Prove no real entity IDs, URLs, names, timestamps, or logs. |
| Small pure utility with no Domain, Adapter, Channel, runtime, or configuration coupling | Reuse directly, conditional | Acceptable only where ownership already matches a GAIA responsibility. | Source, licence, dependency, and test review. |
| Deterministic tests expressed only as observable scenarios | Reuse directly, conditional | Scenario semantics may transfer without legacy implementation structure. | Confirm no live API, clock, network, Telegram, or household data. |
| Home Assistant request/response and authentication lessons | Reimplement using lessons learned | Protocol knowledge can guide the real Adapter; secrets and legacy coupling cannot transfer. | Sanitised protocol notes and API evidence. |
| Home Assistant state-normalisation logic | Reimplement using lessons learned | Source values must be translated at the Adapter boundary. | Enumerate real states and malformed/unavailable cases. |
| Human label to Home Assistant entity mapping | Reimplement using lessons learned | Label meaning belongs in Home Domain; entity ID stays an external reference. | Sanitised bounded mapping and ambiguity examples. |
| Query parsing or intent shortcuts | Reimplement using lessons learned | User examples are useful, but routing stays bounded and deterministic. | Sanitised utterances and expected Capability/scope. |
| Error handling and retry observations | Reimplement using lessons learned | Failure knowledge is useful, but technical errors must map to explicit outcomes. | Sanitised failure catalogue. |
| Telegram response wording or formatting | Reimplement using lessons learned, later | Channel formatting is separate and Telegram is a later stage. | Examples based only on structured outcomes. |
| Home Assistant client code | Reference only until real Adapter stage | May document endpoints and payloads but must be assessed against the validated contract. | Licence, dependency, timeout, error, freshness, and secret review. |
| Telegram bot handlers, polling, webhook, runtime | Reference only | Transport knowledge may be useful later but must not own Home behaviour. | Sanitised transport notes and separation proof. |
| Docker and deployment layout | Reference only | Historical runtime input, not GAIA architecture. | Minimal operational requirements. |
| Dependency manifest | Reference only | Useful for risk and library review; dependencies are not inherited wholesale. | Per-dependency necessity, security, and licence review. |
| README and operational runbook | Reference only | Useful if sanitised; may encode legacy assumptions. | Remove secrets, private URLs, household IDs, and PoC-only architecture. |
| Logs, traces, chat histories, Home Assistant backups | Reject | Sensitive and unnecessary for the assessment. | None. |
| `.env`, `.secret`, `secrets.yaml`, tokens, passwords, keys, VPN configuration | Reject | Secrets and private configuration must never enter the assessment package. | None. Use placeholder-only examples if needed. |
| Telegram handler that fetches Home state | Reject | Channel code must not own Home source access. | None for reuse. Reimplement responsibilities separately. |
| Core code with entity IDs, label matching, HTTP, or Telegram | Reject | These responsibilities are outside Core. | None for reuse. |
| Resource objects that call Home Assistant | Reject | Resource identifies a subject; external calls belong to an Adapter. | None for reuse. |
| Home Assistant entity ID as canonical GAIA Resource identity | Reject | External identifier must remain an external reference. | None for reuse. |
| Adapter that resolves rooms, floors, labels, or groups | Reject | Home semantic resolution belongs to Home Domain. | None for reuse. |
| Model text treated as current state | Reject | Source-grounded Observation remains authoritative. | None for reuse. |
| Cached last-known state presented as current | Reject | Unavailable current source must remain visible. | None for reuse. |
| Pick-first ambiguity behaviour | Reject | Ambiguity must produce explicit clarification or `ResourceAmbiguous`. | None for reuse. |
| Broad Home Assistant inventory import | Reject for current slice | Expands scope and encourages premature Registry-like design. | Separate future proposal. |
| Planner, Registry, Event Bus, Workflow, plugins, general Memory, graph/vector store, microservices, provider abstraction | Reject for current slice | Deliberately deferred. | Future architecture approval backed by evidence. |
| Act operations | Reject for current slice | The approved slice is read-only. | Separate Capability, Policy, risk, and Approval review. |

## Current disposition summary

### Reuse directly

No legacy production code is approved for direct reuse before inspection. Only small pure sanitised fixtures, scenario tests, or utilities may become candidates after passing every gate.

### Reimplement using lessons learned

Primary candidates:

- Home Assistant protocol and state-shape lessons
- Failure and freshness lessons
- Bounded label-to-external-reference lessons
- Sanitised user phrase examples
- Telegram formatting lessons in the later channel stage

### Reference only

Primary candidates:

- Existing Home Assistant client
- Telegram transport/runtime
- Docker and deployment layout
- Dependency manifest
- README and operational notes

### Reject

Reject secrets, sensitive artefacts, responsibility coupling, external IDs as canonical identity, hidden uncertainty, source guessing, broad inventory import, out-of-scope Act behaviour, and unapproved infrastructure.

## Architecture conflicts to look for

1. **Core pollution:** Home meaning, HTTP, entity IDs, Telegram, or formatting inside Core.
2. **Domain/Adapter inversion:** Adapter decides labels, locations, grouping, ambiguity, or aggregation.
3. **Capability collapse:** Capability implemented as an API client.
4. **Resource activation:** Resource executes external calls.
5. **Identity leakage:** Entity ID becomes canonical GAIA identity.
6. **Channel ownership:** Telegram fetches Home state or determines application behaviour.
7. **Authority violation:** Model text or cache overrides source-grounded Observation.
8. **Failure flattening:** Errors become generic text instead of structured outcomes.
9. **Scope expansion:** Broad inventory, Act operations, or platform machinery enters the first slice.
10. **Retention without evidence:** Clarifications become a general Memory subsystem.

Conflicts require reimplementation, rejection, or architecture review, never silent modification of accepted ADRs.

## Inspection checklist

Use only a sanitised source snapshot:

- [ ] Record repository and third-party licences.
- [ ] Inventory modules by observed responsibility.
- [ ] Identify every network boundary.
- [ ] Identify entity IDs and confirm they remain external references.
- [ ] Identify Channel, Domain, Core, and Adapter coupling.
- [ ] Catalogue source states and failures without household data.
- [ ] Identify clocks, retries, caches, globals, and background tasks.
- [ ] Check logs and fixtures for private data.
- [ ] Inspect configuration shape through placeholder-only examples.
- [ ] Assign one disposition and one reason to each item.
- [ ] Escalate architecture conflicts rather than changing ADRs.

## Decisions recorded

- No production code receives direct-reuse approval before source inspection.
- Home Assistant integration knowledge may be harvested, but the real client remains a later Adapter implementation.
- Telegram artefacts remain reference-only until the ordered Telegram stage.
- A sanitised inventory is the only acceptable basis for final item-by-item disposition.

## Recommended next artefact

`PROTOTYPE_BOOTSTRAP_PROPOSAL.md`

## Security note

Before placing personal Home Assistant or Telegram material in a Microsoft 365 business tenant, verify the applicable company policy. Never provide tokens, private URLs, household-sensitive logs, backups, or VPN configuration.
