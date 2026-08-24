# Context Model

**Project:** GAIA  
**Document type:** Foundation Document  
**Status:** Draft  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document defines the conceptual Context Model for GAIA.

Its purpose is to establish a shared vocabulary and clear boundaries for information that is temporarily or selectively made available to GAIA, its Collaborators, and its Domains while handling an interaction or task.

The Context Model exists to prevent different concerns from collapsing into a single unbounded state container. In particular, it distinguishes Context from:

- conversation history;
- persistent Memory;
- knowledge;
- the World Model;
- audit records;
- execution history;
- configuration;
- model context windows;
- caches and implementation state.

This document defines what Context means conceptually. It does not define how Context is stored, serialised, transported, indexed, retrieved, or injected into an AI model.

## 2. Status and Authority

This document is a **Draft Foundation Document** produced during Architecture Convergence.

It refines the `Shared Context` concept already present in the current GAIA conceptual model, but it does not change the official first-class concepts by itself.

Until accepted:

- the existing definition of `Shared Context` in `GAIA_MODEL.md` remains authoritative;
- this document provides the proposed detailed interpretation of that concept;
- conflicts must be resolved explicitly rather than silently normalised.

A future architectural decision may require updates to this document, `GAIA_MODEL.md`, `GLOSSARY.md`, or related ADRs.

## 3. Scope

This document covers:

- the meaning and purpose of Context;
- Context categories;
- Context ownership and scope;
- visibility and write authority;
- lifetime and invalidation;
- provenance and authority;
- propagation across Collaborators and Domains;
- relationships with Memory, knowledge, the World Model, audit, and execution;
- conceptual safety and governance rules.

It intentionally excludes:

- database schemas;
- object models and class hierarchies;
- message formats;
- API contracts;
- prompt templates;
- token-budget strategies;
- retrieval algorithms;
- embedding models;
- vector stores;
- event buses;
- cache technology;
- distributed-consistency mechanisms;
- framework-specific context abstractions;
- programming-language selection.

## 4. Design Goals

The Context Model should allow GAIA to:

1. provide relevant information without exposing all available information;
2. preserve clear responsibility and authority boundaries;
3. coordinate Collaborators without creating hidden global state;
4. distinguish temporary information from persistent Memory;
5. distinguish interpreted information from authoritative facts;
6. explain where contextual information came from;
7. clear, replace, or invalidate Context predictably;
8. avoid coupling conceptual Context to a specific model, channel, framework, or storage technology;
9. remain understandable to the human owner;
10. evolve from simple single-interaction scenarios without requiring a general distributed-state platform.

## 5. Non-Goals

This Context Model is not intended to:

- remember everything;
- define GAIA's Memory architecture;
- become a universal system state store;
- replace the World Model;
- replace a knowledge base;
- represent authoritative external state automatically;
- record every action for audit;
- define workflow or execution state;
- act as a message bus;
- expose all Context to every Collaborator;
- prescribe how much information an AI model receives;
- guarantee consistency across external systems;
- solve distributed state management in advance.

## 6. Definition of Context

**Context is a bounded, purpose-specific view of information made available to support interpretation, coordination, or action within a defined scope and lifetime.**

Context exists because a Collaborator or process rarely needs all information known or accessible to GAIA. It needs a relevant subset selected for a specific purpose.

Context is therefore characterised by:

- a purpose;
- a scope;
- an owner or steward;
- an intended audience;
- a source or provenance;
- an authority level;
- a lifetime;
- rules for visibility and modification;
- an invalidation or clearing condition.

Context is not defined by where it is stored. The same conceptual Context could be represented in memory, a local file, a process, a request envelope, or another implementation mechanism without changing its meaning.

## 7. Core Context Principles

### 7.1 Context Is Scoped

Context must belong to an explicit scope. Information must not become globally visible merely because it may be useful.

### 7.2 Context Is Purpose-Bound

Every Context item must support a stated interaction, responsibility, Domain, or coordination need.

### 7.3 Context Is Not Authority by Default

The presence of information in Context does not make it true, current, complete, or authorised for action.

### 7.4 Context Is Not Permission

