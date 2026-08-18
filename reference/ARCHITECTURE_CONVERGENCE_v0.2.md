# Architecture Convergence

**Project:** GAIA  
**Document type:** Foundation Document  
**Status:** Proposed  
**Version:** 0.2  
**Supersedes:** `ARCHITECTURE_CONVERGENCE.md`  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document provides the convergence view of the current GAIA architecture work. It distinguishes established foundations, the current conceptual model, provisional concepts, validation needs, candidate ADRs, deferred ideas, and the sequence required before significant development.

It is a coordination and governance document. It does not replace `GAIA_MODEL.md`, accepted ADRs, Domain documents, validation reports, or preserved Sprint research.

## 2. Architectural authority

The repository is the Source of Truth. The order of authority is:

1. accepted ADRs for explicit architectural decisions;
2. accepted reference documents for identity, principles, vocabulary, and conceptual models;
3. accepted Domain documents for bounded Domain responsibilities;
4. completed validation reports for experimental evidence;
5. Sprint documents for research, critique, alternatives, and unresolved questions;
6. Idea Incubator and Parking Lot for immature or deferred ideas;
7. conversations as working context only.

Research and diagrams may challenge the current model but do not change it automatically.

This document remains Proposed as a Foundation Document. References below to accepted rules refer to underlying accepted ADRs or established semantic decisions, not to acceptance of this document itself.

## 3. Convergence principles

All convergence work follows these constraints:

- **Human First:** the human owner remains the final authority for important decisions and actions.
- **Simplicity First:** prefer the smallest model that explains a validated problem.
- **Evolvability:** technologies and components should remain replaceable where practical.
- **Modularity:** responsibilities and boundaries must be explicit.
- **Lightweight Core:** the Core coordinates essential contracts and coherence but does not absorb Domain logic by default.
- **Specialised Collaborators:** each Collaborator has a clear mission and bounded responsibility.
- **Capability as Contract:** a Capability describes what may be requested or performed, not how it is implemented.
- **Abstract Resources:** hardware, models, APIs, services, devices, and sources do not define GAIA's identity.
- **Layered Memory:** conversation, Context, preferences, Knowledge, history, and Audit are distinct concerns.
- **Explicit Boundaries:** every Collaborator and integration operates under stated authority and responsibility.
- **Evidence Before Generalisation:** prototypes reduce uncertainty rather than validate assumptions by construction.
- **No Premature Abstraction:** an abstraction is introduced only after a concrete problem demonstrates its value.

## 4. Current phase

GAIA is in **Architecture Convergence**.

The objectives are:

1. consolidate existing documentation;
2. resolve meaningful inconsistency and redundancy;
3. preserve research history without making it normative accidentally;
4. establish a coherent conceptual model;
5. define Context and World Model semantics;
6. sequence remaining foundational ADRs;
7. prepare a small evidence-oriented start to development.

## 5. Established identity

The following statements are stable:

- GAIA is a local-first Personal AI Operating System.
- GAIA is a personal ecosystem of specialised digital Collaborators.
- GAIA is not a chatbot and is not a framework-first project.
- GAIA is not defined by a model provider, runtime, channel, integration, or UI.
- GAIA exists to reduce cognitive load and support sustainable human augmentation.
- Important decisions and sensitive or irreversible actions remain under human control.
- GAIA must remain understandable and maintainable by a very small team.
- Growth must be incremental and preserve conceptual coherence.
- Home automation may validate the first Domain but must not define the whole system.

## 6. Current official conceptual model

The official model remains limited to:

1. **Identity:** what GAIA is and what must remain true.
2. **Core:** the minimal internal coordination boundary preserving coherence and essential contracts.
3. **Collaborator:** a bounded digital role with a specific responsibility.
4. **Domain:** a coherent area of responsibility.
5. **Capability:** an explicit semantic contract describing what may be requested or performed.
6. **Resource:** an identifiable subject of observation, reference, reasoning, access, or action within a Domain.
7. **Shared Context:** deliberately selected Context shared for a bounded coordination purpose.

