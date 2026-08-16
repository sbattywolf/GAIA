# World Model

**Project:** GAIA  
**Document type:** Foundation Document  
**Status:** Draft  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document defines the initial conceptual World Model for GAIA.

The World Model describes how GAIA represents relevant parts of reality so that Collaborators and Domains can reason about Resources, observations, assertions, relationships, provenance, authority, temporal validity, and uncertainty without depending on a specific external system or storage technology.

Its purpose is to provide a coherent answer to the question:

> What does GAIA need to represent about the world in order to interpret context, support decisions, and act through explicit Capabilities while preserving human control?

This document defines conceptual semantics. It is not a persistence model, ontology, database schema, knowledge graph, event model, digital twin, or implementation blueprint.

## 2. Status and Authority

This document is a **Draft Foundation Document** produced during Architecture Convergence.

It builds on the established concepts in `GAIA_MODEL.md`, especially:

- Domain;
- Resource;
- Capability;
- Collaborator;
- Shared Context.

It also respects the boundaries defined in `CONTEXT_MODEL.md`.

This document does not add `World Model` automatically as a first-class element of the official GAIA conceptual model. Acceptance of this document establishes a foundation for reasoning and future ADRs, but a material change to the official model must be explicit.

Until accepted, `GAIA_MODEL.md` remains authoritative for the official conceptual model.

## 3. Scope

This document covers:

- the purpose and boundary of the World Model;
- Resources and their identities;
- observations and assertions;
- facts and claims;
- provenance and authority;
- relationships;
- temporal validity;
- uncertainty and conflict;
- views across Domains;
- representation of user corrections;
- interaction with Context, Memory, Knowledge, Capabilities, and external systems;
- minimum validation requirements for the first Domain.

It intentionally excludes:

- database schemas;
- graph technology;
- RDF or semantic-web standards;
- ontology languages;
- vector stores and embeddings;
- event sourcing;
- digital-twin platforms;
- synchronisation protocols;
- API contracts;
- class hierarchies;
- identifiers in a particular format;
- conflict-resolution algorithms;
- programming-language choices;
- deployment topology.

## 4. Design Goals

The World Model should allow GAIA to:

1. refer to Resources without being coupled to one external system;
2. distinguish observation from inference;
3. preserve provenance and scoped authority;
4. represent information that changes over time;
5. expose uncertainty and conflicting claims;
6. provide bounded views to Context rather than global state dumps;
7. support human correction;
8. keep Domain-specific semantics within clear boundaries;
9. remain useful if integrations, models, or runtimes are replaced;
10. start small and grow only when validated scenarios require it.

## 5. Non-Goals

The World Model is not intended to:

- represent everything in the user's life;
- create a complete ontology of reality;
- mirror every connected external system;
- become the owner of all state;
- replace authoritative source systems;
- store raw conversation history;
- act as persistent Memory;
- serve as an audit log;
- define workflow or execution state;
- become Shared Context;
- infer truth automatically from model output;
- guarantee globally consistent state;
- predict all future Domains;
- justify a graph database before one is needed.

## 6. Definition

**The World Model is GAIA's conceptual representation of relevant Resources and the scoped claims, observations, relationships, provenance, authority, time, and uncertainty associated with them.**

The World Model is selective. It represents only what GAIA needs for validated responsibilities.

It is also plural in perspective. Different Domains or sources may provide different views of the same Resource. The World Model must preserve those perspectives rather than forcing premature global truth.

## 7. Core Principles

### 7.1 Relevance Before Completeness

GAIA represents only what is needed for a defined responsibility or validated scenario.

### 7.2 Source Before Interpretation

Important information must retain enough provenance to identify its origin.

### 7.3 Authority Is Scoped

A source may be authoritative for one subject or property without being authoritative for the whole Resource.

### 7.4 Observation Is Not Fact by Default

An observation records what a source reported or measured under specific conditions. Whether it should be treated as current truth depends on authority, time, and validity.

### 7.5 Inference Must Remain Visible