Access to Context does not grant permission to invoke a Capability or modify a Resource.

### 7.5 Context Is Not Memory

Context is a working view. Memory concerns intentional retention and continuity over time.

### 7.6 Context Is Not Audit

Context helps current interpretation or coordination. Audit preserves evidence of significant behaviour and decisions.

### 7.7 Context Must Be Inspectable

The human owner should be able to understand important Context that influenced significant behaviour.

### 7.8 Context Must Be Clearable

Temporary Context must have an explicit end condition or invalidation rule.

### 7.9 Shared Context Is Exceptional, Not Default

Information should remain within the narrowest useful scope. Sharing requires a reason.

### 7.10 Context Must Preserve Provenance

When origin affects trust or interpretation, Context must retain enough provenance to identify the source and nature of the information.

## 8. Context Categories

The initial Context Model defines five primary Context categories:

1. Request Context
2. Interaction Context
3. Collaborator Context
4. Domain Context
5. Shared Context

These categories describe conceptual scopes. They do not require five separate services, stores, classes, or processes.

## 9. Request Context

### 9.1 Definition

Request Context is the information required to interpret and handle one bounded request, trigger, or intent.

### 9.2 Purpose

It provides the minimum situational information needed to understand what is being requested and under which immediate conditions.

### 9.3 Typical Contents

Request Context may include:

- the originating request or trigger;
- the requesting identity;
- the originating channel;
- explicit user-provided parameters;
- relevant Resource references;
- applicable time or location references;
- declared constraints;
- correlation with an interaction;
- proposed Capability requests;
- immediate interpretation notes;
- uncertainty requiring clarification.

These are examples, not a required schema.

### 9.4 Scope

One bounded request or trigger.

### 9.5 Owner

The component or coordination responsibility handling the request.

Ownership means responsibility for integrity and lifecycle, not unrestricted authority.

### 9.6 Visibility

Visible only to the minimum set of components or Collaborators required to handle the request.

### 9.7 Write Authority

The request handler may add interpreted or derived information, but must preserve the distinction between:

- user-provided information;
- externally observed information;
- system-derived interpretation;
- model-generated inference.

### 9.8 Lifetime

Normally ends when the request reaches a terminal outcome, is abandoned, expires, or is superseded.

### 9.9 Invalidation

Request Context should be invalidated when:

- the request is cancelled;
- required assumptions become false;
- referenced information is known to be stale;
- the request is replaced;
- its maximum valid lifetime is reached.

### 9.10 Boundary Rule

Request Context must not automatically become persistent Memory, Domain Context, or Shared Context.

## 10. Interaction Context

### 10.1 Definition

Interaction Context is the scoped information needed to preserve continuity across related exchanges between the user and GAIA.

An interaction may be conversational, but the concept is channel-neutral and is not equivalent to a chat thread.

### 10.2 Purpose

It supports coherent follow-up, clarification, correction, and continuation without requiring every exchange to restate all relevant information.

### 10.3 Typical Contents

Interaction Context may include:

- active intent and unresolved questions;
- prior user corrections relevant to the current interaction;
- selected Resource references;
- decisions made within the interaction;
- pending proposals or approvals;
- current response expectations;
- channel-neutral turn references;
- interaction-level constraints;
- links to active Request Contexts.

### 10.4 Scope

One logical interaction, which may span multiple messages or channel events.

A channel thread may help identify an interaction but does not define its semantics.

### 10.5 Owner

The GAIA coordination responsibility managing interaction continuity.

The initial model does not decide whether this responsibility belongs inside or outside the Core.

### 10.6 Visibility

Visible to Collaborators participating in the interaction only when necessary for their responsibility.

### 10.7 Write Authority

Updates may be made by interaction coordination and by explicitly participating Collaborators. Derived content must retain its origin.

### 10.8 Lifetime

Longer than a single request but still temporary. It ends when the interaction is completed, abandoned, expired, explicitly cleared, or replaced by a new interaction scope.

### 10.9 Invalidation

Information should be removed or marked invalid when:

- the user corrects it;
- a newer interaction decision supersedes it;
- an external fact is refreshed;
- the interaction closes;
- continued retention no longer serves the interaction purpose.

