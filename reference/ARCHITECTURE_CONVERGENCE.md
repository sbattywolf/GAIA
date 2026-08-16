# Architecture Convergence

**Project:** GAIA  
**Document type:** Foundation Document  
**Status:** Draft  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document provides a single convergence view of the current GAIA architecture work.

Its purpose is to distinguish clearly between:

- what GAIA has already established;
- what belongs to the current conceptual model;
- what remains provisional;
- what requires an Architecture Decision Record (ADR);
- what requires validation before a decision;
- what should remain in the Idea Incubator or Parking Lot.

This document does not define the final architecture. It does not replace the reference documents, Sprint research, or ADRs. It is a temporary coordination artifact for the Architecture Convergence phase.

When this document conflicts with an accepted reference document or ADR, the accepted reference document or ADR prevails.

## 2. Scope

This document covers architectural convergence across:

- project identity;
- conceptual model;
- Core boundary;
- Collaborators and Domains;
- Capabilities and Resources;
- Shared Context;
- World Model;
- Memory;
- Policy, approval, and audit;
- execution and orchestration;
- channels and external systems;
- local-first operation;
- documentation and decision sequencing.

It intentionally excludes:

- programming-language selection;
- framework selection;
- database and storage technology;
- deployment topology;
- protocol selection;
- implementation-level API design;
- source-code structure beyond placeholders;
- production operations.

## 3. Architectural Authority

GAIA uses the following order of authority:

1. Accepted ADRs for explicit architectural decisions.
2. Stable reference documents for identity, principles, vocabulary, and the current model.
3. Domain documents for bounded domain responsibilities.
4. Validation reports for evidence gathered through experiments.
5. Sprint documents for research, critique, alternatives, and unresolved questions.
6. Idea Incubator and Parking Lot for immature or deferred ideas.
7. Conversations as working context only.

Research material may challenge the current model but does not change it automatically.

Diagrams from Sprint 1 and Sprint 2 are treated as historical representations of hypotheses. They are not canonical architecture unless their contents are adopted explicitly through reference-document updates or ADRs.

## 4. Convergence Principles

All convergence work must respect the following constraints:

1. **Human First**  
   The human owner remains the final authority for important decisions and actions.

2. **Simplicity First**  
   Prefer the smallest model that explains the validated problem.

3. **Evolvability**  
   Technologies and components must remain replaceable where practical.

4. **Modularity**  
   Responsibilities and boundaries must be explicit.

5. **Lightweight Core**  
   The Core coordinates essential contracts and coherence but does not absorb domain logic by default.

6. **Specialised Collaborators**  
   Each Collaborator has a clear mission and bounded responsibility.

7. **Capability as Contract**  
   A Capability describes what may be requested or performed, not how it is implemented.

8. **Abstract Resources**  
   Hardware, models, APIs, services, devices, and data sources must not define GAIA's identity.

9. **Layered Memory**  
   Conversation, context, preferences, knowledge, history, and audit are distinct concerns.

10. **Explicit Boundaries**  
    Every Collaborator and integration operates under explicit responsibilities and authority.

11. **Evidence Before Generalisation**  
    Prototypes should reduce uncertainty, not validate assumptions by construction.

12. **No Premature Abstraction**  
    Do not introduce an abstraction until at least one concrete problem demonstrates its value.

## 5. Current Phase

GAIA is in the **Architecture Convergence** phase.

The objectives of this phase are:

1. consolidate the existing documentation;
2. remove or resolve meaningful redundancy;
3. preserve research history without allowing it to become normative accidentally;
4. establish a coherent conceptual model;
5. define the World Model at a conceptual level;
6. identify and sequence foundational ADRs;
7. prepare a minimal, evidence-oriented start to development.

Architecture Convergence is complete only when the project can explain:

- what is already decided;
- what is deliberately undecided;
- which uncertainties block implementation;
- which uncertainties can be resolved by a small prototype;
- which documents are normative;
- which decisions require ADRs.

