# World Model

**Project:** GAIA  
**Document type:** Foundation Document  
**Status:** Proposed  
**Version:** 0.2  
**Supersedes:** `WORLD_MODEL.md`  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document defines the initial shared semantic World Model for GAIA.

It describes how GAIA refers to relevant Resources and source-scoped information about the world so that Domains and Collaborators can reason consistently about identity, observation, Assertion, Relationship, provenance, authority, time, uncertainty, and Conflict.

It answers:

> What common meaning does GAIA use when components represent or exchange information about the world?

It defines semantics, not a runtime component, persistence model, ontology platform, database schema, knowledge graph, Event model, digital twin, or implementation blueprint.

## 2. Architectural status

**World Model is a shared semantic model, not an architectural component.**

It refines how GAIA describes Resources and source-scoped information. It does not imply a central World Model service, database, graph, runtime boundary, or state store.

Components adhere to these semantics when they represent or exchange information about the world, but they do not depend on one World Model implementation and do not need the complete model.

World Model is not currently a first-class element of `GAIA_MODEL.md`. Promotion, runtime ownership, or dedicated implementation requires explicit review and, when material, an ADR.

## 3. Concept classification

The concepts defined here are semantic constructs, not automatically:

- first-class elements of `GAIA_MODEL.md`;
- runtime components;
- services;
- persisted entities;
- independent implementation abstractions.

`Resource Reference`, `Observation`, `Assertion`, `Relationship`, `Provenance`, `Authority`, `Temporal Validity`, `Uncertainty`, `Conflict`, and `World View` are building blocks for shared meaning. An implementation may represent several together when clear and sufficient for the validated scenario.

## 4. Scope

This document covers Resources and references, Observations and Assertions, Relationships, provenance, authority, temporal validity, uncertainty, Conflict, bounded World Views, human correction, and relationships with Context, Memory, Knowledge, Capabilities, Domains, and external systems.

It excludes database and graph choices, RDF, ontology languages, embeddings, Event sourcing, digital-twin platforms, synchronisation protocols, APIs, class hierarchies, identifier formats, conflict algorithms, programming languages, and deployment topology.

## 5. Definition

**The World Model is GAIA's shared semantic model for relevant Resources and the scoped Assertions, Observations, Relationships, provenance, authority, time, and uncertainty associated with them.**

It is selective. GAIA represents only what is needed for validated responsibilities.

It supports multiple source and Domain perspectives. It does not force premature global truth.

## 6. Goals

The World Model should allow GAIA to:

1. refer to Resources without coupling to one external system;
2. distinguish source evidence from inference;
3. preserve provenance and scoped authority;
4. represent changing information with temporal meaning;
5. expose uncertainty and conflicting claims;
6. provide bounded World Views to Context;
7. support human correction;
8. preserve Domain boundaries;
9. survive replacement of integrations, models, and runtimes;
10. grow only through validated scenarios.

## 7. Non-goals

It does not:

- represent everything in the Human Owner's life;
- create a complete ontology;
- mirror every external system;
- own all state;
- replace source systems;
- store raw conversation history;
- define Memory retention;
- serve as Audit;
- define execution state;
- become Shared Context;
- infer truth automatically;
- guarantee global consistency;
- predict all Domains;
- justify graph technology prematurely.

## 8. Principles

- **Relevance before completeness.**
- **Source before interpretation.**
- **Authority is scoped.**
- **Observation is not current fact by default.**
- **Inference remains visible.**
- **Time is part of meaning.**
- **Conflict is not hidden.**
- **External systems retain scoped authority.**
- **Context receives a bounded view.**
- **Human correction has priority within its scope.**

## 9. Resource

A Resource is an identifiable subject of observation, reference, reasoning, access, or action within a GAIA Domain.

A Resource may be physical, digital, external, or conceptual, but must have sufficient identity and boundary for GAIA to reason about its state, Relationships, or permitted use.

Examples may include a device, room, document, message, calendar item, person reference, service, external record, preference, model endpoint, or Capability target. Examples do not create official Resource types.

The World Model may describe a Resource without owning, controlling, or storing it.

## 10. Resource Reference