### 10.10 Boundary Rule

Interaction Context must not be equated with raw conversation history. Raw messages may be a source, but Context is the bounded working interpretation needed for continuity.

## 11. Collaborator Context

### 11.1 Definition

Collaborator Context is information scoped to the current responsibility of one Collaborator.

### 11.2 Purpose

It allows a Collaborator to perform its mission without receiving unrestricted Context from other Collaborators, Domains, or the user.

### 11.3 Typical Contents

Collaborator Context may include:

- the Collaborator mission relevant to the current work;
- delegated objective;
- allowed Context subset;
- relevant Domain information;
- Resource references;
- Capability contracts available for consideration;
- constraints and boundaries;
- working assumptions;
- produced intermediate results;
- uncertainty and escalation needs.

### 11.4 Scope

One Collaborator responsibility within an interaction, request, or future bounded execution.

### 11.5 Owner

The Collaborator is the steward of its working Context, subject to GAIA-wide boundaries and human authority.

### 11.6 Visibility

Private to the Collaborator by default. Selected outputs may be propagated only through explicit hand-off or sharing rules.

### 11.7 Write Authority

The Collaborator may update its working interpretation and intermediate results. It must not rewrite user input, authoritative facts, policy, or another Collaborator's Context.

### 11.8 Lifetime

Bounded by the delegated responsibility. Context ends when the responsibility is completed, cancelled, expires, or is transferred.

### 11.9 Invalidation

Collaborator Context becomes invalid when:

- the delegated objective changes;
- its source Context is invalidated;
- the Collaborator is replaced or restarted without continuity;
- its assumptions are contradicted;
- the work is completed or cancelled.

### 11.10 Boundary Rule

Collaborator Context must not become private persistent Memory by default. Persistent learning or preference retention requires a separate Memory decision and explicit authority.

## 12. Domain Context

### 12.1 Definition

Domain Context is information relevant to a coherent Domain responsibility and shared within that Domain under explicit rules.

### 12.2 Purpose

It provides Domain-specific situational awareness without exposing Domain details globally or forcing every Collaborator to understand every external system.

### 12.3 Typical Contents

Domain Context may include:

- active Domain conditions;
- relevant Domain terminology;
- Resource references within the Domain;
- Domain-specific constraints;
- known authoritative sources;
- active Domain-level objectives;
- status summaries needed by participating Collaborators;
- links to current observations from external systems.

### 12.4 Scope

One Domain, such as the future Home Domain, within a defined operational or interaction scope.

### 12.5 Owner

The Domain responsibility owns the rules for creating, exposing, updating, and invalidating Domain Context.

Ownership of Domain Context does not imply ownership of every referenced Resource.

### 12.6 Visibility

Visible only within the Domain unless a specific subset is promoted to Shared Context or included in a bounded hand-off.

### 12.7 Write Authority

Only components acting under the Domain responsibility may update Domain Context. External-system data must retain its external source and authority status.

### 12.8 Lifetime

May outlive a single request when Domain continuity requires it, but must still have explicit validity and invalidation rules.

Longer lifetime does not automatically make it Memory.

### 12.9 Invalidation

Domain Context should be refreshed, removed, or marked stale when:

- its authoritative source changes;
- its observation validity expires;
- the Domain scope closes;
- a newer observation supersedes it;
- the Domain can no longer verify the information.

### 12.10 Boundary Rule

Domain Context must not become a second World Model or an uncontrolled mirror of an external platform.

## 13. Shared Context

### 13.1 Definition

Shared Context is a deliberately selected subset of Context made available across more than one Collaborator or Domain for a bounded coordination purpose.

### 13.2 Purpose

It supports cross-boundary coordination without making all Context global.

### 13.3 Admission Rule

Information may enter Shared Context only when:

- more than one bounded responsibility requires it;
- the coordination purpose is explicit;
- the source and authority are known;
- visibility is appropriate;
- lifetime and invalidation are defined;
- sharing does not bypass a Domain, Capability, policy, or approval boundary.

### 13.4 Typical Contents

Shared Context may include:

- a user-approved objective shared by multiple Collaborators;
- a common Resource reference;
- a coordination constraint;
- a cross-Domain status summary;
- an interaction-level decision required by multiple responsibilities;
- the result of an explicit hand-off;
- a shared uncertainty requiring resolution.

### 13.5 Scope

Limited to the named Collaborators, Domains, Requests, or interaction that require the information.

There is no implicit GAIA-wide Shared Context.

### 13.6 Owner

Every Shared Context item requires a steward responsible for:

- purpose;
- provenance;
- visibility;
- validity;
- modification rules;
- removal or invalidation.

The steward is not necessarily the source of the information.

### 13.7 Visibility

Explicit allowlist by responsibility or scope. Global visibility is not the default.

### 13.8 Write Authority

Shared write access should be avoided. One owner should normally control updates, while other participants consume or propose changes.

If multiple writers are necessary, conflict semantics require an explicit architectural decision.

### 13.9 Lifetime

The shortest lifetime that satisfies the coordination purpose.

### 13.10 Invalidation

Shared Context must be removed or marked invalid when:

- the coordination purpose ends;
- the source becomes invalid;
- the steward can no longer establish validity;
- the sharing scope changes;
- the user clears or corrects it;
- a superseding item is accepted.

### 13.11 Boundary Rule

Shared Context must not become:

- global mutable state;
- long-term Memory;
- an audit log;
- an event bus;
- a Registry;
- a cache abstraction;
- a replacement for explicit hand-offs;
- a mechanism for bypassing access controls.

## 14. Context Item Concept

A Context item is the smallest conceptual unit made available within a Context scope.

A Context item should be describable through the following conceptual properties:

| Property | Meaning |
|---|---|
| Purpose | Why the item is needed in this Context. |
| Scope | Where and for whom it is valid. |
| Subject | The Resource, objective, condition, or concept it concerns. |
| Value or assertion | The information being provided. |
| Origin | Where the information came from. |
| Nature | User statement, observation, authoritative fact, inference, proposal, or derived summary. |
| Authority | Which source is entitled to define or update the information. |
| Confidence | The degree of certainty when the item is inferred or uncertain. |
| Observed at | When the source information was observed, if relevant. |
| Validity | Conditions or period under which the item may be treated as current. |
| Steward | Responsibility accountable for lifecycle and sharing. |
| Visibility | Which scopes or responsibilities may access it. |
| Mutability | Who may replace, correct, or invalidate it. |
| Invalidation condition | What makes it no longer suitable for use. |

This table is a conceptual checklist, not an implementation schema. Not every item requires every property to be represented explicitly.

## 15. Information Nature and Trust

Context must preserve the nature of information where it affects interpretation or action.

### 15.1 User Statement

Information explicitly provided by the human owner or another authorised human participant.

A user statement is authoritative for the user's current intent and explicit preferences within its scope, but may not be authoritative for external facts.

### 15.2 External Observation

Information observed from an external Resource or system.

Its validity depends on source authority, observation time, and freshness.

### 15.3 Authoritative Fact

Information supplied by a source recognised as authoritative for that specific subject.

Authority is scoped. A system may be authoritative for device state but not for user intent.

### 15.4 Derived Information

Information deterministically transformed or summarised from identified source material.

Its derivation should remain traceable when important.

### 15.5 Inference

Information proposed by a model, rule, heuristic, or Collaborator when it is not directly established by an authoritative source.

Inference must not be silently promoted to fact.

### 15.6 Proposal

A suggested interpretation, decision, or action that has not yet been accepted.

A proposal must remain distinct from an approved decision or authorised action.

### 15.7 Conflict

Two or more Context items conflict when they make incompatible claims within overlapping scope and validity.

Conflict must be surfaced or resolved through an explicit authority rule. It must not be hidden by arbitrary last-write-wins behaviour at the conceptual level.

## 16. Context Lifecycle

The conceptual lifecycle of Context is:

1. **Created**  
   Information is introduced for a defined purpose and scope.

2. **Qualified**  
   Origin, nature, authority, visibility, and validity are identified as needed.

3. **Used**  
   The information supports interpretation, coordination, or a proposed action.