A model-generated or rule-derived conclusion must not be silently promoted to authoritative fact.

### 7.6 Time Is Part of Meaning

Many claims are meaningful only with an observation time, validity period, or supersession relation.

### 7.7 Conflict Must Not Be Hidden

Incompatible claims should remain visible until authority, correction, additional evidence, or human judgement resolves them.

### 7.8 External Systems Retain Their Authority

GAIA should not become the source of truth merely because it has copied or interpreted external information.

### 7.9 Context Receives a View

The World Model may supply selected information to a Context scope. It must not be exposed wholesale.

### 7.10 Human Correction Has Priority Within Its Scope

The human owner must be able to correct user-related interpretations and resolve ambiguities, without rewriting evidence from external sources silently.

## 8. Conceptual Building Blocks

The initial World Model uses the following conceptual building blocks:

1. Resource
2. Resource Reference
3. Observation
4. Assertion
5. Relationship
6. Provenance
7. Authority
8. Temporal Validity
9. Uncertainty
10. Conflict
11. World View

These are semantic building blocks within this Foundation Document. They are not automatically new first-class elements of `GAIA_MODEL.md`, nor do they imply individual software components.

## 9. Resource

### 9.1 Definition

A Resource is anything GAIA may observe, reference, reason about, read, modify, or control.

### 9.2 Examples

Depending on the Domain, a Resource may be:

- a physical device;
- a room;
- a document;
- a message;
- a calendar item;
- a person reference;
- a service;
- an external record;
- a user preference;
- a model endpoint;
- a Capability target.

Examples illustrate scope only. Inclusion in this list does not make a Resource type part of the official model.

### 9.3 Resource Boundary

A Resource is not defined by a database row, API object, or external identifier. Those may represent or refer to it.

### 9.4 Resource Ownership

The World Model may describe a Resource without owning it. Ownership, authority, access, and control are separate concerns.

### 9.5 Resource Identity

Resource identity should be stable enough to avoid accidental substitution, but the implementation of identity remains undecided.

## 10. Resource Reference

### 10.1 Definition

A Resource Reference is a scoped way to identify or locate a Resource from a particular source, Domain, or interaction.

### 10.2 Purpose

It allows GAIA to recognise that different systems or users may refer to the same Resource differently.

### 10.3 Reference Types

Conceptually, a reference may include:

- an external-system identifier;
- a Domain-local identifier;
- a human-readable name or label;
- a location-qualified name;
- a relationship-based reference;
- a temporary interaction reference.

### 10.4 Non-Equivalence Rule

Two similar labels do not prove that two references identify the same Resource.

### 10.5 Resolution

Resource resolution is the act of determining which Resource a reference denotes. Ambiguous resolution must remain visible and may require clarification.

The World Model does not define the resolution algorithm.

## 11. Observation

### 11.1 Definition

An Observation is information reported, measured, retrieved, or otherwise obtained from a source at a relevant point in time.

### 11.2 Purpose

Observations preserve evidence about what a source indicated without immediately declaring universal truth.

### 11.3 Conceptual Properties

An Observation may need:

- subject Resource;
- observed property or condition;
- reported value;
- source;
- observation time;
- retrieval time;
- applicable Domain;
- expected freshness;
- confidence or quality indicator;
- known limitations.

This is a conceptual checklist, not a schema.

### 11.4 Observation Boundary

An Observation is not:

- automatically current state;
- necessarily authoritative;
- a persistent Memory;
- a Domain Event;
- an audit record;
- a model inference.

### 11.5 External Observation

When an external system supplies an Observation, the external source and relevant time semantics must remain identifiable.

## 12. Assertion

### 12.1 Definition

An Assertion is a claim about a Resource, relationship, condition, or concept made by an identified source.

### 12.2 Assertion Types

An Assertion may be:

- explicitly stated by the user;
- reported by an external system;
- derived deterministically;
- inferred by a model or heuristic;
- proposed by a Collaborator;
- accepted through human confirmation.

### 12.3 Assertion Boundary

An Assertion records that a source made or supports a claim. It does not guarantee that the claim is true outside its scope.

