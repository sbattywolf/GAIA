# Context Model

**Project:** GAIA  
**Document type:** Foundation Document  
**Status:** Proposed  
**Version:** 0.2  
**Supersedes:** `CONTEXT_MODEL.md`  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document defines the conceptual Context Model for GAIA. It establishes a common vocabulary and boundaries for information temporarily or selectively made available to GAIA, its Collaborators, and Domains while handling an interaction or task.

It prevents Context, conversation history, persistent Memory, Knowledge, World Model information, Audit, execution state, configuration, model context windows, caches, and implementation state from collapsing into one unbounded container.

It defines semantics, not storage, serialisation, transport, retrieval, indexing, prompting, or framework use.

## 2. Authority and classification

This is a Proposed Foundation Document. It refines the existing `Shared Context` concept without automatically changing the official first-class concepts in `GAIA_MODEL.md`.

The concepts here are semantic constructs, not automatically:

- first-class elements of `GAIA_MODEL.md`;
- runtime components;
- services;
- persisted entities;
- independent implementation abstractions.

Primary Context scopes:

1. Request Context;
2. Interaction Context;
3. Shared Context.

Bounded views:

1. Collaborator Context;
2. Domain Context.

Promotion into the official conceptual model requires explicit review and, where material, an ADR.

## 3. Scope

This document covers:

- the meaning and purpose of Context;
- Context scopes and bounded views;
- stewardship, visibility, and write authority;
- lifetime and invalidation;
- provenance and scoped authority;
- propagation across Collaborators and Domains;
- relationships with World Model, Memory, Knowledge, Audit, Capability, and execution;
- conceptual safety and governance.

It excludes database schemas, object models, APIs, prompt templates, token strategies, retrieval algorithms, vector stores, event buses, cache technology, distributed consistency, framework abstractions, and programming languages.

## 4. Definition

**Context is a bounded, purpose-specific view of information made available to support interpretation, coordination, or action within a defined scope and semantic lifetime.**

Context is characterised by:

- purpose;
- scope;
- steward;
- intended audience;
- source and provenance;
- authority;
- visibility and modification rules;
- lifetime;
- invalidation or clearing condition.

Context is not defined by where it is stored.

## 5. Design goals

The model should allow GAIA to:

1. expose relevant rather than all available information;
2. preserve authority and responsibility boundaries;
3. coordinate without hidden global state;
4. distinguish temporary relevance from retention;
5. distinguish interpretation from authoritative information;
6. explain important provenance;
7. invalidate or clear Context predictably;
8. remain independent of models, channels, frameworks, and storage;
9. remain inspectable by the Human Owner;
10. evolve from simple scenarios without becoming a state platform.

## 6. Non-goals

Context does not:

- remember everything;
- define Memory architecture;
- replace the World Model or Knowledge;
- own authoritative external state;
- record every action for Audit;
- define workflow or execution state;
- act as a message bus;
- expose everything to every Collaborator;
- grant permission;
- guarantee distributed consistency.

## 7. Core principles

- **Scoped:** Context belongs to an explicit scope.
- **Purpose-bound:** each item supports a stated responsibility or coordination need.
- **Not authority by default:** presence does not make information true, current, or complete.
- **Not permission:** access does not grant Capability execution.
- **Not Memory:** Context is a working view; Memory concerns intentional retention.
- **Not Audit:** Context supports current work; Audit preserves evidence.
- **Inspectable:** significant Context influencing consequential behaviour should be understandable.
- **Clearable:** temporary Context has an end or invalidation condition.
- **Least sharing:** information stays in the narrowest useful scope.
- **Provenance-aware:** origin is retained when it affects trust or interpretation.

## 8. Request Context

### Definition

Information required to interpret and handle one bounded request, trigger, or intent.

### Typical content

- originating request or trigger;
- requesting identity;
- channel signal;
- explicit parameters and constraints;
- relevant Resource References;
- time or location references;
- proposed Capability request;
- immediate interpretation and uncertainty.

### Steward

The request-handling responsibility. Stewardship means integrity and lifecycle responsibility, not unrestricted authority.

### Visibility

Only the minimum participants required for the request.

### Write authority