4. **Updated or superseded**  
   New information replaces or narrows previous Context without erasing provenance when this matters.

5. **Invalidated**  
   The information is marked unsuitable for further reliance.

6. **Cleared**  
   The temporary representation is removed from the active Context scope.

7. **Optionally promoted**  
   Information may be proposed for persistent Memory, knowledge, World Model representation, or audit only through the rules of that target concern.

Promotion is not automatic retention. It is a boundary crossing that requires explicit semantics and authority.

## 17. Context Propagation

Context propagation is the deliberate movement or exposure of selected Context between scopes.

### 17.1 Default Rule

Do not propagate Context unless another responsibility needs it.

### 17.2 Minimum Necessary Context

A receiving Collaborator or Domain should receive the smallest meaningful subset required for its responsibility.

### 17.3 Preserve Meaning

Propagation must preserve:

- origin;
- information nature;
- authority;
- relevant validity;
- restrictions;
- uncertainty;
- intended purpose.

### 17.4 No Authority Escalation

Moving information into a broader scope must not increase its authority.

### 17.5 No Permission Escalation

Receiving Context must not grant additional Capability access.

### 17.6 Explicit Hand-Off

When responsibility transfers between Collaborators, the hand-off should identify:

- the objective being transferred;
- relevant Context;
- unresolved uncertainty;
- constraints;
- expected output;
- retained ownership or final authority.

The implementation form of hand-offs remains undecided.

### 17.7 Cross-Domain Propagation

Cross-Domain Context requires an explicit coordination purpose and must avoid leaking Domain-internal details unnecessarily.

## 18. Context Selection

Context selection is the conceptual act of deciding which available information is relevant to a purpose.

Selection must consider:

- relevance;
- scope;
- authority;
- freshness;
- sensitivity;
- user intent;
- Collaborator responsibility;
- Domain boundaries;
- risk of omission;
- risk of excessive disclosure.

Selection may be performed by deterministic logic, a model, a Collaborator, or a combination. This document does not choose the implementation.

Important or sensitive behaviour must not rely solely on opaque model selection when omission could create unacceptable risk.

## 19. Context and Human Control

The Context Model must support Human First behaviour.

The human owner should be able to:

- inspect important Context influencing a consequential proposal or action;
- identify where significant information came from;
- distinguish fact from inference;
- correct user-related Context;
- clear temporary Context;
- deny promotion into persistent Memory;
- understand why additional Context is requested;
- restrict Context sharing across Collaborators or Domains;
- stop work based on incorrect or excessive Context.

The exact user interface is outside this document.

## 20. Context and Capability

Context and Capability are separate concepts.

- Context describes information available for interpretation or coordination.
- Capability describes what action, access, or operation may be requested or performed.

Context may help determine:

- which Capability is relevant;
- which Resource is in scope;
- which constraints apply;
- whether clarification is needed;
- whether a proposal should be presented.

Context must not:

- define executable authority by itself;
- bypass policy evaluation;
- replace approval;
- conceal the target Resource;
- turn a model instruction into permission.

The final separation of Capability, policy, approval, execution binding, and audit belongs in `ADR-0003-Capability-Model.md`.

## 21. Context and Resource

Context may refer to Resources but does not own them automatically.

A Resource reference in Context should preserve enough identity and source information to avoid accidental substitution or ambiguity.

A Context item about a Resource may describe:

- an observed state;
- an intended target;
- a user-provided label;
- a relationship;
- a constraint;
- an uncertainty;
- a proposed action.

The authoritative Resource state may remain in an external system. Context is a view used for a bounded purpose, not necessarily a copy of truth.

## 22. Context and the World Model

The Context Model and World Model have different responsibilities.

### Context Model

Defines bounded, purpose-specific views of information made available to support current interpretation, coordination, or action.

### World Model

Will define how GAIA conceptually represents entities, Resources, observations, assertions, provenance, relationships, authority, temporal validity, and uncertainty about relevant parts of the world.

### Relationship

Context may select information from the World Model for a specific purpose. Context may also contain information that is too temporary, unverified, or interaction-specific to enter the World Model.

Context does not become the World Model, and the World Model must not be copied wholesale into Context.