### 12.4 Fact

Within this model, a Fact is not a separate primitive. It is an Assertion that GAIA is justified in treating as authoritative within a defined scope and validity period.

This avoids creating an unqualified global truth category.

### 12.5 Correction

A correction creates a new authoritative or user-confirmed Assertion and supersedes the incorrect interpretation within its scope. It must not erase the original provenance when history is materially important.

## 13. Relationship

### 13.1 Definition

A Relationship is an Assertion connecting two or more Resources or concepts within a defined scope.

### 13.2 Examples

Relationships may express that:

- a device is located in a room;
- a document concerns a project;
- a Capability targets a Resource type;
- a Resource is represented by an external record;
- one Resource is part of another;
- a user-provided label refers to a Resource.

### 13.3 Boundary Rule

A Relationship must not become globally valid merely because one Domain or source asserts it.

### 13.4 Direction and Meaning

The meaning and direction of a Relationship must be understandable. The World Model should avoid generic links with no defined semantics.

## 14. Provenance

### 14.1 Definition

Provenance describes where information came from and, where relevant, how it was produced or transformed.

### 14.2 Purpose

Provenance supports:

- trust assessment;
- correction;
- freshness evaluation;
- conflict analysis;
- explanation;
- human control;
- safe reuse across Contexts.

### 14.3 Provenance Sources

A source may be:

- the human owner;
- another authorised human participant;
- an external system;
- a Domain component;
- a Collaborator;
- a deterministic transformation;
- an AI model;
- a document or knowledge source.

### 14.4 Transformation Provenance

When information is summarised, mapped, aggregated, or inferred, the resulting claim should preserve the source lineage needed to understand its meaning and reliability.

### 14.5 Minimum Provenance

Not every low-risk item requires complete lineage. The required detail should be proportional to consequence, ambiguity, sensitivity, and correction needs.

## 15. Authority

### 15.1 Definition

Authority identifies which source is entitled to define, confirm, or update a particular subject, property, or decision within a scope.

### 15.2 Scoped Authority

Authority is never assumed to be universal.

Examples:

- the user is authoritative for current intent;
- an external device platform may be authoritative for its reported device state;
- a source document may be authoritative for its own published content;
- a model is not authoritative merely because it produces a fluent answer.

### 15.3 Authority and Access

Authority to state or update information is separate from permission to execute an action.

### 15.4 Authority Conflict

When two sources claim authority over the same subject, the conflict must be surfaced or resolved by an explicit rule or human decision.

### 15.5 No Automatic Promotion

Frequency, recency, or model confidence alone must not promote a source to authoritative status.

## 16. Temporal Validity

### 16.1 Definition

Temporal Validity describes when an Observation, Assertion, or Relationship may be treated as applicable.

### 16.2 Relevant Time Concepts

The model may need to distinguish:

- when something was observed;
- when it was reported;
- when GAIA retrieved it;
- when it became valid;
- when it stopped being valid;
- when it was superseded;
- how quickly it becomes stale.

These distinctions should be represented only when the scenario requires them.

### 16.3 Current State

Current state is a conclusion based on sufficiently authoritative and fresh information. It is not a timeless property of an Observation.

### 16.4 Staleness

Staleness means the available information may no longer be reliable for the intended purpose. Staleness thresholds are Domain- and use-case-specific and are not defined here.

### 16.5 Historical Information

Historical information may remain valuable, but historical retention belongs to Memory, knowledge, audit, or source-system responsibilities depending on purpose. The World Model does not require retaining every prior state.

## 17. Uncertainty

### 17.1 Definition

Uncertainty represents the known limits of GAIA's ability to identify, interpret, or rely on information.

### 17.2 Sources of Uncertainty

Uncertainty may result from:

- ambiguous Resource references;
- incomplete evidence;
- stale Observations;
- conflicting sources;
- model inference;
- unavailable authoritative systems;
- imprecise user language;
- Domain translation;
- lossy summarisation.

### 17.3 Representation

