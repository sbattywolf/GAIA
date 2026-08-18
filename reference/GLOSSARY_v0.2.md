# Glossary

**Project:** GAIA  
**Document type:** Reference Document  
**Status:** Proposed  
**Version:** 0.2  
**Supersedes:** `GLOSSARY.md`  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document defines the official and provisional vocabulary used across the GAIA repository.

A stable vocabulary reduces ambiguity, limits architecture drift, and helps reference documents, ADRs, Domain documents, validation work, experiments, and implementation use the same terms consistently.

The Glossary defines language. It does not decide architecture, select technology, or promote every listed term into the official conceptual model.

## 2. Vocabulary classes

The Glossary contains:

1. **GAIA-native concepts** used to describe GAIA itself;
2. **semantic supporting terms** used by Foundation Documents to clarify existing concepts;
3. **provisional architectural terms** whose role is still under validation;
4. **external ecosystem terms** used in research or implementation discussions.

Only terms explicitly identified as official model concepts are first-class elements of `GAIA_MODEL.md`.

## 3. Status markers

| Marker | Status | Meaning |
|---|---|---|
| ✅ | Established | Accepted vocabulary used consistently in the current reference model. |
| 🟡 | Partially Established | Useful working term whose architectural role or boundary remains incomplete. |
| 🔵 | Proposed | Candidate vocabulary introduced for validation or future decision/decision support. |
| ⚪ | External | Ecosystem term that does not define GAIA's native conceptual model. |

Status indicates vocabulary maturity, not implementation status.

## 4. Usage rules

- Use established terms consistently.
- Use partially established terms with their open boundaries visible.
- Treat proposed terms as candidates, not commitments.
- Do not promote a term because a framework uses it.
- Do not infer a runtime component from a semantic term.
- Prefer GAIA-native `Collaborator` over external `Agent` when discussing GAIA roles.
- Use capitalised terms when referring to defined GAIA concepts; use lower case for generic meanings.

## 5. Official conceptual model terms

These seven terms are the current first-class concepts of `GAIA_MODEL.md`.

| Status | Term | Definition |
|---|---|---|
| ✅ | GAIA | A local-first Personal AI Operating System: a personal ecosystem of specialised digital Collaborators that helps the Human Owner reduce cognitive load, coordinate Context, and act through explicit Capabilities while keeping important decisions under human control. |
| ✅ | Identity | The durable conceptual definition of what GAIA is and what must remain true when implementation choices change. |
| ✅ | Core | The minimal internal coordination boundary that preserves GAIA's coherence and essential contracts. Its responsibilities are defined by accepted `ADR-0001-Core-Boundary.md`. |
| ✅ | Collaborator | A bounded digital role within GAIA with a specific responsibility. A Collaborator is not merely a model call and is not automatically an autonomous Agent, process, prompt, Workflow, Tool, or model instance. |
| ✅ | Domain | A coherent area of responsibility within GAIA, such as home, research, or communication. Domains remain independently understandable. Memory is not currently an established Domain. |
| ✅ | Capability | An explicit semantic contract describing what action, access, or operation may be requested or performed. It does not prescribe implementation. Resource scope, Policy, Approval, execution binding, and Audit remain separate responsibilities. |
| ✅ | Resource | An identifiable subject of observation, reference, reasoning, access, or action within a Domain. A Resource may be physical, digital, external, or conceptual, but requires sufficient identity and boundary for GAIA to reason about its state, Relationships, or permitted use. |
| ✅ | Shared Context | A deliberately selected subset of Context made available across more than one Collaborator or Domain for a bounded coordination purpose. It is not global mutable state, Memory, Audit, Event bus, Registry, or cache. |

## 6. Established principles and roles