No new Foundation Document promotes additional concepts into this official list automatically.

## 7. Accepted boundary rules

- Identity is independent of implementation.
- The Core must not absorb every shared concern.
- Collaborators have bounded responsibilities.
- Domains remain independently understandable.
- Capabilities are explicit and do not prescribe implementation.
- Resources have identifiable scope.
- Shared Context is controlled and non-global.
- Domain logic does not enter the Core by default.
- Channels do not own GAIA's conceptual state.
- External systems do not silently become the architectural centre of gravity.
- Model output is not an enforceable security boundary.
- Important actions remain inspectable and governable.

## 8. Established working convergence clarifications

### 8.1 World Model is a shared semantic model

The World Model defines how GAIA describes Resources and source-scoped information about the world. It is not a runtime component, service, database, graph, or central state store. It is not currently a first-class element of `GAIA_MODEL.md`.

Components adhere to its semantics when they represent or exchange world information. They do not require a single World Model implementation and do not need the complete model.

### 8.2 Context uses three primary scopes and two bounded views

Primary semantic scopes:

- Request Context;
- Interaction Context;
- Shared Context.

Bounded views:

- Collaborator Context;
- Domain Context.

The bounded views are not mandatory independent containers, services, stores, classes, or processes.

### 8.3 Observation is source-grounded Assertion

Observation is a source-grounded kind of Assertion. The distinction remains semantically useful, but the initial implementation need not represent them as separate entity types.

### 8.4 Context does not mutate world information automatically

Collaborators may propose Assertions or Relationships. They become accepted world information only through the appropriate source, Domain responsibility, deterministic validation, or human confirmation.

### 8.5 Concern boundaries

> **World Model defines meaning. Context defines current relevance. Memory defines retention. Knowledge defines reusable understanding. Audit preserves evidence.**

The same underlying information may participate in several concerns without making those concerns identical.

## 9. Provisional concepts

| Concept | Status | Reason |
|---|---|---|
| World Model | Proposed semantic foundation, not first-class | Defines shared semantics without implying a component or store. |
| Memory | Partially established | Role, ownership, layers, authority, and retention remain unresolved. |
| Planner | Partially established | An explicit planner has not been validated. |
| Policy | Partially established | Necessary conceptually, but location and relationship with Core and Capability remain open. |
| Approval | Partially established | Required in principle, but semantics and lifecycle are undefined. |
| Audit | Partially established | Inspectability is required, but evidence boundaries are unresolved. |
| Boundary | Partially established | Used as a design concern, not yet a model element. |
| Adapter | Partially established | Useful pattern; required contracts are not yet known. |
| Tool | Partially established | Execution mechanism that must not be conflated with Capability. |
| Workflow | Partially established | May help selected tasks, but is not universal. |
| Registry | Partially established | Its necessity and scope have not been validated. |
| Runtime | Partially established | Operationally necessary but subordinate to GAIA contracts. |
| Model | Partially established | Replaceable computational Resource, not GAIA identity. |
| Event | Proposed | Semantics, durability, ordering, and visibility are unresolved. |
| Run | Proposed | May support observability and recovery, but is unvalidated. |

## 10. Architectural tensions

### 10.1 Lightweight Core versus necessary coherence

A Core that is too small scatters coordination, policy, state, and failure handling. A Core that is too large becomes a proprietary framework. The project must define the minimum stable responsibilities, not a minimum module count.

### 10.2 Orchestration versus direct coordination

GAIA may eventually require orchestration across Collaborators, tools, approvals, channels, and long-running work. It is not yet proven that the first scenarios require a general planner, workflow engine, graph runtime, or event bus.

### 10.3 Memory as support versus centre of gravity

Persistent personal continuity may become principal value. Premature centralisation risks collapsing identity, retrieval, Context, Knowledge, history, and personal data into one subsystem. Memory requires validation.

### 10.4 Capability versus governance

Capability expresses what may be requested or performed. Resource scope, Policy, Approval, execution binding, and Audit evidence remain separate responsibilities even if an early implementation keeps them physically close.