Uncertainty should be represented in the simplest form sufficient for the scenario. The World Model does not prescribe numerical probabilities.

### 17.4 Behaviour

Material uncertainty should lead to a bounded response such as:

- clarification;
- source refresh;
- narrower interpretation;
- visible qualification;
- human confirmation;
- refusal to perform a consequential action.

### 17.5 No False Precision

GAIA should not introduce confidence scores unless they have defined meaning and validated value.

## 18. Conflict

### 18.1 Definition

A Conflict exists when Assertions that overlap in subject, scope, and validity cannot all be accepted simultaneously.

### 18.2 Conflict Handling Principles

Conflicts should be handled through:

1. source and provenance comparison;
2. scoped authority;
3. temporal validity;
4. information nature;
5. user correction or confirmation when appropriate;
6. explicit unresolved status when evidence is insufficient.

### 18.3 Prohibited Default

The conceptual model must not assume silent last-write-wins behaviour.

### 18.4 Conflict Preservation

Unresolved conflict may need to remain represented so that Context selection does not present one claim as settled truth.

## 19. World View

### 19.1 Definition

A World View is a bounded projection of the World Model for a particular Domain, Collaborator, interaction, or purpose.

### 19.2 Purpose

It avoids requiring a single universal representation to serve every responsibility.

### 19.3 Domain View

A Domain View contains the Resources, Assertions, Relationships, authority rules, and temporal semantics relevant to one Domain.

### 19.4 Collaborator View

A Collaborator View exposes only what the Collaborator requires for its bounded mission.

### 19.5 Context View

A Context View selects World Model information for a temporary Context scope.

### 19.6 Boundary Rule

A World View is not an independent source of truth. It remains a projection with traceable origins.

## 20. Relationship with Context

The World Model and Context Model have different responsibilities.

### World Model

Represents relevant Resources and claims about the world, including provenance, authority, time, and uncertainty.

### Context Model

Defines the bounded information view made available for a specific purpose, audience, and lifetime.

### Interaction

Context may include:

- selected Resource References;
- current authoritative Assertions;
- relevant Observations;
- unresolved Conflict;
- uncertainty;
- relationships needed for the active purpose.

### Boundary Rule

Context selection must not:

- remove material uncertainty;
- increase authority;
- turn inference into fact;
- expose more information than required;
- copy the entire World Model into a working scope.

## 21. Relationship with Memory

The World Model and Memory are distinct.

### World Model

Defines the meaning of Resources and claims relevant to GAIA's understanding of reality.

### Memory

Will define intentional retention, continuity, correction, and forgetting across time.

### Interaction

Memory may retain selected Observations, Assertions, Relationships, corrections, or user preferences that support future continuity.

The World Model does not decide:

- what must be retained;
- for how long;
- in which memory layer;
- when forgetting is required;
- whether history is preserved.

### Promotion Rule

Information must not become persistent merely because it is represented in the World Model.

## 22. Relationship with Knowledge

Knowledge is reusable information used to understand, explain, or ground reasoning.

A knowledge source may provide Assertions about Resources or concepts. The World Model may reference those Assertions and their provenance without absorbing the complete source.

The World Model does not decide whether Knowledge becomes a first-class GAIA concept.

## 23. Relationship with Capabilities

The World Model describes what GAIA understands about Resources. A Capability describes what may be requested or performed.

The World Model may support Capability use by identifying:

- the target Resource;
- relevant state or conditions;
- source authority;
- uncertainty;
- relationships affecting scope;
- whether information is fresh enough for the proposed action.

The World Model does not grant execution authority.

Capability governance, policy, approval, execution binding, and audit remain separate concerns.

## 24. Relationship with Collaborators

Collaborators may:

- consume a bounded World View;
- produce proposed Assertions;
- request fresh Observations;
- identify uncertainty or Conflict;
- propose corrections or actions.

Collaborators must not:

- silently rewrite authoritative Assertions;
- treat model inference as fact;
- expand their World View beyond their responsibility;
- create persistent personal knowledge without the relevant Memory authority;
- use access to the World Model as permission to act.