The detailed World Model is defined separately in `reference/WORLD_MODEL.md`.

## 23. Context and Memory

Context and Memory must remain distinct.

### Context

- purpose-specific;
- bounded in scope;
- normally temporary;
- selected for current work;
- clearable when the purpose ends.

### Memory

- intentionally retained across time;
- designed to support continuity;
- subject to correction and forgetting;
- governed by retention and ownership semantics;
- not assumed to be raw interaction history.

### Promotion Rule

Context may be proposed for Memory only when:

- continued retention has a clear user benefit;
- the information category is allowed to be remembered;
- provenance is sufficient;
- the user has the required visibility or control;
- correction and forgetting are possible;
- retention does not violate a boundary.

The detailed Memory role remains subject to validation and a future ADR.

## 24. Context and Knowledge

Knowledge is information intended to support reusable understanding or reference beyond one temporary Context.

Context may use knowledge, but knowledge is not Context merely because it is retrieved for an interaction.

A retrieved document, rule, or fact may enter Context as a scoped reference while remaining owned by its knowledge source.

Context must preserve:

- the source of retrieved knowledge;
- applicable authority;
- relevant date or version information;
- uncertainty introduced by interpretation or summarisation.

The project has not yet decided whether Knowledge requires its own first-class model element.

## 25. Context and Audit

Context and Audit serve different purposes.

### Context

Supports present interpretation and coordination.

### Audit

Preserves evidence of significant decisions, approvals, denials, actions, failures, and changes.

Context may influence an auditable decision, but the active Context itself is not automatically the audit record.

Where important, an audit record may need to reference:

- which Context items were material;
- their source and nature;
- the decision or action produced;
- human approval or denial;
- uncertainty or conflict known at the time.

The exact audit model remains provisional.

## 26. Context and Execution State

Context must not be used as an undefined substitute for execution state.

Execution state may include concepts such as:

- started;
- waiting;
- awaiting approval;
- completed;
- failed;
- cancelled;
- retryable;
- compensated.

Whether GAIA requires a first-class `Run`, workflow state, task state, or event model remains undecided.

Context may reference execution status when relevant, but lifecycle control belongs to the future execution model rather than Shared Context.

## 27. Context and Channels

Channels carry interaction but must not define GAIA's Context semantics.

Telegram, a web interface, voice, desktop, or another channel may provide:

- messages;
- sender identity signals;
- thread references;
- attachments;
- interaction events;
- delivery constraints.

Channel-specific data may enter Request or Interaction Context, but must be translated into channel-neutral meaning before it becomes a dependency of GAIA behaviour.

Replacing a channel should not require redefining:

- user intent;
- Interaction Context;
- approval semantics;
- Collaborator responsibility;
- Capability contracts;
- Memory semantics.

Detailed communication-state ownership belongs in a future ADR.

## 28. Context and External Systems

External systems may be authoritative for selected Resources or observations.

Examples may include Home Assistant for selected home-automation state or another source for its own records. This document does not assign authority to any system universally.

When external information enters Context:

- the external source must remain identifiable;
- observation time or freshness must be represented when relevant;
- Context must not silently become the new source of truth;
- stale or unavailable external information must be visible;
- derived summaries must not replace authoritative records without an explicit decision.

## 29. Context and AI Models

A model context window is an implementation mechanism, not the GAIA Context Model.

Information may be selected from GAIA Context and supplied to a model, but:

- not all GAIA Context must be exposed to the model;
- model input limits must not redefine conceptual boundaries;
- model output is inference unless validated by another authority;
- prompts do not enforce access control;
- hidden model state must not be treated as durable GAIA Context;
- provider-specific conversation state must not become GAIA's source of interaction continuity.

## 30. Sensitivity and Least Exposure

Context should follow least-exposure principles.

A Context scope should receive only information necessary for its responsibility. Selection should consider:

- personal sensitivity;
- operational sensitivity;
- risk of unintended disclosure;
- external-provider exposure;
- Domain and Collaborator boundaries;
- action risk;
- user expectations.

This document does not define a data-classification scheme. If classification becomes necessary, it should be introduced through a separate policy or security document rather than embedded implicitly in Context.

