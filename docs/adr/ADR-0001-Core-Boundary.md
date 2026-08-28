# ADR-0001: Core Boundary

**Project:** GAIA  
**Document type:** Architecture Decision Record  
**Status:** Accepted  
**Version:** 1.0  
**Date:** 2026-08-03  
**Accepted:** 2026-08-03  
**Decision owner:** Human Owner  
**Phase:** Architecture Convergence

## 1. Decision summary

GAIA will begin with a **minimal in-process Core** responsible only for preserving a small set of stable coordination contracts and enforcing the boundaries required by the first domestic production slice.

The Core will:

1. accept a bounded Request;
2. preserve Request and Interaction correlation;
3. select or invoke one appropriate Collaborator through explicit routing;
4. provide that Collaborator with a bounded Context view;
5. resolve requested Capability definitions and their Resource scope;
6. require the applicable Policy and Approval outcome before execution;
7. delegate execution to an Adapter or Tool boundary;
8. return a structured result or explicit failure;
9. emit minimal diagnostic and Audit evidence required by the scenario.

The Core will **not** initially contain Domain logic, a general Planner, persistent Memory, a World Model service, a Registry platform, an Event Bus, a Workflow engine, a Plugin system, model-provider abstraction, or distributed coordination.

This decision favours the shortest safe path to useful domestic production while preserving replaceability and clear boundaries.

## Clarifications

- Persistent agent Memory is outside Core boundary;
- Document/resource retrieval does not make retrieved material part of Core-owned Memory.

## 2. Context

GAIA is a personal, local-first ecosystem of specialised digital Collaborators. It is maintained by one Human Owner for domestic use.

The project needs enough common coordination to prevent the implementation from becoming a collection of unrelated scripts, model calls, channel handlers, and Home Assistant-specific logic.

At the same time, a sophisticated Core would delay useful production behaviour and risk turning GAIA into a custom framework before the project has evidence that such a framework is necessary.

The first expected validation slice is narrow and read-only or low-risk. A representative scenario is answering whether selected windows or doors are open while distinguishing confirmed, stale, unavailable, or ambiguous state.

The Core boundary must therefore solve the immediate coordination problem without pre-building infrastructure for hypothetical future Domains.

## 3. Decision drivers

The decision is guided by:

- **Human First:** consequential behaviour remains visible and governable.
- **Simplicity First:** include only responsibilities required for coherence and the first scenario.
- **Fast domestic value:** prefer direct, robust implementation over months of platform construction.
- **Replaceability:** channels, models, Tools, Adapters, and external systems remain replaceable.
- **Domain separation:** Home Domain behaviour must not become Core behaviour.
- **Explicit Capability boundary:** what may be requested remains separate from how it is executed.
- **Visible failure:** ambiguity, stale information, unavailable sources, and denied actions must not become silent success.
- **Single-owner maintainability:** one person must be able to understand, operate, and change the Core.
- **Evidence-driven evolution:** add coordination machinery only after real scenarios demonstrate need.

## 4. Definitions used by this ADR

### Core

The minimal internal coordination boundary preserving GAIA coherence and essential contracts.

### Coordination contract

A stable conceptual interaction between responsibilities, independent of a specific framework or technology.

### Domain logic

Rules and interpretations meaningful to one Domain, such as deciding which Home Assistant entities represent windows or how home locations are resolved.

### Policy decision

A result stating whether a proposed Capability use is allowed, denied, requires Approval, or cannot be determined.

### Enforcement boundary

The point that prevents execution unless the required Policy and Approval result exists.

## 5. Decision

### 5.1 Core responsibility

The Core owns **coordination and enforcement of required boundaries**, not Domain intelligence and not general infrastructure.

Its initial responsibility is limited to the following conceptual flow:

```text
Request
   ↓
Request validation and correlation
   ↓
Explicit Collaborator selection
   ↓
Bounded Context construction
   ↓
Capability and Resource-scope resolution
   ↓
Policy / Approval requirement check
   ↓
Execution delegation to Adapter or Tool
   ↓
Structured result or explicit failure
   ↓
Minimal diagnostic / Audit evidence
```

This flow describes responsibility, not a required class structure or framework pipeline.

### 5.2 Core responsibilities included now

#### A. Request boundary

The Core accepts a normalised, bounded Request from a channel Adapter or another trusted internal entry point.

It preserves enough identity, origin, correlation, and scope to process the Request safely.