The handler may add interpretation but preserves the distinction between user statements, external observations, deterministic derivation, and model inference.

### Lifetime

Until terminal outcome, cancellation, expiry, abandonment, or supersession.

### Boundary

Request Context does not automatically become Memory, Domain Context, or Shared Context.

## 9. Interaction Context

### Definition

Information needed to preserve continuity across related exchanges. The concept is channel-neutral and not equivalent to a chat thread.

### Typical content

- active intent and unresolved questions;
- relevant user corrections;
- selected Resources;
- interaction decisions;
- pending proposals or approvals;
- response expectations and constraints;
- links to active Request Context.

### Steward

The responsibility managing interaction continuity. Whether this belongs inside the Core remains an ADR question.

### Visibility

Only participating responsibilities, and only when needed.

### Lifetime

Longer than one request but semantically temporary. It ends when the interaction completes, expires, is cleared, abandoned, or replaced.

### Boundary

Raw messages may be a source, but Interaction Context is the bounded interpretation needed for continuity, not conversation history itself.

## 10. Shared Context

### Definition

A deliberately selected subset of Context made available across more than one Collaborator or Domain for a bounded coordination purpose.

### Admission rules

Information enters Shared Context only when:

- multiple bounded responsibilities require it;
- the coordination purpose is explicit;
- provenance and authority are known where material;
- visibility is appropriate;
- lifetime and invalidation are defined;
- sharing does not bypass Domain, Capability, Policy, or Approval boundaries.

### Steward

Every shared item has a named steward responsible for purpose, provenance, visibility, validity, update rules, and removal.

### Visibility

Explicitly permitted consumers. There is no implicit GAIA-wide Shared Context.

### Write authority

A single steward normally controls accepted updates. Other participants may propose changes. Multiple writers require explicit conflict semantics.

### Lifetime

The shortest semantic lifetime satisfying the coordination purpose.

### Boundary

Shared Context is not global mutable state, Memory, Audit, Event bus, Registry, cache, or permission bypass.

## 11. Collaborator Context view

Collaborator Context is the bounded view of Context available to one Collaborator for its current responsibility.

It may contain the delegated objective, allowed Context subset, relevant Domain information, Resources, available Capability definitions, constraints, assumptions, intermediate results, and escalation needs.

It is private by default. Selected output crosses the boundary only through explicit hand-off or sharing. It does not become private persistent Memory automatically.

## 12. Domain Context view

Domain Context is the bounded view of currently relevant Context within a Domain responsibility.

It may contain active Domain conditions, relevant terminology, Resource References, Domain constraints, known authoritative sources, objectives, and selected world information.

It does not become a second World Model, Domain knowledge repository, or uncontrolled mirror of an external platform.

## 13. Context item semantics

A Context item should be understandable through these conceptual properties when relevant:

| Property | Meaning |
|---|---|
| Purpose | Why it is needed. |
| Scope | Where and for whom it applies. |
| Subject | Resource, objective, condition, or concept concerned. |
| Value or assertion | Information provided. |
| Origin | Source of the information. |
| Nature | User statement, observation, authoritative assertion, inference, proposal, or derived summary. |
| Authority | Source entitled to define or update it. |
| Confidence | Degree of uncertainty when inferred. |
| Observed at | Relevant observation time. |
| Validity | Conditions or period of applicability. |
| Steward | Lifecycle responsibility. |
| Visibility | Permitted consumers. |
| Mutability | Who may correct or invalidate it. |
| Invalidation | What makes it unsuitable for further use. |

This is a checklist, not an implementation schema.

## 14. Information nature

- **User Statement:** authoritative for current intent or explicit preference within scope, not necessarily external fact.
- **External Observation:** reported or measured by an external source, with source and freshness.
- **Authoritative Assertion:** supplied by a source authoritative for a scoped subject.
- **Derived Information:** deterministic transformation or summary with traceable origin when material.
- **Inference:** model, rule, heuristic, or Collaborator conclusion that is not authoritative by default.
- **Proposal:** suggested interpretation, decision, Relationship, or action not yet accepted.
- **Conflict:** incompatible claims overlapping in subject, scope, and validity.