A Resource Reference identifies or locates a Resource within a source, Domain, or interaction. It is not the Resource itself.

References may be external identifiers, Domain-local identifiers, user labels, location-qualified names, Relationship-based references, or temporary interaction references.

Similar labels do not prove identical Resources. Ambiguity remains visible and may require clarification. Resolution algorithms are outside this document.

## 11. Assertion

An Assertion is a claim about a Resource, Relationship, condition, or concept made by an identified source.

Assertions may be:

- stated by the Human Owner;
- reported by an external system;
- derived deterministically;
- inferred by a model or heuristic;
- proposed by a Collaborator;
- accepted through confirmation.

An Assertion records that a source made or supports a claim. It is not universally true outside its authority, scope, and validity.

A Fact is not a separate primitive. It is an Assertion GAIA is justified in treating as authoritative within a defined scope and validity period.

## 12. Observation

An Observation is a source-grounded kind of Assertion describing what a source reported, measured, or returned at a relevant time.

The initial model does not require Observation and Assertion to be separate implementation types. The distinction is semantic: an Observation preserves source and time; other Assertions may be stated, derived, inferred, proposed, corrected, or confirmed.

An Observation may require subject, property, value, source, observation or retrieval time, Domain, freshness, quality, and limitations.

It is not automatically current, authoritative, persistent Memory, an Event, Audit, or model inference.

## 13. Relationship

A Relationship is an Assertion connecting Resources or concepts within a defined scope.

Examples include location, part-of, representation by an external record, a Capability target, or a user label referring to a Resource.

A Relationship asserted by one Domain or source is not automatically globally valid. Its direction and meaning must be clear; generic untyped links should be avoided.

## 14. Provenance

Provenance describes where information came from and, when relevant, how it was transformed.

It supports trust assessment, correction, freshness, Conflict analysis, explanation, human control, and safe Context use.

Sources may include the Human Owner, another authorised participant, external systems, Domain components, Collaborators, deterministic transformations, models, and Knowledge sources.

The required detail is proportional to consequence, ambiguity, sensitivity, and correction need.

## 15. Authority

Authority identifies which source may define, confirm, or update a subject, property, or decision within a scope.

Authority is never universal by default. The Human Owner may be authoritative for current intent; an external platform may be authoritative for its reported device state; a source document may be authoritative for its published content; a model is not authoritative because it is fluent.

Authority over information is separate from permission to execute an action. Frequency, recency, or model confidence alone does not create authority.

## 16. Temporal validity

Temporal Validity describes when an Observation, Assertion, or Relationship applies.

Relevant distinctions may include observed time, reported time, retrieval time, valid-from, valid-until, supersession, and staleness. Only distinctions needed by the scenario are represented.

Current state is a conclusion based on sufficiently authoritative and fresh information. It is not a timeless property of an Observation.

Historical retention belongs to Memory, Knowledge, Audit, or the source system according to purpose. The World Model does not require all history.

## 17. Uncertainty

Uncertainty arises from ambiguous references, incomplete evidence, stale Observations, conflicting sources, inference, unavailable sources, imprecise language, Domain translation, or lossy summarisation.

Use the simplest representation sufficient for the scenario. Numerical probabilities are not required and false precision is avoided.

Material uncertainty may trigger clarification, refresh, narrower interpretation, qualification, human confirmation, or refusal of consequential action.

## 18. Conflict

Conflict exists when Assertions overlap in subject, scope, and validity but cannot all be accepted.

Conflict handling considers provenance, scoped authority, temporal validity, information nature, user correction, and explicit unresolved status.

Silent last-write-wins is prohibited at the conceptual level. Unresolved Conflict remains visible where it affects Context or action.

## 19. World View

A World View is a bounded projection of World Model semantics for a Domain, Collaborator, interaction, or purpose.

- **Domain View:** Resources, Assertions, Relationships, authority, time, and uncertainty relevant to a Domain.
- **Collaborator View:** only the world information needed for a bounded mission.
- **Context View:** selected world information used in temporary Context.

A World View is not an independent source of truth and preserves traceable origin.

## 20. Semantic responsibility boundaries