The Core does not own channel-specific message semantics.

#### B. Explicit routing

The Core chooses the responsible Collaborator through simple explicit routing sufficient for the first scenario.

Initial routing may be deterministic configuration or straightforward code. A general Planner is not required.

#### C. Context boundary

The Core coordinates creation of the minimum Request Context and bounded Collaborator Context view needed for the selected responsibility.

It does not expose all available information and does not treat Context as global mutable state.

It may persist Context operationally only when continuity requires it. Operational persistence does not make Context long-term Memory.

#### D. Capability boundary

The Core resolves the requested Capability definition and identifies the intended Resource scope before execution.

The Core does not implement Domain-specific Capability behaviour.

#### E. Policy enforcement boundary

The Core is responsible for ensuring that no Capability execution bypasses a required Policy or Approval result.

For the initial implementation, Policy evaluation may be a small explicit rule or a replaceable function. The Core does not require a general Policy engine.

The Core owns enforcement of the result, not necessarily authorship of all Policy rules.

#### F. Execution delegation

The Core delegates implementation-specific work through an Adapter or Tool boundary.

The Core does not call Home Assistant, Telegram, a model runtime, or another external system through Domain-specific logic embedded inside the Core.

#### G. Result and failure boundary

The Core returns a structured outcome that distinguishes at least:

- success;
- denied;
- clarification required;
- unavailable dependency;
- ambiguous Resource;
- stale or insufficient information;
- execution failure.

The exact representation remains an implementation detail.

#### H. Minimal evidence

The Core preserves only the diagnostic or Audit evidence required to understand important outcomes for the current scenario.

Initial read-only queries may require simple correlation, selected Capability, target Resource references, outcome, and material failure reason.

The Core does not initially implement an enterprise Audit platform or distributed tracing system.

### 5.3 Responsibilities explicitly outside the Core

The following responsibilities remain outside the initial Core:

| Responsibility | Initial location or treatment |
|---|---|
| Home-specific interpretation | Home Domain |
| Home Assistant calls and mapping | Home Assistant Adapter |
| Telegram message formatting and delivery | Telegram Adapter |
| Model invocation details | Model/runtime Adapter |
| Resource taxonomy for Home | Home Domain |
| Persistent Memory | Deferred pending validation |
| Knowledge retrieval | Deferred or bounded external concern |
| World Model storage | Not introduced; World Model remains semantic |
| General planning | Deferred until direct routing proves insufficient |
| Workflow engine | Not required |
| Event Bus | Not required |
| Registry platform | Not required |
| Plugin system | Not required |
| Multi-user / tenancy | Out of scope |
| Distributed coordination | Out of scope |
| General Policy engine | Not required initially |
| General Approval workflow | Not required initially |
| General Audit platform | Not required initially |
| Provider abstraction layer | Deferred until replacement pressure exists |

### 5.4 Initial physical shape

The conceptual decision permits a simple in-process implementation, for example:

```text
application
├── core coordination
├── home Domain
└── adapters
```

This is not a mandated source tree.

The first Core may be a small module with explicit interfaces. It does not need to run as a separate service or process.

### 5.5 Dependency direction

The intended dependency rule is:

```text
Core contracts ← Domain and Adapter implementations
```

The Core may depend on stable abstractions required for coordination. It must not depend directly on Home Assistant entity types, Telegram payloads, model-provider SDK objects, or storage-specific schemas.

Pragmatic exception: the first implementation may use simple language-native data structures rather than a formal abstraction package, provided external representations are translated at the boundary and do not leak through the Core.

## 6. Policy decision explained simply

There are two different jobs:

1. **decide whether an action is allowed**;
2. **make sure the action cannot run without that decision**.

This ADR assigns the second job to the Core.

For the first domestic slice, the first job can remain a small explicit rule. For example, a read-only state query may be allowed without Approval, while a sensitive state-changing action may require explicit Approval.

If Policy becomes complex later, its evaluator can move behind a replaceable boundary without changing the Core's responsibility to enforce the result.

## 7. Alternatives considered

### Alternative A: No Core, direct scripts and integrations

Each channel or Domain directly calls external systems and models.

**Advantages**

- fastest initial coding;
- minimal abstraction.

**Disadvantages**

- duplicated routing, error, authority, and Context behaviour;
- Home Assistant or Telegram may become the actual architecture;
- difficult to add a second Collaborator or channel safely;
- inconsistent execution boundaries.