Conflict is surfaced or resolved through authority and confirmation, not hidden last-write-wins behaviour.

## 15. Lifecycle

1. **Created:** introduced for a defined purpose and scope.
2. **Qualified:** origin, nature, authority, visibility, and validity identified as needed.
3. **Used:** supports interpretation, coordination, or proposal.
4. **Updated or superseded:** newer information replaces or narrows previous Context.
5. **Invalidated:** no longer suitable for reliance.
6. **Cleared:** removed from active scope.
7. **Optionally promoted:** proposed for Memory, Knowledge, World Model acceptance, or Audit through the rules of that concern.

Promotion is an explicit boundary crossing, not automatic retention.

## 16. Semantic lifetime and operational persistence

Temporary is a semantic lifetime, not a storage mechanism.

Context may be persisted operationally to survive interruption, restart, channel change, or an Approval wait without becoming persistent Memory. Operational persistence remains bound to the original purpose, scope, visibility, and invalidation conditions.

Persistence for continuity does not authorise long-term retention or reuse outside the original purpose.

## 17. Propagation and hand-off

Context is not propagated unless another responsibility needs it. The receiver gets the smallest meaningful subset.

Propagation preserves:

- origin;
- nature;
- authority;
- validity;
- restrictions;
- uncertainty;
- intended purpose.

Propagation does not increase authority or permission.

A hand-off identifies objective, relevant Context, unresolved uncertainty, constraints, expected output, and retained authority. Its implementation remains undecided.

## 18. Selection

Context selection considers relevance, scope, authority, freshness, sensitivity, user intent, Collaborator responsibility, Domain boundaries, omission risk, and excessive-disclosure risk.

Selection may use deterministic logic, a model, a Collaborator, or a combination. Consequential behaviour must not rely solely on opaque model selection where omission creates unacceptable risk.

## 19. Human control

The Human Owner should be able to:

- inspect important Context influencing consequential behaviour;
- identify material provenance;
- distinguish fact from inference;
- correct user-related Context;
- clear temporary Context;
- deny promotion into Memory;
- understand why more Context is requested;
- restrict sharing;
- stop work based on incorrect or excessive Context.

## 20. Context and Capability

Context describes information available for interpretation or coordination. Capability describes what may be requested or performed.

Context may identify relevant Capability, Resource scope, constraints, clarification needs, or proposal conditions. It does not grant authority, bypass Policy, replace Approval, conceal targets, or turn model instructions into permission.

## 21. Semantic responsibility boundaries

> **World Model defines meaning. Context defines current relevance. Memory defines retention. Knowledge defines reusable understanding. Audit preserves evidence.**

A **Domain View** describes what the World Model represents for a Domain. A **Domain Context** selects what is currently relevant for a bounded Domain activity.

Context consumption does not mutate the World Model. A Collaborator may propose an Assertion or Relationship, but only an appropriate source, Domain responsibility, deterministic validation, or human confirmation may accept it as world information.

## 22. Context and World Model

World Model represents relevant Resources and scoped information about them. Context selects a bounded view for a purpose, audience, and lifetime.

Context may contain selected Resources, Assertions, Observations, Relationships, unresolved Conflict, and uncertainty. It may also contain temporary interaction information that should not enter world representation.

Selection must not remove material uncertainty, increase authority, turn inference into fact, expose unnecessary data, or copy the full World Model.

## 23. Context and Memory

Context is purpose-specific, bounded, normally temporary, and clearable. Memory is intentionally retained, supports continuity, and is subject to correction and forgetting.

Context may be proposed for Memory only when retention has clear benefit, the category may be remembered, provenance is sufficient, user control is present, correction and forgetting are possible, and boundaries are preserved.

## 24. Context, Knowledge, and Audit

Knowledge is reusable understanding beyond a temporary Context. Retrieval into Context does not transfer ownership from the Knowledge source.

Audit preserves evidence of significant decisions, actions, approvals, denials, failures, and changes. Context may influence an auditable decision but is not itself the Audit record.

## 25. Context and execution

Context is not undefined execution state. Started, waiting, awaiting Approval, completed, failed, cancelled, retryable, or compensated belong to a future execution model.