> **World Model defines meaning. Context defines current relevance. Memory defines retention. Knowledge defines reusable understanding. Audit preserves evidence.**

A Domain View describes what is represented for a Domain. Domain Context describes what is currently relevant for a bounded Domain activity.

## 21. Proposal boundary

Context consumption does not mutate world information.

```text
Authoritative or external source
              ↓
World Model semantics
              ↓
Bounded World View
              ↓
Context
              ↓
Collaborator interpretation or proposal
```

A return path is explicit:

```text
Collaborator output
        ↓
Proposal
        ↓
Validation, authority check, or human confirmation
        ↓
Possible accepted Assertion
```

A proposed Assertion or Relationship becomes accepted only through the appropriate source, Domain responsibility, deterministic validation, or human authority.

## 22. Relationship with Context

World Model defines shared meaning; Context selects a bounded view for a purpose, audience, and lifetime.

Context may include selected Resource References, authoritative or provisional Assertions, recent Observations, Relationships, Conflict, and uncertainty. It may also contain temporary interaction information that does not enter world representation.

Selection does not increase authority, remove material uncertainty, turn inference into fact, expose unnecessary information, or copy the entire World Model.

## 23. Relationship with Memory

World Model defines semantic meaning. Memory defines intentional retention, continuity, correction, and forgetting.

Memory may retain selected world information, but representation does not authorise persistence. This document does not decide what is retained, for how long, in which layer, or with what forgetting rules.

## 24. Relationship with Knowledge and Audit

Knowledge supplies reusable understanding or grounding. World Model may reference its Assertions and provenance without absorbing the full source.

Audit preserves evidence of consequential decisions and actions. World Model information may be referenced by Audit but is not itself the Audit record.

## 25. Relationship with Capability

World Model describes Resources and source-scoped information. Capability describes what may be requested or performed.

World information may identify target Resource, state, authority, uncertainty, Relationships, and freshness. It does not grant execution authority. Policy, Approval, execution binding, and Audit remain separate.

## 26. Collaborators and Domains

Collaborators may consume bounded World Views, request Observations, produce proposals, and identify uncertainty or Conflict. They do not silently rewrite authority, promote inference to fact, expand access, create persistent Memory, or treat representation as permission.

Domains define relevant Resource types, accepted sources, scoped authority, Relationships, freshness, and translation from external representations. Domain-specific concepts enter general semantics only when cross-Domain evidence shows value.

## 27. External systems

External systems may remain authoritative for selected Resources and properties. GAIA may reference identifiers, retrieve Observations, map records, expose selected information through Context, and request action through Capabilities.

GAIA does not assume imported information is current, an external taxonomy is universal, copied state becomes GAIA-owned truth, access implies permission, or an external Event model becomes GAIA's Event model.

## 28. Home Assistant boundary

For the first Home Domain, Home Assistant may provide authoritative Observations for selected home Resources.

- Home Assistant identifiers are external Resource References, not universal GAIA identities.
- Home Assistant state remains source-scoped.
- Entity categories do not define future Resource types.
- GAIA interpretation remains distinct from source observation.
- availability and freshness remain visible.
- Capability and Approval stay outside World Model semantics.

The final responsibility split belongs in `ADR-0004-HomeAssistant-Boundary.md`.

## 29. AI model boundary

Models may help resolve references, extract candidate Assertions, summarise sources, identify possible Relationships, propose interpretations, and surface uncertainty.

Model output remains inference or proposal unless validated by authority, deterministic transformation, or human confirmation. A model's internal representation is not the GAIA World Model.

## 30. Human correction

The Human Owner should be able to inspect significant Assertions and provenance, distinguish source reports from inference, correct user-related information, reject proposed Relationships, resolve ambiguous references, challenge authority, refresh stale information, and understand unresolved Conflict.

Correction distinguishes reinterpretation, preference change, scoped override, and actual modification of an external Resource.

## 31. Scoped source of truth

GAIA uses scoped sources of truth rather than one universal source.

For material information, GAIA should be able to identify source, authority for the property, observation time, validity, Conflict, and user correction or override.

The repository remains Source of Truth for GAIA project documentation. Operational authority is separate.