## 6. Established Project Identity

The following statements are treated as established and stable:

- GAIA is a local-first Personal AI Operating System.
- GAIA is a personal ecosystem of specialised digital Collaborators.
- GAIA is not a chatbot.
- GAIA is not a framework-first project.
- GAIA is not defined by a model provider, runtime, channel, integration, or user interface.
- GAIA exists to reduce cognitive load and support sustainable human augmentation.
- Important decisions and sensitive or irreversible actions remain under human control.
- GAIA must remain understandable and maintainable by a very small team.
- Growth must be incremental and must preserve conceptual coherence.
- The first practical validation domain may be home automation, but that domain must not define the whole system.

Changes to this section represent identity changes and therefore require exceptional scrutiny and coordinated updates to the reference documentation.

## 7. Current Official Conceptual Model

The current official model contains seven first-class concepts.

### 7.1 Identity

Defines what GAIA is, what it is not, and what must remain true as implementation choices change.

### 7.2 Core

The minimal internal coordination boundary responsible for preserving ecosystem coherence and essential conceptual contracts.

The precise Core boundary is not yet decided.

### 7.3 Collaborator

A bounded digital role with a specific responsibility. A Collaborator is not automatically an autonomous agent, process, prompt, workflow, model, or tool.

### 7.4 Domain

A coherent area of responsibility that groups related concerns and helps GAIA grow without universal coupling.

### 7.5 Capability

An explicit semantic contract describing what action, access, or operation may be requested or performed under defined constraints.

A Capability does not prescribe its implementation.

### 7.6 Resource

Anything GAIA may observe, reference, reason about, read, modify, or control.

### 7.7 Shared Context

Scoped contextual information made available across parts of GAIA to support coordination.

Shared Context is not a substitute for Memory, knowledge, audit, event history, registry, cache, or arbitrary shared state.

## 8. Accepted Boundary Rules

The following boundary rules are accepted as current architectural constraints:

- Identity must not be derived from implementation.
- The Core must not absorb every shared concern.
- Collaborators must have bounded responsibilities.
- Domains must remain independently understandable.
- Capabilities must be explicit.
- Resources must have identifiable scope.
- Shared Context must remain controlled and scoped.
- Domain logic must not be placed in the Core by default.
- Channels must not own GAIA's conceptual state.
- External systems must not silently become the architectural centre of gravity.
- Model output must not be treated as an enforceable security boundary.
- Important actions must remain inspectable and governable.

These rules constrain future decisions but do not prescribe a runtime architecture.

## 9. Provisional Architectural Concepts

The following concepts are relevant but are not yet first-class elements of the official model:

| Concept | Current status | Reason it remains provisional |
|---|---|---|
| Memory | Partially established | Its role, ownership, layers, authority, and relationship with the World Model remain unresolved. |
| Planner | Partially established | The need for an explicit planner has not been validated; simple routing may initially be sufficient. |
| Policy | Partially established | Policy is necessary conceptually, but its location and relationship with the Core and Capability are undecided. |
| Approval | Partially established | Human approval is required in principle, but approval semantics and lifecycle are undefined. |
| Audit | Partially established | Inspectability is required, but audit boundaries and required evidence are not defined. |
| Boundary | Partially established | Used consistently as a design concern, but not yet formalised as a model element. |
| Adapter | Partially established | Valuable as a separation pattern, but the required adapter contracts are not yet known. |
| Tool | Partially established | External execution mechanism; it must not be conflated with Capability. |
| Workflow | Partially established | May be useful for some tasks, but is not assumed to be a universal execution model. |
| Registry | Partially established | A catalogue may become useful, but its necessity and scope are not validated. |
| Runtime | Partially established | Required operationally, but must remain subordinate to GAIA contracts. |
| Model | Partially established | A replaceable computational Resource, not the identity of a Collaborator or GAIA. |
| Event | Proposed | Event semantics, durability, ordering, visibility, and value are unresolved. |
| Run | Proposed | A bounded execution concept may support audit and recovery, but has not been validated. |
| World Model | Proposed foundation concept | Required for convergence, but its exact responsibilities and boundaries are not yet documented. |