## 31. Failure and Degraded Behaviour

Context handling must remain explicit under failure.

Relevant failure conditions include:

- missing Context;
- stale Context;
- conflicting Context;
- unavailable authoritative source;
- unknown provenance;
- insufficient visibility permission;
- failed propagation;
- excessive Context;
- ambiguous Resource reference;
- unverifiable model inference.

GAIA should respond by choosing one or more bounded behaviours:

- ask for clarification;
- retrieve or refresh information;
- narrow the requested action;
- expose uncertainty;
- request approval;
- decline to act;
- continue with an explicitly limited interpretation;
- invalidate the affected Context.

Silent assumption is not the default response to material uncertainty.

## 32. Conceptual Context Matrix

| Context type | Primary purpose | Normal owner | Default visibility | Typical lifetime | Persistent by default |
|---|---|---|---|---|---|
| Request Context | Handle one request or trigger | Request-handling responsibility | Minimum participants | Until terminal outcome or expiry | No |
| Interaction Context | Preserve continuity across related exchanges | Interaction coordination | Interaction participants as needed | Until interaction closure or expiry | No |
| Collaborator Context | Support one bounded Collaborator responsibility | The Collaborator as steward | Private to Collaborator by default | Until delegated work ends | No |
| Domain Context | Provide Domain-specific situational awareness | Domain responsibility | Within Domain by default | Explicit Domain validity | No |
| Shared Context | Coordinate selected responsibilities | Named steward | Explicitly allowed consumers | Shortest useful coordination lifetime | No |

The matrix states defaults. Exceptions require an explicit reason and lifecycle rule.

## 33. Minimal Context for the First Prototype

The first prototype should implement only the conceptual minimum needed to validate Context boundaries.

It should demonstrate:

- one Request Context;
- one Interaction Context if follow-up is required;
- one Collaborator Context;
- one Domain Context for the first bounded Domain;
- Shared Context only if at least two responsibilities demonstrably require the same information;
- explicit source distinction between user input, external observation, and inference;
- Context clearing at the end of the scenario;
- no automatic persistence into Memory.

The first prototype should not implement:

- a generic Context service;
- a universal Context graph;
- distributed Shared Context;
- cross-device synchronisation;
- automatic long-term retention;
- model-provider-owned continuity;
- a shared blackboard for arbitrary state;
- framework-specific abstractions for hypothetical future needs.

## 34. Validation Questions

The first prototype and first Domain should help answer:

1. Can a request be handled using only bounded Request and Collaborator Context?
2. When is Interaction Context genuinely required?
3. Does Domain Context reduce coupling to the external system?
4. Is Shared Context necessary, or can explicit hand-offs suffice?
5. Which Context influenced an important proposal or action?
6. Can the user correct or clear relevant Context?
7. Can stale external observations be detected?
8. Can a channel be replaced without changing Context semantics?
9. Can Context remain separate from execution state?
10. Which information, if any, creates a justified need for persistent Memory?

## 35. Architectural Risks

| Risk | Consequence | Guardrail |
|---|---|---|
| Global Context | Hidden coupling and excessive exposure. | Require explicit scope and steward. |
| Shared Context as blackboard | Arbitrary mutable state becomes the integration mechanism. | Shared Context is exceptional and purpose-bound. |
| Context-Memory collapse | Temporary information is retained unintentionally. | Promotion requires separate Memory semantics. |
| Context-World Model collapse | Interaction-specific interpretation becomes perceived truth. | Preserve separate responsibilities and authority. |
| Channel-owned Context | Telegram or another channel defines GAIA continuity. | Translate channel signals into channel-neutral Context. |
| Model-owned Context | Provider session state becomes authoritative. | GAIA owns conceptual Context independently. |
| Implicit authority | Inference or stale observation is treated as fact. | Preserve information nature, source, and validity. |
| Context as permission | Available information grants unintended execution authority. | Capability and policy remain separate. |
| Multiple uncontrolled writers | Conflicts and last-write-wins behaviour become invisible. | Prefer one steward and explicit change proposals. |
| Indefinite lifetime | Context becomes accidental storage. | Every scope requires end or invalidation conditions. |
| Excessive documentation | Context types become theoretical bureaucracy. | Implement only categories demonstrated by real scenarios. |