| Status | Term | Definition |
|---|---|---|
| ✅ | Human Owner | The person for whom GAIA exists, who owns the system and retains final authority for important outcomes. Use this term instead of the ambiguous generic `owner` when referring to the person. |
| ✅ | Human Control | The principle that important decisions, sensitive actions, and irreversible changes remain visible, governable, and correctable by the Human Owner. |
| ✅ | Local-First | A design preference for local ownership, control, recoverability, and execution whenever practical, with external services explicit and replaceable. Operational meaning requires scenario-based validation. |
| ✅ | Simplicity First | The principle that GAIA introduces only the minimum concepts and complexity justified by validated value. |
| ✅ | Steward | A responsibility accountable for the lifecycle, validity, visibility, and clearing or supersession of Context or information. Stewardship does not imply universal authority or ownership of the referenced Resource. |
| ✅ | Authoritative Source | A source entitled to define, confirm, or update a specific subject or property within a defined scope. Authority is scoped and does not imply permission to execute an action. |
| ✅ | Domain Responsibility | The boundary responsible for Domain semantics, rules, and interpretation. It does not automatically own every Resource referenced by the Domain. |

## 7. Context semantic terms

The following terms refine `Shared Context`. They are semantic scopes or views, not automatically first-class model elements, services, stores, classes, processes, or persisted entities.

| Status | Term | Definition |
|---|---|---|
| 🟡 | Context | A bounded, purpose-specific view of information made available to support interpretation, coordination, or action within a defined scope and semantic lifetime. |
| 🟡 | Request Context | The Context needed to interpret and handle one bounded request, trigger, or intent. |
| 🟡 | Interaction Context | Channel-neutral Context needed to preserve continuity across related exchanges. It is not raw conversation history. |
| ✅ | Shared Context | Context explicitly shared across selected responsibilities for a bounded coordination purpose. |
| 🟡 | Collaborator Context | The bounded view of Context available to one Collaborator for its current responsibility. It is not necessarily an independent container. |
| 🟡 | Domain Context | The bounded view of currently relevant Context within a Domain responsibility. It is not a second World Model or Domain knowledge store. |
| 🟡 | Context Item | A conceptual unit within Context characterised as needed by purpose, scope, subject, origin, information nature, authority, validity, Steward, visibility, and invalidation. It is not a required persisted entity. |
| 🟡 | Hand-off | An explicit transfer of bounded responsibility and the minimum relevant Context between Collaborators or other responsibilities. Its implementation remains undecided. |
| 🟡 | Semantic Lifetime | The period and conditions during which information remains relevant for its original purpose. A temporary semantic lifetime does not prohibit operational persistence for restart or continuity. |

## 8. World Model semantic terms

**World Model is an accepted semantic foundation, not a first-class concept or runtime component.** The terms in this section define shared meaning and do not require separate implementation types.

| Status | Term | Definition |
|---|---|---|
| 🟡 | World Model | GAIA's shared semantic model for relevant Resources and source-scoped Assertions, Observations, Relationships, provenance, authority, time, uncertainty, and Conflict. It is not a service, database, graph, central state store, or claim to universal truth. |
| 🟡 | Resource Reference | A source-, Domain-, or interaction-scoped identifier or reference for a Resource. A Resource Reference is not the Resource itself. |
| 🟡 | Assertion | A claim about a Resource, Relationship, condition, or concept made by an identified source. Its acceptance depends on scope, provenance, authority, validity, and uncertainty. |
| 🟡 | Observation | A source-grounded kind of Assertion describing what a source reported, measured, or returned at a relevant time. Observation and Assertion need not be separate implementation types. |
| 🟡 | Fact | An Assertion that GAIA is justified in treating as authoritative within a defined scope and validity period. Fact is not a separate primitive or universal truth category. |
| 🟡 | Relationship | An Assertion connecting Resources or concepts within a defined scope and meaning. |
| 🟡 | Provenance | Information explaining where an Assertion, Observation, or derived item came from and, when material, how it was transformed. |
| 🟡 | Authority | The scoped entitlement of a source to define, confirm, or update a subject or property. Authority is separate from execution permission. |
| 🟡 | Temporal Validity | The time or conditions under which an Assertion, Observation, or Relationship may be treated as applicable, including relevant freshness or supersession. |
| 🟡 | Uncertainty | The known limit of GAIA's ability to identify, interpret, or rely on information. It should use the simplest representation justified by the scenario. |
| 🟡 | Conflict | A condition in which Assertions overlap in subject, scope, and validity but cannot all be accepted simultaneously. Conflict must not be hidden by implicit last-write-wins behaviour. |
| 🟡 | World View | A bounded projection of World Model semantics for a Domain, Collaborator, interaction, or purpose. It is not an independent source of truth. |
| 🟡 | Domain View | The World View describing what is represented for a Domain. Domain View describes representation; Domain Context describes current relevance. |
| 🟡 | Proposal | An interpretation, Assertion, Relationship, decision, or action suggested by a Collaborator or other source but not yet accepted by the appropriate authority or validation boundary. |