## 25. Relationship with Domains

Domains organise responsibility and provide bounded semantics.

Each Domain may define:

- relevant Resource types;
- accepted external sources;
- scoped authority rules;
- Domain-specific Relationships;
- freshness expectations;
- translations between external representations and GAIA concepts.

Domain-specific concepts should not enter the general World Model unless they demonstrate cross-Domain value and reduce ambiguity.

The first Home Domain must validate the model without turning home-automation entities into universal GAIA abstractions.

## 26. Relationship with External Systems

External systems may remain authoritative for their own Resources and state.

GAIA may:

- reference their identifiers;
- retrieve Observations;
- map external records to Resource References;
- expose selected information through Context;
- request actions through Capabilities.

GAIA must not assume that:

- an imported record is current;
- one platform's taxonomy is universal;
- copied state becomes GAIA-owned truth;
- integration access implies action permission;
- an external event model should become GAIA's event model.

## 27. Relationship with Home Assistant

For the first Home Domain, Home Assistant may provide observations and authoritative state for selected home Resources.

This document does not decide the final Home Assistant boundary.

The World Model must preserve these constraints:

- Home Assistant identifiers are external Resource References, not universal GAIA identities;
- Home Assistant state remains source-scoped;
- entity categories must not define all future Resource types;
- GAIA interpretations must remain distinguishable from Home Assistant observations;
- external availability and freshness must be visible;
- capability and approval boundaries remain outside the World Model.

The final responsibility split belongs in `ADR-0004-HomeAssistant-Boundary.md`.

## 28. Relationship with AI Models

AI models may help:

- resolve ambiguous references;
- extract candidate Assertions;
- summarise source information;
- identify possible Relationships;
- propose interpretations;
- surface uncertainty.

Model output remains inference or proposal unless validated by an authoritative source, deterministic transformation, or human confirmation.

A model's internal representation is not the GAIA World Model.

## 29. Human Control and Correction

The human owner should be able to:

- inspect important Assertions influencing significant behaviour;
- identify provenance;
- distinguish source reports from GAIA inference;
- correct user-related information;
- reject proposed Relationships;
- resolve ambiguous Resource References;
- challenge claimed authority;
- request refresh of stale information;
- understand unresolved Conflict;
- prevent inappropriate use or retention.

A correction must preserve the difference between:

- correcting GAIA's interpretation;
- changing a user preference;
- overriding an external source for a specific purpose;
- modifying the external Resource itself.

## 30. Source-of-Truth Model

GAIA should use a **scoped source-of-truth model**, not a single universal source of truth.

For each material subject, the model should be able to answer:

- which source reports this information;
- which source is authoritative for this property;
- when the information was observed;
- whether it is still valid for the current purpose;
- whether another source conflicts;
- whether the user has corrected or overridden the interpretation.

The repository remains the Source of Truth for GAIA project documentation. This is distinct from operational sources of truth represented by the World Model.

## 31. Minimal Conceptual Record

A World Model item should be understandable through the following conceptual questions:

| Question | Purpose |
|---|---|
| What does this concern? | Identify the Resource or relationship. |
| What is being claimed or observed? | State the semantic content. |
| Who or what supplied it? | Preserve provenance. |
| What kind of information is it? | Distinguish observation, assertion, inference, proposal, or correction. |
| Who is authoritative? | Establish scoped authority. |
| When was it observed or valid? | Preserve temporal meaning. |
| How certain is it? | Expose relevant uncertainty. |
| What conflicts with it? | Avoid hidden inconsistency. |
| Which Domain owns its semantics? | Preserve boundary and vocabulary. |
| Who may see or use it? | Support bounded Context selection. |

This is a semantic checklist, not an implementation schema.

## 32. Minimal First-Domain World Model

The first Home Domain validation should use the smallest sufficient model.

It should demonstrate:

- a small set of home Resources;
- external references from Home Assistant;
- user-facing labels distinct from external identifiers;
- current Observations with source and time;
- at least one Relationship, such as Resource location;
- one ambiguous reference requiring resolution;
- one stale or unavailable observation;
- one distinction between authoritative external state and GAIA inference;
- a bounded World View supplied to Context;
- no automatic persistence beyond the scenario unless separately justified.

It should not implement:

- a general knowledge graph;
- a whole-home digital twin;
- historical state replication;
- every Home Assistant entity;
- universal Resource taxonomies;
- cross-Domain ontology;
- probabilistic truth scoring;
- event sourcing;
- automatic self-expansion of the model.

## 33. Example Scenario: Window Status

The following conceptual example illustrates the model without prescribing implementation.

A user asks:

> Are any upstairs windows open?

The scenario may require:

1. resolving `upstairs windows` to a set of Resource References;
2. using Domain Relationships that associate windows with locations;
3. retrieving recent Observations from the authoritative home source;
4. checking freshness and availability;
5. excluding or surfacing ambiguous Resources;
6. constructing a bounded Context View;
7. returning an answer that distinguishes confirmed state from unavailable or stale state.

The World Model does not decide how the query, lookup, or response is implemented.

## 34. Example Scenario: Conflicting Location

A user refers to a sensor as being in the kitchen, while the external system labels it as belonging to the living room.

The model should preserve:

- the external-system Relationship;
- the user Assertion;
- their provenance;
- their scopes;
- the Conflict;
- any human-confirmed correction.

It must not silently overwrite one source or hide the inconsistency.

## 35. Failure and Degraded Behaviour

Relevant World Model failure conditions include:

- unresolved Resource identity;
- missing authoritative source;
- stale Observation;
- conflicting Assertions;
- unknown provenance;
- unavailable external system;
- unsupported Relationship semantics;
- excessive or irrelevant data;
- model inference presented without qualification.

GAIA should respond with bounded behaviour such as:

- clarification;
- source refresh;
- explicit uncertainty;
- reduced scope;
- human confirmation;
- refusal of a consequential action;
- use of a known safe fallback;
- preservation of unresolved status.

## 36. Architectural Risks

| Risk | Consequence | Guardrail |
|---|---|---|
| Universal ontology | Large speculative model with high maintenance cost. | Model only validated Domain needs. |
| External taxonomy capture | Home Assistant or another system defines GAIA concepts. | Treat external identifiers and types as source-scoped references. |
| World Model as database design | Conceptual semantics become coupled to storage. | Keep technology and schema out of this document. |
| World Model as Memory | All represented information becomes persistent. | Retention requires separate Memory semantics. |
| World Model as Shared Context | Global state becomes visible everywhere. | Supply bounded World Views through Context. |
| Inference promoted to truth | Fluent model output becomes unsafe authority. | Preserve information nature and provenance. |
| Hidden staleness | Old state is used as current truth. | Represent observation time and validity where material. |
| Silent conflict resolution | Incorrect information appears settled. | Preserve Conflict and use scoped authority. |
| Resource identity collapse | Similar names cause actions on the wrong target. | Make ambiguity visible and require resolution. |
| Domain leakage | First-Domain concepts become universal abstractions. | Keep Domain semantics bounded until cross-Domain evidence exists. |
| Source-of-truth duplication | GAIA becomes responsible for copied external state. | Keep authoritative ownership explicit. |
| Premature graph platform | Infrastructure complexity precedes validated need. | Defer graph and ontology technology. |

## 37. Decisions Deferred

This document deliberately does not decide:

- whether World Model is a first-class official model element;
- whether it is implemented as a service, library, store, or set of contracts;
- whether the Core owns the World Model;
- identifier format;
- Resource taxonomy;
- persistence strategy;
- graph versus relational representation;
- ontology language;
- event sourcing;
- synchronisation and consistency;
- history retention;
- conflict-resolution algorithms;
- confidence scoring;
- inference models;
- caching;
- cross-device replication;
- the final Home Assistant boundary;
- the Memory architecture;
- World Model update permissions;
- audit requirements.

These decisions require validated implementation pressure or an explicit ADR.

## 38. ADR Implications

