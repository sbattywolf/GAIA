# Next Steps

**Project:** GAIA  
**Document type:** Project Maturity Roadmap  
**Status:** Proposed  
**Version:** 0.2  
**Supersedes:** `NEXT_STEPS.md`  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document translates the current GAIA state into a practical sequence of deliverables, decisions, validations, and implementation steps.

GAIA is a personal, domestic-use project maintained by one Human Owner with support from AI Collaborators. The roadmap therefore optimises for:

- useful production value early;
- low operational and cognitive cost;
- safe, understandable behaviour;
- small replaceable steps;
- avoidance of speculative infrastructure;
- professional discipline without enterprise-scale ceremony.

The objective is not the most elegant possible architecture. The objective is the simplest robust architecture that can reach useful domestic production quickly without accepting avoidable correctness, safety, or maintainability risks.

## 2. Delivery principle: shortest safe path to value

When two options provide comparable correctness and safety:

- prefer the option that can be implemented and operated sooner;
- prefer a direct implementation over a general platform;
- prefer one concrete integration over premature provider abstraction;
- prefer explicit rules over sophisticated orchestration when rules are sufficient;
- prefer a small local solution over distributed infrastructure;
- prefer manual approval over a complex automated governance engine;
- prefer a replaceable rough edge over months of framework construction.

This principle does not justify known bugs, silent data loss, unsafe actions, hidden authority, or untestable behaviour.

## 3. Current status

GAIA is in **Architecture Convergence**.

Research Foundation is substantially complete. The following proposed v0.2 documents now exist:

- `ARCHITECTURE_CONVERGENCE_v0.2.md`;
- `CONTEXT_MODEL_v0.2.md`;
- `WORLD_MODEL_v0.2.md`;
- `GLOSSARY_v0.2.md`;
- `GAIA_MODEL_v0.2.md`.

The next documentation work is:

1. reconcile `NEXT_STEPS.md` and `REPOSITORY_STRUCTURE_v0.3.md`;
2. review the complete v0.2 reference set;
3. accept or revise the proposed documents;
4. use the accepted ADR baseline and reconcile dependent documentation;
5. validate architecture through a narrow domestic scenario.

No framework, language, database, event bus, graph platform, general Planner, Registry, or Plugin system is committed.

## 4. Established assumptions

- GAIA is personal and single-owner, not multi-tenant.
- GAIA is local-first, with external services explicit and replaceable where practical.
- GAIA is built around bounded digital Collaborators.
- Important and sensitive actions remain under Human Control.
- Home automation is the first validation Domain.
- Home Assistant, Telegram, and a local AI runtime are expected initial boundaries, but do not define GAIA identity.
- Architecture decisions are recorded when they materially constrain implementation.
- Experiments exist to reduce uncertainty and may be discarded.
- The project must remain maintainable by one person.

## 5. Decision filter

Before adding a deliverable, abstraction, dependency, or component, ask:

1. Does it solve a problem required by the next usable scenario?
2. Does it prevent a realistic safety, correctness, or maintenance failure?
3. Can the problem be solved more directly?
4. Can the choice be replaced later without rewriting GAIA identity?
5. Can one person understand and operate it?
6. Does the expected value justify delaying production use?

If the answer to questions 1 and 2 is no, defer the item.

## 6. Maturity stages

GAIA progresses through evidence-based stages:

0. Research Foundation
1. Architecture Convergence
2. Minimal Core Prototype
3. First Domestic Production Slice
4. Operational Hardening
5. Domain Expansion
6. Long-Term Evolution

Progress is based on reduced uncertainty and demonstrated behaviour, not document volume or feature count.

## 7. Stage 0: Research Foundation

**Status:** Substantially complete.

### Objective

Establish project identity, principles, vocabulary, research history, and the initial conceptual model.

### Existing deliverables

- project identity and North Star;
- Design Principles and Manifesto;
- Sprint 1 and Sprint 2 research;
- reuse analysis and architectural critique;
- initial Glossary and GAIA Model;
- repository organisation guidance.

### Closure condition

Stage 0 closes when the proposed v0.2 reference documents are reviewed and unresolved questions remain visible rather than hidden.

## 8. Stage 1: Architecture Convergence

**Status:** In progress.

### Objective

Create a coherent, implementation-neutral foundation sufficient to begin a small prototype without designing the final system.

### Required deliverables

#### Foundation and reference reconciliation