## 9. Cross-concern distinction

The following sentence is normative for vocabulary separation:

> **World Model defines meaning. Context defines current relevance. Memory defines retention. Knowledge defines reusable understanding. Audit preserves evidence.**

The same underlying information may participate in more than one concern without making those concerns identical or requiring duplicated storage.

## 10. Provisional architectural terms

| Status | Term | Definition |
|---|---|---|
| 🟡 | Memory | A structured and intentional way for GAIA to retain, retrieve, correct, and forget information over time. Memory is broader than chat history and is not currently an established Domain or first-class official model element. |
| 🟡 | Knowledge | Reusable understanding or reference material used to support interpretation, grounding, or explanation beyond one temporary Context. Its status as a first-class concept remains undecided. |
| 🟡 | Planner | A possible coordination function that determines how intent, Collaborators, Capabilities, Resources, Policy, and Context combine to handle a task. The need for an explicit Planner is unvalidated. |
| 🟡 | Policy | A rule or decision constraint governing what is allowed, denied, delayed, approved, logged, or escalated. Policy is not a prompt instruction. Its relationship with the Core is unresolved. |
| 🟡 | Approval | An explicit authorisation decision required before a proposed action is executed. Approval is not implicit consent or absence of objection. |
| 🟡 | Audit | Evidence of significant decisions, actions, Tool calls, Approvals, denials, failures, Memory changes, and external interactions. Audit is not generic logging or active Context. |
| 🟡 | Boundary | A conceptual or technical separation between responsibilities, trust zones, Domains, Adapters, Memory layers, or external systems. |
| 🟡 | Adapter | A boundary component connecting GAIA to an external system, channel, runtime, or integration while limiting conceptual and technical coupling. |
| 🟡 | Tool | A callable implementation mechanism, function, service, or operation. A Tool is not a Capability; it may implement or support one. |
| 🟡 | Workflow | A structured sequence or graph of steps used to coordinate tasks, Tools, Collaborators, Approvals, or state transitions. It is not assumed to be GAIA's universal execution model. |
| 🟡 | Registry | A discoverable catalogue of items such as Collaborators, Capabilities, Tools, Adapters, Resources, or runtimes. Its necessity and scope remain unvalidated. |
| 🟡 | Runtime | The environment or service executing model inference, Tool operations, Workflows, or other computation. Runtime choice must remain subordinate to GAIA semantics. |
| 🟡 | Model | An AI model used for reasoning, generation, classification, Tool selection, summarisation, embedding, or other AI functions. A Model is replaceable and does not define a Collaborator or GAIA identity. |
| 🔵 | Event | A recorded occurrence relevant to system behaviour. Event semantics, durability, ordering, and visibility remain unresolved. |
| 🔵 | Run | A possible bounded execution instance from trigger or intent to outcome. Its value for observability, recovery, and Audit remains unvalidated. |

## 11. Capability responsibility separation

The following distinctions are established by accepted `ADR-0003-Capability-Model_Accepted.md`:

| Concern | Question |
|---|---|
| Capability Definition | What may be requested or performed? |
| Resource Scope | On what Resource or Resource class? |
| Policy Decision | Is it allowed under current rules? |
| Approval | Who or what must authorise it? |
| Execution Binding | How is it performed by an implementation mechanism? |
| Audit Evidence | What evidence is preserved? |

A Capability may declare semantic requirements but does not contain the Policy engine, Approval Workflow, Tool binding, or Audit history.