## 36. Decisions Deferred

This document deliberately does not decide:

- whether Context is implemented as objects, documents, messages, or records;
- whether the Core owns Context storage or only Context contracts;
- whether a dedicated Context service is needed;
- whether Context changes produce Events;
- whether a Run owns Request Context;
- how Context is serialised;
- how Context is selected for model input;
- how Context is synchronised across machines;
- whether context snapshots are required;
- which information is retained as Memory;
- the complete policy and approval model;
- data-classification levels;
- encryption and storage mechanisms;
- framework or protocol choices.

These decisions must be made only when required by validated scenarios.

## 37. ADR Implications

This Context Model informs, but does not replace, future ADRs.

### ADR-0001 Core Boundary

Must decide whether the Core owns:

- Context contracts only;
- Context lifecycle coordination;
- Context selection;
- Shared Context governance;
- none or only a subset of these responsibilities.

### ADR-0003 Capability Model

Must preserve the separation between Context and execution authority.

### ADR-0002 Memory Semantics

Must define the boundary and promotion path between temporary Context and persistent Memory.

### ADR-0005 Communication State

Must define channel-neutral Interaction Context and prevent channels from owning conceptual continuity.

### ADR-0007 Event Semantics

Must decide whether Context lifecycle changes require first-class Events or can remain internal lifecycle operations.

## 38. Required Repository Updates

If this document is accepted, review the following documents for alignment:

### `reference/GAIA_MODEL.md`

- preserve Shared Context as an official concept;
- consider referencing this document for detailed Context semantics;
- do not add the five Context categories as new first-class model elements automatically.

### `reference/GLOSSARY.md`

- align the Shared Context definition;
- distinguish Context, Memory, knowledge, audit, and conversation history;
- add provisional definitions only where they reduce ambiguity.

### `reference/ARCHITECTURE_CONVERGENCE.md`

- mark the Context Model deliverable as produced;
- retain unresolved Core, Memory, Capability, and execution questions.

### `reference/NEXT_STEPS.md`

- record completion of the Context Model draft;
- retain acceptance and validation work as separate steps.

### `reference/WORLD_MODEL.md`

- use the boundary defined here;
- avoid turning the World Model into active interaction Context.

No ADR is required merely to create this draft. An ADR is required if acceptance assigns new architectural responsibility to the Core or changes the official conceptual model materially.

## 39. Acceptance Criteria

This document may be accepted as the initial GAIA Context Model when:

- Context is clearly distinguished from Memory, knowledge, World Model, audit, and execution state;
- every Context category has a unique purpose;
- Shared Context is bounded and non-global;
- ownership, visibility, write authority, lifetime, and invalidation are conceptually defined;
- channel and model implementations do not own Context semantics;
- Context does not grant Capability authority;
- the model remains simple enough for the first prototype;
- no storage, framework, or protocol choice is implied;
- known open decisions are preserved explicitly.

## 40. Review Questions

1. Does each Context category solve a distinct conceptual problem?
2. Can any category be removed without losing necessary clarity?
3. Is Shared Context sufficiently constrained?
4. Is Context clearly separated from persistent Memory?
5. Is Context clearly separated from the World Model?
6. Are facts, observations, inferences, and proposals distinguishable?
7. Does the model preserve Human First control?
8. Does the model prevent channels and AI providers from owning continuity?
9. Does it avoid specifying implementation prematurely?
10. Can a minimal first prototype validate these boundaries without building a Context platform?

## 41. Final Statement

GAIA Context is not everything the system knows, remembers, observes, or has ever discussed.

It is the smallest bounded view of information needed for a defined purpose, exposed to the right responsibility, for the right lifetime, with visible provenance and authority.

A healthy Context Model helps GAIA coordinate without accumulating hidden global state. It enables useful continuity without turning every interaction into permanent Memory. It supports intelligent behaviour without granting inference the status of fact or permission.

**Context must remain bounded, purposeful, inspectable, and disposable.**