- `ARCHITECTURE_CONVERGENCE_v0.2.md` — produced;
- `CONTEXT_MODEL_v0.2.md` — produced;
- `WORLD_MODEL_v0.2.md` — produced;
- `GLOSSARY_v0.2.md` — produced;
- `GAIA_MODEL_v0.2.md` — produced;
- `NEXT_STEPS_v0.2.md` — produced by this reconciliation;
- `REPOSITORY_STRUCTURE_v0.2.md` — paired reconciliation deliverable.

#### Minimum accepted ADR baseline before prototype

The current minimum accepted ADR baseline is:

1. `ADR-0001-Core-Boundary.md` — Accepted
2. `ADR-0003-Capability-Model_Accepted.md` — Accepted

Other ADRs remain candidates until the prototype produces evidence.

#### Validation brief

- `sprint-03/MEMORY_ROLE_VALIDATION.md`

This may start as a short validation brief rather than a large research document.

### Completion criteria

- terminology is coherent across the v0.2 reference set;
- World Model remains semantic rather than a component;
- Context, Memory, Knowledge, and Audit are separated;
- the Core boundary is decided sufficiently for prototype work;
- the Capability contract is decided sufficiently for one scenario;
- the first production slice is explicit and small;
- deferred complexity is documented;
- no implementation depends on an undocumented architectural assumption.

### Explicit non-goals

Stage 1 does not require:

- a final Memory architecture;
- a general Planner;
- Event semantics;
- a Registry;
- a Plugin model;
- multi-Domain orchestration;
- a general security platform;
- selection of every technology.

## 9. Stage 2: Minimal Core Prototype

### Objective

Build the smallest replaceable prototype that tests the current conceptual boundaries with real behaviour.

### Recommended first scenario

Use a read-only or low-risk domestic query, for example:

> Determine whether selected windows or doors are open and explain unavailable, stale, or ambiguous state.

This scenario is recommended because it can test:

- Resource identity and Resource References;
- Home Assistant as an Authoritative Source for selected state;
- a bounded Domain View;
- Request Context;
- one Collaborator responsibility;
- source-grounded Observation;
- freshness and unavailable state;
- no-action or low-risk Capability semantics;
- channel-neutral response meaning.

### Minimum deliverables

- one bounded request flow;
- one Collaborator definition;
- one or more read-only Capabilities;
- a small Resource set;
- a direct Home Assistant Adapter;
- a direct initial channel Adapter;
- explicit failure and uncertainty handling;
- minimal diagnostic trace;
- tests for deterministic boundaries;
- a prototype README listing exclusions.

### Implementation bias

For this stage, prefer:

- one runtime rather than a provider abstraction;
- direct Adapter interfaces rather than Plugin infrastructure;
- in-process coordination rather than distributed messaging;
- explicit routing rather than a general Planner;
- simple structured records rather than a graph platform;
- local persistence only when a validated continuity need exists;
- manual configuration rather than a configuration platform.

### Explicit non-deliverables

- complete Memory;
- general orchestration;
- Event bus;
- Registry;
- Plugin ecosystem;
- broad automation;
- complete UI;
- multi-machine distribution;
- production-grade HA clustering;
- framework abstraction for hypothetical future providers.

### Completion criteria

- the scenario works end to end;
- ambiguity, unavailable data, and stale data do not produce false certainty;
- the channel and Home Assistant remain replaceable boundaries;
- the Core does not contain Home Domain logic;
- deterministic logic is tested;
- the implementation remains small enough to discard;
- the prototype identifies the next real architectural uncertainty.

## 10. Stage 3: First Domestic Production Slice

### Objective

Turn one validated scenario into a small, reliable, always-available domestic capability.

### Scope rule

Promote only behaviour already demonstrated in the prototype. Add one production concern at a time.

### Required deliverables

- one clearly documented domestic use case;
- a small Capability allowlist;
- explicit Resource mapping;
- user-visible uncertainty and failure behaviour;
- safe startup and restart behaviour;
- configuration and secret handling appropriate to a personal local system;
- basic logs or diagnostic evidence;
- automated tests for deterministic rules;
- manual recovery instructions;
- a simple rollback or disable mechanism.

### Initial action policy

Prefer read-only queries first. Introduce state-changing actions only when:

- the target Resource is unambiguous;
- Capability scope is explicit;
- failure is observable;
- the action is reversible or requires explicit Approval;
- the Human Owner can disable it easily.

### Completion criteria

- the system provides recurring domestic value;
- restart and common failures are understandable;
- unsafe ambiguity results in clarification or refusal;
- operation does not require daily maintenance;
- the Human Owner can inspect, stop, and recover the system;
- no enterprise-grade platform was built unnecessarily.