**Decision:** rejected. A small Core provides necessary coherence.

### Alternative B: Orchestrator-centric Core

The Core contains planning, Workflow graphs, retries, state transitions, Event handling, Tool selection, and multi-step execution.

**Advantages**

- powerful coordination;
- easier support for complex future workflows.

**Disadvantages**

- large up-front cost;
- framework capture risk;
- most capability is unneeded for the first scenario;
- difficult for one person to maintain;
- delays production value.

**Decision:** rejected for the initial architecture. Reconsider only with concrete orchestration pressure.

### Alternative C: Memory-centric Core

Persistent Memory is the central coordination mechanism.

**Advantages**

- continuity and personalisation become central;
- shared information may be easy to access.

**Disadvantages**

- Memory role is unvalidated;
- risks collapsing Context, Knowledge, World Model information, history, and Audit;
- raises privacy and lifecycle complexity before value is demonstrated.

**Decision:** rejected. Memory remains outside the Core pending validation.

### Alternative D: Event-driven microkernel

The Core is a Registry and Event Bus with loosely coupled Plugins.

**Advantages**

- extensibility;
- decoupled components;
- asynchronous evolution.

**Disadvantages**

- requires Event semantics, Registry, Plugin lifecycle, ordering, failure, and observability decisions;
- disproportionate to a single-owner domestic project;
- adds operational and debugging complexity.

**Decision:** rejected for now.

### Alternative E: Minimal coordination and enforcement Core

The Core owns bounded request coordination, explicit routing, Context boundaries, Capability resolution, enforcement, delegation, result semantics, and minimal evidence.

**Advantages**

- enough coherence for the first production slice;
- small, understandable, and testable;
- preserves replaceability;
- does not require general infrastructure;
- can grow only when evidence demands it.

**Disadvantages**

- some early logic may be direct and less general;
- future orchestration may require refactoring;
- explicit configuration may initially be manual.

**Decision:** selected. The disadvantages are acceptable and reversible.

## 8. Consequences

### Positive

- The first prototype can remain small and in-process.
- Domain logic stays outside the Core.
- Home Assistant and Telegram remain bounded integrations.
- The World Model remains semantic rather than a central service.
- Policy enforcement exists without introducing a Policy platform.
- Direct routing can reach production sooner than a general Planner.
- Deterministic boundaries can be tested without testing model internals.
- Future infrastructure must justify itself through evidence.

### Negative

- The first implementation may include explicit mappings and manual configuration.
- Some abstractions may be introduced later rather than designed perfectly now.
- A second Domain may reveal missing coordination contracts.
- Operational persistence and multi-step work may require later decisions.

### Risks

| Risk | Mitigation |
|---|---|
| Core accumulates Domain logic | Keep Domain-specific types and rules behind Domain or Adapter boundaries. |
| Core becomes a framework | Add responsibilities only through demonstrated need and ADR review. |
| Policy enforcement becomes superficial | Test that execution cannot proceed without the required result. |
| Direct routing stops scaling | Introduce Planner only after explicit routing becomes materially inadequate. |
| Error handling becomes inconsistent | Use one small structured outcome contract. |
| Adapters leak external schemas | Translate external data at the boundary. |
| Audit expands excessively | Record only evidence proportional to action risk. |
| Rough implementation becomes permanent | Keep interfaces narrow and record known limitations in the prototype README. |

## 9. Validation plan

The first prototype should validate the decision with one read-only Home scenario.

### Required checks

1. A channel-specific input is translated before entering the Core.
2. The Core routes to one Home Collaborator without a general Planner.
3. The Collaborator receives only the Context required for the request.
4. Home Assistant identifiers remain inside the Home or Adapter boundary.
5. The Capability and target Resource scope are explicit.
6. The execution path cannot bypass the Policy result.
7. Stale, unavailable, or ambiguous state produces an explicit non-success outcome.
8. The response can be rendered by another channel without changing Domain logic.
9. Deterministic Core behaviour has automated tests.
10. The implementation can be replaced without changing GAIA Identity or World Model semantics.

### Evidence that would challenge this ADR

Review or supersede this decision if:

- multiple scenarios require complex multi-step coordination;
- direct routing creates substantial duplicated logic;
- long-running work requires durable execution state;
- multiple components require dynamic discovery;
- asynchronous events are necessary for correctness rather than convenience;
- Policy rules become complex enough to require a dedicated evaluator;
- the Core cannot remain independent of Domain or external-system types.