Context may reference execution status, but lifecycle control does not belong in Shared Context.

## 26. Channels and models

Channels carry messages, identity signals, references, attachments, and delivery constraints. Their signals are translated into channel-neutral meaning before they become GAIA dependencies.

A model context window is an implementation mechanism, not this Context Model. Not all Context is exposed to a model. Model output remains inference unless validated. Prompts do not enforce access control and provider session state does not own GAIA continuity.

## 27. External sources

When external information enters Context:

- the source remains identifiable;
- relevant time and freshness remain visible;
- Context does not become the new source of truth;
- unavailable or stale information is explicit;
- summaries do not replace authoritative records without a decision.

## 28. Failure and degraded behaviour

Failures include missing, stale, conflicting, excessive, or ambiguous Context; unavailable authority; unknown provenance; denied visibility; failed propagation; and unverifiable inference.

Bounded responses include clarification, refresh, narrower scope, visible uncertainty, Approval, refusal, limited interpretation, or invalidation. Silent material assumption is not the default.

## 29. Conceptual matrix

| Context | Purpose | Steward | Default visibility | Semantic lifetime | Memory by default |
|---|---|---|---|---|---|
| Request Context | Handle one request | Request responsibility | Minimum participants | Until outcome or expiry | No |
| Interaction Context | Preserve exchange continuity | Interaction responsibility | Participants as needed | Until closure or expiry | No |
| Collaborator Context view | Expose a responsibility-specific subset | Collaborator | Private by default | Until delegated work ends | No |
| Domain Context view | Expose current Domain relevance | Domain responsibility | Within Domain by default | Explicit Domain validity | No |
| Shared Context | Coordinate selected responsibilities | Named steward | Explicit consumers | Shortest useful lifetime | No |

## 30. First prototype

The first prototype should demonstrate one Request Context, Interaction Context only if needed, one Collaborator view, one Domain view, Shared Context only when multiple responsibilities demonstrably require it, clear source distinction, Context clearing, and no automatic Memory promotion.

It should not build a generic Context service, universal graph, distributed state, automatic retention, provider-owned continuity, or shared blackboard.

## 31. Risks and guardrails

| Risk | Guardrail |
|---|---|
| Global Context | Explicit scope and steward. |
| Shared blackboard | Shared Context is exceptional and purpose-bound. |
| Context-Memory collapse | Explicit promotion semantics. |
| Context-World Model collapse | Separate meaning from relevance. |
| Channel-owned Context | Channel-neutral interpretation. |
| Model-owned Context | GAIA-owned semantics. |
| Implicit authority | Preserve nature, source, and validity. |
| Context as permission | Keep Capability and Policy separate. |
| Multiple uncontrolled writers | Prefer one steward and explicit proposals. |
| Indefinite lifetime | End and invalidation conditions. |
| Over-modeling | Implement only validated distinctions. |

## 32. Deferred decisions

Deferred decisions include representation, Core ownership, dedicated service, Event production, Run ownership, serialisation, model-input selection, machine synchronisation, snapshots, Memory retention, full Policy and Approval model, data classification, encryption, and framework choice.

## 33. ADR implications

- **ADR-0001:** decide whether Core owns Context contracts, lifecycle coordination, selection, Shared Context governance, or only a subset.
- **ADR-0003:** preserve separation between Context and execution authority.
- **ADR-0002:** define promotion from temporary Context to Memory.
- **ADR-0005:** define channel-neutral Interaction Context.
- **ADR-0007:** decide whether Context lifecycle changes require Events.

## 34. Acceptance criteria

This document may be accepted when Context is distinct from Memory, Knowledge, World Model, Audit, and execution; scopes and views have unique purpose; Shared Context is non-global; stewardship, visibility, lifetime, and invalidation are clear; channels and models do not own semantics; Context grants no Capability authority; and no technology choice is implied.

## 35. Final statement

GAIA Context is not everything the system knows, remembers, observes, or has discussed. It is the smallest bounded view of information needed for a defined purpose, exposed to the right responsibility, for the right semantic lifetime, with visible provenance and authority.

**Context must remain bounded, purposeful, inspectable, and disposable.**