## 11. Stage 4: Operational Hardening

### Objective

Improve reliability only after the first production slice creates real value.

### Candidate deliverables, introduced by evidence

- backup and restore;
- upgrade and rollback;
- dependency review;
- more structured Audit where actions require it;
- threat review for exposed interfaces;
- stronger secret handling;
- regression tests;
- health checks;
- degraded-mode behaviour;
- retention and cleanup rules;
- operational documentation.

### Guardrail

Do not build enterprise governance, complex observability, distributed tracing, or high-availability infrastructure unless a concrete domestic failure mode justifies it.

## 12. Stage 5: Domain Expansion

### Entry condition

Begin only when the Home Domain demonstrates stable boundaries and useful production behaviour.

### Required questions

- Can another Domain use the Core without rewriting it?
- Are Capability semantics reusable?
- Does Shared Context remain bounded?
- Is Memory now required?
- Is a Registry now justified?
- Has direct routing become insufficient?

A second Domain is evidence for generalisation, not a reason to generalise in advance.

## 13. Stage 6: Long-Term Evolution

Ongoing practices may include:

- periodic architecture review;
- ADR supersession;
- dependency replacement;
- Collaborator lifecycle and deprecation;
- Memory retention and correction review;
- security and permission review;
- Idea Incubator cleanup;
- documentation consolidation.

The project is healthy when old decisions can be replaced without losing history and one person can still understand why GAIA has its current shape.

## 14. Candidate ADR backlog

| Priority | ADR | Current treatment |
|---|---|---|
| Accepted | ADR-0001 Core Boundary | Accepted baseline for prototype structure. |
| Accepted | ADR-0003 Capability Model | Accepted baseline for Capability implementation. |
| 3 | ADR-0002 Memory Semantics | Defer until Memory validation produces evidence. |
| 4 | ADR-0004 Home Assistant Boundary | Draft after first prototype evidence if the boundary remains unclear. |
| 5 | ADR-0005 Communication State | Draft when restart, channel replacement, or multi-turn continuity creates pressure. |
| 6 | ADR-0006 Tool Trust | Draft before sensitive Tool execution expands. |
| 7 | ADR-0007 Event Semantics | Draft only if events solve a demonstrated coordination or Audit problem. |

The filenames are provisional candidates until each ADR is created.

## 15. Idea Incubator

Ideas remain non-committed until they solve a validated problem:

- Memory Inspector;
- Capability Simulator;
- Planner red-team exercise;
- MCP kill-switch test;
- Event chaos testing;
- Research Collaborator;
- Voice Domain;
- auto-generated Domains;
- runtime scorecard;
- Home Assistant replay sandbox;
- Collaborator version diff;
- boundary violation detector;
- Knowledge provenance viewer;
- long-term Memory review assistant.

## 16. Fast-path exclusions

The following do not block the first production slice:

- polished general UI;
- multi-provider abstraction;
- general Knowledge Graph;
- Event sourcing;
- distributed deployment;
- multi-user support;
- Plugin marketplace;
- cross-Domain planner;
- complete Memory system;
- universal Resource taxonomy;
- perfect documentation formatting.

They remain available for future evidence-based promotion.

## 17. Stop conditions

Pause and review architecture when:

- implementation places Domain logic in the Core;
- multiple components silently write shared state;
- model inference becomes action authority;
- the same Resource resolves ambiguously during action;
- a dependency becomes difficult to replace;
- operation requires frequent manual repair;
- a simple change requires broad unrelated modification;
- production speed is being reduced by hypothetical future needs rather than current correctness or safety.

## 18. Next concrete steps

1. Review and accept or revise the complete v0.2 reference set.
2. Use accepted `ADR-0001-Core-Boundary.md` as the Core baseline.
3. Use accepted `ADR-0003-Capability-Model_Accepted.md` as the Capability baseline.
4. Write a short first-scenario validation brief.
5. Begin the minimal read-only prototype.
6. Defer all non-blocking sophistication.

## 19. Success indicators

GAIA is progressing when:

- useful domestic behaviour reaches production incrementally;
- the Core remains small and understandable;
- Capabilities and Resources are explicit;
- failures and uncertainty are visible;
- external systems remain bounded;
- the Human Owner retains control;
- dependencies and components can be replaced;
- documentation supports decisions without becoming the product;
- one person can operate the system without a second job.

## 20. Final statement

GAIA should be professionally engineered but proportionate to a personal domestic project.

The preferred path is not maximum architectural elegance. It is the shortest safe path to useful, maintainable production behaviour.