### ADR-0001 Core Boundary

Must decide whether the Core owns:

- World Model contracts;
- Resource identity coordination;
- source registration;
- World View selection;
- no World Model responsibility beyond integration boundaries.

### ADR-0003 Capability Model

Must define how Capability targets reference Resources without granting authority through representation alone.

### ADR-0002 Memory Semantics

Must define which World Model information may be retained and how correction and forgetting interact with provenance.

### ADR-0004 Home Assistant Boundary

Must define authority, mapping, freshness, and state ownership between GAIA and Home Assistant.

### ADR-0007 Event Semantics

Must decide whether changes in Observations or Assertions require first-class Events.

## 39. Required Repository Updates

If this document is accepted, review these documents for alignment.

### `reference/GAIA_MODEL.md`

- preserve Resource as the official concept;
- reference this document for detailed world-representation semantics if appropriate;
- do not add all World Model building blocks as first-class concepts automatically.

### `reference/GLOSSARY.md`

- align definitions for Resource, Context, Observation, Assertion, provenance, authority, and World Model;
- mark new terms as provisional unless formally accepted.

### `reference/CONTEXT_MODEL.md`

- ensure the World View and Context View boundaries remain consistent;
- preserve Context as bounded and temporary.

### `reference/ARCHITECTURE_CONVERGENCE.md`

- mark the initial World Model draft as produced;
- retain deferred decisions and ADR dependencies.

### `reference/NEXT_STEPS.md`

- record completion of the World Model draft;
- keep acceptance, ADR work, and prototype validation separate.

### Future Home Domain document

- define the initial Resource set, authority sources, Relationships, and freshness needs without expanding the general model prematurely.

No ADR is required merely to create this draft. An ADR is required if acceptance materially changes the official conceptual model or assigns World Model responsibility to the Core.

## 40. Validation Questions

1. Can the first scenario distinguish Resource identity from external identifiers?
2. Can GAIA preserve source and observation time?
3. Can it distinguish Observation, Assertion, inference, and accepted fact?
4. Can conflicting claims remain visible?
5. Can the user correct an interpretation without erasing provenance?
6. Can Context receive a bounded view rather than full global state?
7. Can Home Assistant remain authoritative for selected state without defining the whole model?
8. Can the same Resource support another Domain without adopting Home Assistant semantics?
9. Does the model help prevent action on an ambiguous Resource?
10. Can the prototype validate these semantics without a graph platform?

## 41. Acceptance Criteria

This document may be accepted as the initial World Model when:

- its responsibility is distinct from Context, Memory, Knowledge, Audit, and execution state;
- Resources can have source-scoped references;
- provenance and scoped authority are explicit;
- temporal validity and staleness are recognised;
- inference remains distinct from authoritative information;
- Conflict is not hidden;
- Human First correction is supported conceptually;
- external systems retain explicit authority;
- the first Domain can validate the model with a small Resource set;
- no storage, graph, framework, or protocol decision is implied.

## 42. Review Questions

1. Is the World Model necessary as a separate Foundation Document?
2. Does it clarify Resource semantics without creating a universal ontology?
3. Are Observation and Assertion sufficiently distinct?
4. Is Fact correctly treated as scoped and justified rather than absolute?
5. Are provenance, authority, time, and uncertainty proportionate to GAIA's needs?
6. Is the boundary with Context clear?
7. Is the boundary with Memory clear?
8. Does the model avoid Home Assistant capture?
9. Does it preserve Capability and policy separation?
10. Can a very small team maintain the resulting model?

## 43. Final Statement

GAIA's World Model is not a copy of the world and not a claim to universal truth.

It is a small, explicit, and correctable representation of the Resources and claims that matter for validated responsibilities. It preserves where information came from, who is authoritative, when it applies, and where uncertainty or Conflict remains.

A healthy World Model helps GAIA reason without pretending to know more than it does. It supports useful Context without becoming global state, persistent Memory, or an implementation platform.

**Represent only what is needed, preserve its origin, and never hide uncertainty.**