### 10.5 Shared Context versus hidden shared state

Shared Context is useful but may become a global mutable blackboard. It must have explicit purpose, scope, steward, visibility, lifetime, and invalidation.

### 10.6 Home Assistant boundary

Home Assistant provides entities, state, events, automation, and integrations. GAIA must preserve explicit authority and avoid allowing it to become the Core, World Model, or universal event system.

### 10.7 Channel boundary

Telegram can be an initial channel, but its sessions, threads, and notifications must not define GAIA interaction semantics.

### 10.8 Local-first meaning

Local-first is established, but privacy, resilience, ownership, recoverability, offline value, cost, and cloud replaceability require operational validation.

## 11. Reconciliation items

### 11.1 Memory as Domain example

`GLOSSARY.md` must stop presenting Memory as an established Domain. Memory's role remains subject to validation.

### 11.2 Policy semantics in Core definition

`GAIA_MODEL.md` refers to the Core preserving policy semantics. This remains open for `ADR-0001-Core-Boundary.md`; it must not be silently normalised.

### 11.3 Resource boundary

Resource should be refined as an identifiable subject with sufficient identity and boundary for reasoning about state, relationships, and permitted use. A Resource Reference identifies a Resource within a source, Domain, or interaction and is not the Resource itself.

### 11.4 Domain View and Domain Context

A Domain View describes what is represented about the world for a Domain. Domain Context describes what is currently relevant for a bounded Domain activity.

### 11.5 Terminology for responsibility

- **Human Owner:** the person who owns GAIA and retains final authority.
- **Steward:** responsibility for information or Context lifecycle.
- **Authoritative Source:** source entitled to define a scoped property.
- **Domain Responsibility:** boundary responsible for Domain semantics.

### 11.6 Semantic lifetime versus storage

Temporary is a semantic lifetime, not an in-memory guarantee. Context may be persisted operationally for continuity without becoming long-term Memory.

## 12. ADR sequence

| Priority | ADR | Decision | Dependency |
|---|---|---|---|
| Accepted | ADR-0001 Core Boundary | Accepted baseline: minimum stable Core responsibilities and explicit exclusions. | Context and World Model semantics. |
| Accepted | ADR-0003 Capability Model | Accepted baseline: separation of Capability, Resource scope, Policy, Approval, execution, and Audit. | Core boundary and Resource semantics. |
| 3 | ADR-0002 Memory Semantics | Role and ownership of persistent continuity. | Memory validation and World Model boundary. |
| 4 | ADR-0004 Home Assistant Boundary | Responsibility and authority split. | Core and Capability decisions. |
| 5 | ADR-0005 Communication State | Channel-neutral interaction-state ownership. | Context Model and first Domain. |
| 6 | ADR-0006 Tool Trust | Tool isolation and execution authority. | Capability and Approval. |
| 7 | ADR-0007 Event Semantics | Whether Event is required as a first-class concept. | Prototype evidence and Audit needs. |

Numbering preserves the existing candidate set. Priority determines decision order.

## 13. Validation before decision

Evidence is required before deciding:

- whether Memory is a service, layered concern, Domain responsibility, or central subsystem;
- whether explicit orchestration is needed;
- whether a Registry is justified;
- whether Run materially improves Audit, recovery, or user understanding;
- whether durable Events are required;
- whether Telegram can remain replaceable;
- whether Home Assistant can remain authoritative without defining the World Model;
- what local value remains when cloud services are unavailable.

## 14. Parking Lot

Deferred choices include:

- programming language;
- agent or workflow framework;
- database and vector store;
- graph or ontology technology;
- event-bus technology;
- MCP as internal standard;
- provider abstraction such as LiteLLM;
- plugin packaging or marketplace;
- distributed deployment;
- multi-user or multi-tenant design;
- general-purpose UI framework;
- production orchestration platform.

## 15. Approved work sequence