## 12. External ecosystem terms

| Status | Term | Definition |
|---|---|---|
| ⚪ | Agent | External term for an AI system or component that may reason, use Tools, or perform multi-step tasks. Prefer `Collaborator` for GAIA-native roles. |
| ⚪ | Tool Calling | Allowing a model to request predefined Tool use and receive results. |
| ⚪ | Function Calling | Tool Calling where Tools are described as functions or schemas and an application executes them. |
| ⚪ | MCP | Model Context Protocol, an external protocol for connecting AI applications to Tools, data sources, and Workflows. Its adoption is not assumed. |
| ⚪ | RAG | Retrieval-Augmented Generation, where external Knowledge is retrieved and supplied to a model during generation. RAG is not Memory by itself. |
| ⚪ | LLM | Large Language Model used for language processing or generation. It is an implementation Resource, not GAIA identity. |
| ⚪ | Vector Store | Storage optimised for embeddings and similarity retrieval. It is not automatically required by GAIA. |
| ⚪ | Connector | Generic integration component connecting a system to a source, service, API, or Tool. In GAIA architecture discussions, use `Adapter` when the boundary semantics are intended. |
| ⚪ | Plugin | Packaged extension to a host system. GAIA does not currently define a Plugin model. |
| ⚪ | Event Bus | Mechanism for publishing and consuming Events. GAIA does not currently require one. |
| ⚪ | Knowledge Base | Curated or indexed information used for retrieval, reference, or grounding. It does not define GAIA's complete Knowledge semantics. |

## 13. Descriptive notes and open questions

### Core

The Core prevents GAIA from becoming unrelated scripts or framework-specific components. It is not necessarily a Workflow engine, Agent runtime, UI, Memory database, Home Assistant extension, model gateway, Policy engine, or World Model service.

Defined by accepted `ADR-0001-Core-Boundary.md`:

- What minimum responsibilities preserve coherence?
- What must remain outside the Core?
- Does the Core evaluate Policy, enforce a Policy decision, or only require an enforceable decision contract?
- Which Context and World Model contracts, if any, belong to the Core?

### Collaborator

Open questions include Memory access, Capability use, inter-Collaborator coordination, lifecycle, versioning, and escalation. Collaborators must not become mini-platforms or unbounded assistants.

### Domain

Open questions include cross-Domain Capability use, Context sharing, authority, and evolution beyond the Home Domain. The first Domain must not define the general model.

### Capability

Open questions include minimum metadata, Resource scoping, revocation, versioning, Policy, Approval, execution binding, and Audit. Avoid Capability explosion and prompt-based permission.

### Resource

Open questions include identity across sources, Domain-specific types, ambiguous references, authority, and relationships. Weak Resource identity makes authorisation and Audit unreliable.

### Shared Context

Open questions include admission, Steward, visibility, lifetime, invalidation, and conflict. Shared Context must not become global state.

### Memory

Open questions include role, layers, write authority, inspection, correction, export, deletion, prohibited retention, and relationship with World Model, Knowledge, Context, and Audit. These require validation before `ADR-0002`.

## 14. Term promotion rules

A term may become established only when:

- it is used consistently across relevant reference documents;
- it solves durable ambiguity;
- its responsibility is distinct;
- it is not merely an implementation choice;
- it has evidence from research, validation, or accepted ADRs;
- its inclusion reduces rather than increases conceptual complexity.

A semantic supporting term does not need promotion to remain useful.

## 15. Repository alignment

This Glossary is aligned with:

- `GAIA_MODEL_v0.2.md`;
- `ARCHITECTURE_CONVERGENCE_v0.2.md`;
- `CONTEXT_MODEL_v0.2.md`;
- `WORLD_MODEL_v0.2.md`.

Future accepted ADRs may require targeted updates. Terminology changes must preserve previous versions during Architecture Convergence.

## 16. Final statement

The Glossary exists to make GAIA easier to understand, not to maximise the number of concepts.

Use stable words, keep provisional boundaries visible, and do not turn semantic vocabulary into architecture accidentally.