## 32. Minimal semantic checklist

| Question | Purpose |
|---|---|
| What does this concern? | Identify Resource or Relationship. |
| What is claimed or observed? | State semantic content. |
| Who supplied it? | Preserve provenance. |
| What kind of information is it? | Observation, stated, derived, inferred, proposed, or corrected Assertion. |
| Who is authoritative? | Establish scoped authority. |
| When does it apply? | Preserve temporal meaning. |
| What uncertainty exists? | Avoid false certainty. |
| What conflicts? | Avoid hidden inconsistency. |
| Which Domain owns semantics? | Preserve boundaries. |
| Who may use it? | Support bounded Context selection. |

This is not an implementation schema.

## 33. First-Domain validation

The first Home Domain should demonstrate:

- a small Resource set;
- external Home Assistant references;
- user-facing labels distinct from source identifiers;
- recent source-grounded Observations;
- one meaningful Relationship;
- one ambiguous reference;
- one stale or unavailable observation;
- distinction between source authority and GAIA inference;
- a bounded World View supplied to Context;
- no automatic retention.

It should not build a general knowledge graph, whole-home digital twin, state history replica, universal taxonomy, cross-Domain ontology, probabilistic truth engine, Event sourcing, or self-expanding model.

## 34. Example: window status

For “Are any upstairs windows open?”, the model may require resolving Resource References, using location Relationships, retrieving recent authoritative Observations, checking freshness, exposing ambiguity, selecting a bounded Context View, and distinguishing confirmed from unavailable or stale information.

This example does not prescribe code, schema, database, or query mechanism.

## 35. Failures

Relevant failures include unresolved identity, missing authority, stale Observation, conflicting Assertion, unknown provenance, unavailable source, unsupported Relationship semantics, excessive data, and unqualified inference.

Bounded responses include clarification, refresh, explicit uncertainty, reduced scope, human confirmation, refusal of consequential action, safe fallback, or preservation of unresolved status.

## 36. Risks and guardrails

| Risk | Guardrail |
|---|---|
| Universal ontology | Model only validated needs. |
| External taxonomy capture | Treat external identifiers and types as source-scoped. |
| Database-driven semantics | Keep storage out of this document. |
| World Model as Memory | Retention requires Memory semantics. |
| World Model as Shared Context | Supply bounded views. |
| Inference as truth | Preserve nature and provenance. |
| Hidden staleness | Represent time and validity where material. |
| Silent conflict resolution | Preserve Conflict and authority. |
| Identity collapse | Surface ambiguity. |
| Domain leakage | Generalise only with cross-Domain evidence. |
| Source duplication | Keep authority explicit. |
| Premature graph platform | Defer graph and ontology choices. |

## 37. Deferred decisions

Deferred decisions include first-class promotion, implementation as service/library/store/contracts, Core ownership, identifier format, taxonomy, persistence, graph versus relational representation, ontology language, Event sourcing, synchronisation, consistency, history retention, conflict algorithms, confidence scoring, inference models, caching, replication, Home Assistant boundary, Memory architecture, update permissions, and Audit requirements.

## 38. ADR implications

- **ADR-0001:** World Model contract ownership, Resource identity coordination, source registration, and World View selection.
- **ADR-0003:** Resource targeting without representation granting authority.
- **ADR-0002:** retention and correction of world information.
- **ADR-0004:** Home Assistant authority, mapping, freshness, and ownership.
- **ADR-0007:** whether changes in world information require Events.

## 39. Acceptance criteria

The document may be accepted when World Model remains distinct from Context, Memory, Knowledge, Audit, and execution; Resource References are source-scoped; provenance and authority are explicit; time and staleness are recognised; inference is distinct from authority; Conflict remains visible; human correction is supported; external systems retain scoped authority; first-Domain validation stays small; and no technology decision is implied.

## 40. Final statement

GAIA's World Model is a shared semantic model. It is not a runtime component, copy of the world, central state store, or claim to universal truth.

It provides small, explicit, and correctable meaning for the Resources and claims required by validated responsibilities.

**Represent only what is needed, preserve its origin, and never hide uncertainty.**