1. `ARCHITECTURE_CONVERGENCE_v0.2.md` — proposed convergence register.
2. `CONTEXT_MODEL_v0.2.md` — proposed Context semantics.
3. `WORLD_MODEL_v0.2.md` — proposed shared semantic World Model.
4. Reconcile `GLOSSARY_v0.2.md`, `GAIA_MODEL_v0.2.md`, `NEXT_STEPS_v0.2.md`, and `REPOSITORY_STRUCTURE.md` conservatively.
5. Use accepted `ADR-0001-Core-Boundary.md` as the Core boundary baseline.
6. Use accepted `ADR-0003-Capability-Model_Accepted.md` as the Capability Model baseline.
7. Create `sprint-03/MEMORY_ROLE_VALIDATION.md`.
8. Use evidence before remaining first-Domain ADRs.

## 16. Entry criteria for development

Significant implementation begins only when:

- vocabulary is coherent;
- Context and World Model boundaries are sufficiently coherent and remain explicitly Proposed working semantics;
- Core boundary is accepted or sufficiently bounded;
- Capability contract is accepted or sufficiently bounded;
- ADR-0001 and ADR-0003 are already accepted; implementation readiness still depends on the bounded first scenario;
- the first validation scenario and assumptions are explicit;
- excluded functionality is documented;
- the prototype can be discarded without losing architectural knowledge.

Small experiments remain allowed when uncertainty, evidence target, and disposal expectation are explicit.

## 17. Minimal prototype guardrails

The first prototype must not attempt to deliver:

- complete Memory;
- a general planner;
- a universal event bus;
- a plugin ecosystem;
- multi-Domain orchestration;
- a complete UI;
- abstractions for hypothetical runtimes;
- production distributed infrastructure.

It should test one bounded intent, one Collaborator responsibility, explicit Capabilities, scoped Resources, controlled Context, a replaceable external boundary, visible Approval where required, and an inspectable outcome.

## 18. Risks

| Risk | Guardrail |
|---|---|
| Core expansion | Explicit inclusions and exclusions in ADR-0001. |
| Model inflation | Promote concepts only when durable and ambiguity-reducing. |
| Shared-state coupling | Context scope, stewardship, and invalidation. |
| Memory centralisation | Validate role and preserve layered semantics. |
| Capability overload | Separate contract, governance, execution, and evidence. |
| First-Domain capture | Keep Domain evidence separate from general architecture. |
| Channel capture | Channel-neutral Interaction Context. |
| Framework capture | Reuse at boundaries after validated need. |
| Local-first ambiguity | Test degraded-mode scenarios. |
| Documentation proliferation | Unique responsibility and lifecycle for every document. |

## 19. Document update plan

Immediate reconciliation targets:

- `GLOSSARY_v0.2.md`: Memory/Domain, Resource, Shared Context, and provisional semantic terms.
- `GAIA_MODEL_v0.2.md`: minimal cross-references only; no promotion of World Model or Context views.
- `NEXT_STEPS_v0.2.md`: active phase, produced deliverables, reconciliation, and ADR sequence.
- `REPOSITORY_STRUCTURE_v0.2.md`: new Foundation Documents, candidate ADR label, and document lifecycle.

`IDENTITY.md`, `MANIFESTO.md`, `NORTH_STAR.md`, and `DESIGN_PRINCIPLES.md` remain unchanged unless specific evidence requires revision.

## 20. Exit criteria

Architecture Convergence may conclude when:

- reference documents use consistent terminology;
- Context and World Model semantics are sufficiently coherent for the current working baseline and remain Proposed pending explicit lifecycle acceptance;
- critical inconsistency is corrected or explicitly deferred;
- Core and Capability decisions are recorded or bounded for prototype work;
- Memory has a validation plan;
- first-Domain assumptions remain separate from general architecture;
- the ADR backlog is sequenced;
- the prototype has explicit learning objectives and exclusions;
- no major implementation commitment depends on an undocumented assumption.

## 21. Final statement

Architecture Convergence does not attempt to complete GAIA's architecture in advance. It makes the project harder to misunderstand and establishes the smallest coherent foundation from which evidence-driven development can begin.

**Simplicity is a feature.**