## 10. Implementation guardrails

The first implementation should prefer:

- a single process;
- explicit dependency injection or simple constructor wiring;
- direct interfaces;
- deterministic routing;
- simple structured records;
- local configuration;
- unit tests for boundary rules;
- integration tests for Adapters;
- no framework unless a concrete need justifies it.

The first implementation should avoid:

- reflection-driven Plugin loading;
- dynamic Registry discovery;
- distributed messaging;
- Event sourcing;
- graph orchestration;
- generic Workflow DSL;
- mandatory vector storage;
- central World Model persistence;
- multi-provider abstraction;
- premature microservices.

## 11. Security and safety implications

This ADR does not define a complete security architecture.

It establishes three minimum safety properties:

1. Context access does not grant execution permission.
2. Capability execution cannot bypass the required Policy and Approval outcome.
3. Ambiguous or insufficient Resource identity must not result in consequential execution.

For the first read-only scenario, these properties may be implemented with simple explicit rules and tests rather than a general security platform.

## 12. Operational implications

The Core may run in the same local process as the first Domain and Adapters.

A separate service boundary is not required.

Operational concerns should remain proportionate:

- clear startup failure;
- explicit dependency-unavailable result;
- basic correlation in logs;
- simple health indication if needed by deployment;
- easy disable or rollback;
- no distributed tracing or high-availability platform without evidence.

## 13. Documentation impact

If accepted, update:

- `GAIA_MODEL_v0.2.md`: replace the open Core responsibility with this accepted boundary;
- `GLOSSARY_v0.2.md`: align the Core and Policy definitions;
- `ARCHITECTURE_CONVERGENCE_v0.2.md`: mark ADR-0001 accepted;
- `NEXT_STEPS_v0.2.md`: mark the first pre-prototype ADR complete;
- future prototype README: list implemented and excluded Core responsibilities.

No changes are required to:

- `IDENTITY.md`;
- `NORTH_STAR.md`;
- `MANIFESTO.md`;
- `WORLD_MODEL_v0.2.md`;
- `CONTEXT_MODEL_v0.2.md`, unless implementation reveals a semantic conflict.

## 14. Relationship with future ADRs

### ADR-0003 Capability Model

Must define the minimum Capability contract, Resource scope, Policy result, Approval requirement, execution binding, and evidence needed by the first scenario.

### ADR-0002 Memory Semantics

Must not move Memory into the Core without validation and explicit supersession or amendment of this ADR.

### ADR-0004 Home Assistant Boundary

May refine Adapter and authority responsibilities after prototype evidence.

### ADR-0005 Communication State

May define operational persistence and channel-neutral Interaction Context when continuity pressure appears.

### ADR-0007 Event Semantics

Must justify Events through correctness or coordination needs. Events are not part of the initial Core by default.

## 15. Decision review triggers

Review this ADR when:

- two production Domains are active, so the boundary can be checked against real cross-Domain experience;
- a second production Domain is added and reveals immediate boundary pressure;
- direct routing becomes materially difficult;
- actions with meaningful physical or financial consequence are introduced;
- persistent multi-step execution is required;
- Policy rules outgrow simple explicit evaluation;
- dynamic component discovery becomes necessary;
- the Core exceeds an understandable coordination role;
- operation becomes difficult for one person.

## 16. Acceptance record

The Human Owner reviewed and accepted this ADR on 2026-08-03, with the explicit expectation that the decision remains revisable and should be reviewed after practical experience with two active Domains.

The following acceptance conditions were confirmed:

- the Core remains smaller than the surrounding Domain and integration logic;
- no Home-specific rule is assigned to the Core;
- Policy enforcement is clear without requiring a Policy platform;
- the first scenario can be implemented without Planner, Registry, Event Bus, Memory, or Plugin system;
- failure outcomes are explicit;
- the Human Owner can understand the full Core responsibility;
- the decision supports faster domestic production without hiding safety or correctness risk.

Future correction will be recorded as an amendment for compatible clarification or as a superseding ADR for a materially different Core boundary.

## 17. Final decision statement

GAIA will start with a small in-process Core that coordinates bounded Requests, explicit Collaborator routing, Context views, Capability and Resource scope, required Policy and Approval results, execution delegation, structured outcomes, and minimal evidence.

Everything not required for this responsibility remains outside the Core until real usage demonstrates otherwise.

**The Core protects coherence. It does not become the product.**