Provisional concepts must not enter the Core or official model merely because a framework uses them.

## 10. Important Architectural Tensions

### 10.1 Lightweight Core versus Necessary Coherence

A Core that is too small may leave coordination, policy, state, and error handling scattered across adapters. A Core that is too large may become a proprietary framework and absorb every cross-cutting concern.

The project must define the minimum stable responsibilities of the Core, not a minimum number of modules.

### 10.2 Orchestration versus Direct Coordination

Orchestration may become important when multiple Collaborators, tools, approvals, channels, and long-running work interact. It is not yet proven that GAIA requires a general planner, workflow engine, graph runtime, or event bus.

The architecture must preserve a path to richer orchestration without requiring it for the first bounded scenarios.

### 10.3 Memory as Supporting Capability versus Centre of Gravity

Persistent personal continuity may become one of GAIA's principal sources of value. However, treating Memory prematurely as the centre of the system risks coupling identity, retrieval, context, knowledge, history, and personal data into a single subsystem.

Memory requires validation before architectural promotion.

### 10.4 Capability Contract versus Governance

A Capability must express what can be requested or performed. It must not itself become a container for implementation, policy evaluation, approval state, execution binding, and audit history.

These responsibilities must be separated conceptually even if an early implementation keeps them physically close.

### 10.5 Shared Context versus Hidden Shared State

Shared Context is useful for coordination but can become a hidden integration mechanism. Without explicit scope, ownership, lifetime, and write rules, it may create stale data and invisible coupling.

The Context Model must be defined before Shared Context is used as a general solution.

### 10.6 Home Assistant as Boundary versus Platform

Home Assistant is a valuable first-domain system, but it already provides entities, state, events, automation, integrations, and execution. GAIA must decide which responsibilities remain authoritative in Home Assistant and which belong to GAIA.

Home Assistant must not silently become GAIA's Core, World Model, or universal event system.

### 10.7 Telegram as Channel versus Conversation State Owner

Telegram may provide the initial user interaction channel, but message threads, sessions, notifications, and channel-specific behaviour must not define GAIA's conceptual state.

Removing or replacing Telegram should not require redefining GAIA.

### 10.8 Local-First Principle versus Operational Definition

Local-first is established as a project principle, but its operational meaning is not fully specified. Privacy, resilience, ownership, recoverability, offline value, cost, and cloud replaceability may impose different requirements.

The project must validate local-first behaviour through scenarios rather than treating local execution alone as sufficient.

## 11. Documented Inconsistencies Requiring Resolution

### 11.1 Memory Listed as a Domain Example

The Glossary currently uses Memory as an example of a Domain while the conceptual model explicitly leaves the role of Memory unresolved.

**Resolution:** qualify Memory as a possible but unvalidated Domain interpretation, or remove it from normative Domain examples.

**Required document update:** `reference/GLOSSARY.md`  
**ADR required:** No.

### 11.2 Policy Semantics Implicitly Assigned to the Core

The Core definition refers to preserving policy semantics while Policy remains provisional.

**Resolution:** do not alter the Core definition by assumption. Address the relationship between the Core and Policy in the Core Boundary ADR.

**Required document update:** potentially `reference/GAIA_MODEL.md`, after ADR acceptance.  
**ADR required:** Yes, `ADR-0001-Core-Boundary.md`.

### 11.3 Candidate ADR Filenames Presented as Repository Structure

The repository structure lists specific ADR filenames even though the decisions are not accepted.

**Resolution:** label them explicitly as a provisional candidate ADR set.

**Required document update:** `REPOSITORY_STRUCTURE.md`  
**ADR required:** No.

### 11.4 Project Phase Out of Date

The roadmap describes the project broadly as Research and Architecture, while the active phase is Architecture Convergence.

**Resolution:** update the current phase while preserving the existing maturity model.

**Required document update:** `reference/NEXT_STEPS.md`  
**ADR required:** No.

### 11.5 ADR Work Presented Too Broadly in Parallel

The existing roadmap identifies several valid ADR candidates, but addressing them simultaneously would obscure decision dependencies and create unnecessary documentation.

**Resolution:** sequence ADRs according to conceptual dependencies and validation needs.

**Required document update:** `reference/NEXT_STEPS.md`  
**ADR required:** No.

## 12. Decision Classification

### 12.1 Accepted Foundations

- GAIA identity and non-goals.
- Human control as final authority.
- Local-first as a durable principle.
- Specialised, bounded Collaborators.
- Explicit Capability contracts.
- Replaceability of technologies and Resources.
- Separation of stable reference material from research history.
- ADRs as first-class records for architectural decisions.

### 12.2 Foundation Documents Required

- `reference/ARCHITECTURE_CONVERGENCE.md`
- `reference/CONTEXT_MODEL.md`
- `reference/WORLD_MODEL.md`

### 12.3 Domain Documents Required Later

- first Home Domain brief;
- Home Assistant boundary document;
- communication-channel state document;
- first-domain Capability allowlist;
- initial Resource classification;
- sensitive-action approval policy;
- domain validation report.

These documents should follow the foundational convergence work.

### 12.4 Candidate ADRs

| Priority | ADR | Decision required | Dependency |
|---|---|---|---|
| 1 | ADR-0001 Core Boundary | Minimum stable responsibilities inside and outside the Core. | Context Model and initial World Model boundaries. |
| 2 | ADR-0003 Capability Model | Separation of Capability, Resource scope, policy, approval, execution binding, and audit evidence. | Core boundary and conceptual Resource semantics. |
| 3 | ADR-0002 Memory Semantics | Role and ownership of persistent personal continuity. | Memory validation evidence and World Model boundary. |
| 4 | ADR-0004 Home Assistant Boundary | Authority and responsibility split between GAIA and Home Assistant. | Core and Capability decisions. |
| 5 | ADR-0005 Communication State | Channel-neutral conversation and interaction-state ownership. | Context Model and first-domain scenarios. |
| 6 | ADR-0006 Tool Trust | Trust, isolation, and execution authority for tools. | Capability and approval semantics. |
| 7 | ADR-0007 Event Semantics | Whether GAIA requires events as a first-class concept and, if so, their meaning. | Evidence from prototype execution and audit needs. |

The numbering preserves the existing candidate set. Priority determines decision order and does not require renumbering.

### 12.5 Validation Required Before Decision

The following questions need evidence before an ADR can be accepted:

- Is Memory a supporting service, a set of layers, a Domain responsibility, or a central architectural subsystem?
- Is explicit orchestration necessary for the first bounded scenarios?
- Does GAIA need a Registry before multiple implementations of a concept exist?
- Does a first-class Run concept materially improve audit, recovery, or user understanding?
- Does GAIA need durable events, or are explicit request/result records sufficient initially?
- Can Telegram remain a replaceable channel without owning session semantics?
- Can Home Assistant remain authoritative for home state without becoming GAIA's World Model?
- What meaningful behaviour remains available when cloud services are unavailable?

### 12.6 Idea Incubator

The following concepts remain non-committed ideas unless promoted through explicit validation:

- Memory Inspector;
- Capability Simulator;
- Planner Red-Team exercise;
- MCP kill-switch test;
- event chaos testing;
- Research Collaborator;
- Voice Domain;
- auto-generated Domains;
- local runtime scorecard;
- Home Assistant replay sandbox;
- Collaborator version diff;
- boundary-violation detector;
- personal-knowledge provenance viewer;
- long-term Memory review assistant.

### 12.7 Parking Lot

The following decisions are intentionally deferred:

- programming language;
- agent or workflow framework;
- database engine;
- vector store;
- knowledge-graph technology;
- event-bus technology;
- MCP adoption as a standard internal protocol;
- LiteLLM or equivalent provider abstraction;
- plugin packaging and marketplace model;
- distributed deployment;
- multi-user or multi-tenant architecture;
- general-purpose UI framework;
- production orchestration platform.

A deferred item may be promoted only when a validated problem requires it.

## 13. World Model Direction

The World Model will define how GAIA represents what it knows, observes, or believes about relevant parts of the world.

It must be conceptually separate from:

- persistence technology;
- Memory retention;
- Shared Context;
- conversation history;
- audit history;
- model context windows;
- vector retrieval;
- Home Assistant's entity registry;
- a specific knowledge-graph implementation.

The first World Model document should address only:

- entities and Resources;
- identifiers and references;
- observations;
- facts and assertions;
- provenance;
- temporal validity;
- authority and source-of-truth relationships;
- uncertainty and conflicting information at a conceptual level;
- relationships with Domain, Capability, Shared Context, and Memory.

The first version must not select RDF, graph databases, schemas, embeddings, event sourcing, or ontology frameworks.

## 14. Context Model Direction

The Context Model must be defined before the World Model is used operationally.

It should distinguish at least:

- request context;
- interaction or conversation context;
- Collaborator-scoped context;
- Domain-scoped context;
- Shared Context;
- persistent Memory;
- knowledge;
- audit and history.

For every context type it should define conceptually:

- purpose;
- scope;
- owner;
- visibility;
- write authority;
- lifetime;
- clearing or invalidation responsibility;
- relationship to persistent records.

The Context Model must not specify storage or serialisation.

## 15. Approved Work Sequence

### Step 1: Architecture Convergence Inventory

Create and maintain this document as the convergence register.

**Output:** `reference/ARCHITECTURE_CONVERGENCE.md`

### Step 2: Context Model

Define contextual scopes and boundaries before introducing shared state.

**Output:** `reference/CONTEXT_MODEL.md`

### Step 3: World Model

Define conceptual representation of observed and known reality while remaining implementation-neutral.

**Output:** `reference/WORLD_MODEL.md`

### Step 4: Core Boundary Decision

Decide the minimum stable responsibilities of the Core and the responsibilities explicitly excluded from it.

**Output:** `adr/ADR-0001-Core-Boundary.md`

### Step 5: Capability Model Decision

Separate semantic Capability contracts from governance and execution concerns.

**Output:** `adr/ADR-0003-Capability-Model.md`

### Step 6: Memory Role Validation

Collect evidence about Memory's role before accepting an architectural decision.

**Output:** `sprint-03/MEMORY_ROLE_VALIDATION.md`

### Step 7: First-Domain Decisions

Use the foundational documents and validation evidence to decide Home Assistant, communication state, tool trust, and event semantics.

**Outputs:** domain documents and remaining candidate ADRs.

## 16. Entry Criteria for Development

Significant implementation should begin only when:

- the current conceptual vocabulary is coherent;
- Context and World Model boundaries are documented;
- the minimum Core boundary has an accepted ADR;
- the Capability contract has an accepted ADR or a sufficiently bounded provisional contract;
- the first validation scenario is explicit;
- assumptions under test are documented;
- excluded functionality is documented;
- the prototype can be discarded without losing architectural knowledge.

This does not prohibit small experiments. Experiments are permitted when they have an explicit uncertainty, evidence target, and disposal expectation.

## 17. Minimal Prototype Guardrails

The first prototype must not attempt to deliver:

- a complete Memory system;
- a general planner;
- a universal event bus;
- a plugin ecosystem;
- multi-domain orchestration;
- a complete user interface;
- framework abstraction for hypothetical future runtimes;
- production-grade distributed infrastructure.

The prototype should demonstrate only enough behaviour to test:

- a bounded user intent;
- one Collaborator responsibility;
- one or more explicit Capabilities;
- scoped Resources;
- controlled Context;
- a replaceable external boundary;
- visible approval where risk requires it;
- an inspectable outcome or failure.

## 18. Convergence Risks

| Risk | Consequence | Current response |
|---|---|---|
| Core expansion | GAIA becomes a proprietary framework. | Define explicit inclusions and exclusions in ADR-0001. |
| Model inflation | Every implementation concern becomes a first-class concept. | Require durability and ambiguity-reduction tests before model promotion. |
| Shared-state coupling | Domains and Collaborators depend on hidden mutable state. | Define the Context Model first. |
| Memory centralisation by accident | Personal data, knowledge, context, and audit collapse into one store. | Validate Memory role and preserve layered semantics. |
| Capability overload | Contract, permissions, policy, execution, and audit become inseparable. | Decide explicit responsibility separation in ADR-0003. |
| First-domain capture | Home automation assumptions define the whole architecture. | Keep Home Domain evidence separate from the reference model. |
| Channel capture | Telegram semantics define interaction state. | Define channel-neutral context and communication state. |
| Framework capture | External abstractions replace GAIA vocabulary. | Reuse at boundaries and adopt only after validated need. |
| Local-first ambiguity | Local execution is claimed without resilience or ownership evidence. | Define and test degraded-mode scenarios. |
| Documentation proliferation | More files reduce clarity rather than improve it. | Every document must have a unique role and lifecycle. |

## 19. Document Update Plan

### Immediate updates after review of this document

- `reference/GLOSSARY.md`
  - clarify the provisional relationship between Memory and Domain;
  - align term status with the current official model.

- `REPOSITORY_STRUCTURE.md`
  - mark listed ADR filenames as provisional candidates;
  - include this convergence document if it becomes part of the maintained structure.

- `reference/NEXT_STEPS.md`
  - set the active phase to Architecture Convergence;
  - sequence ADR and validation work;
  - preserve the existing maturity model.

### Documents to review but not change automatically

- `reference/GAIA_MODEL.md`
- `reference/IDENTITY.md`
- `reference/MANIFESTO.md`
- `reference/NORTH_STAR.md`
- `reference/DESIGN_PRINCIPLES.md`

Changes to these documents require specific evidence. This convergence document does not authorise their modification by itself.

## 20. Review Questions

Before accepting this document, review the following:

1. Does it preserve GAIA's established identity?
2. Does it distinguish decisions from hypotheses?
3. Does it introduce any implementation choice prematurely?
4. Does every proposed document have a unique responsibility?
5. Are the candidate ADRs sequenced according to dependency?
6. Is any concept being promoted without evidence?
7. Are Context, World Model, Memory, knowledge, and audit sufficiently separated?
8. Does the planned work reduce uncertainty before adding complexity?
9. Can the resulting architecture remain maintainable by a very small team?
10. Would GAIA remain recognisable if the first implementation were replaced?

## 21. Exit Criteria for Architecture Convergence

The phase may conclude when:

- reference documents use consistent terminology;
- the Context Model is documented;
- the initial World Model is documented;
- critical inconsistencies have been resolved or explicitly deferred;
- Core and Capability decisions are recorded or bounded sufficiently for prototype work;
- Memory has a defined validation plan;
- first-domain assumptions are separated from general architecture;
- the ADR backlog is sequenced;
- the next prototype has explicit learning objectives and exclusions;
- no major implementation commitment depends on an undocumented assumption.

## 22. Final Statement

Architecture Convergence is not an attempt to complete GAIA's architecture in advance.

Its purpose is to make the project harder to misunderstand, prevent research hypotheses from becoming accidental decisions, and establish the smallest coherent foundation from which evidence-driven development can begin.

GAIA should become more capable without becoming less understandable, more personal without becoming less governable, and more evolvable without becoming more complex than its value justifies.

**Simplicity is a feature.**
