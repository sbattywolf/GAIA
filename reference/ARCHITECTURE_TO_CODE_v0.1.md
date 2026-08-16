# Architecture to Code

**Project:** GAIA  
**Document type:** Foundation Bridge Document  
**Status:** Proposed  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Date:** 2026-08-03

## 1. Purpose

This document bridges GAIA architectural documentation and implementation design.

It explains how accepted concepts and ADRs should influence modules, classes, interfaces, and responsibility boundaries before any Proof of Concept code is written.

The goal is not to prescribe a framework, language, library, runtime, or folder structure. The goal is to help a developer answer one practical question:

```text
Where does this responsibility belong?
```

This document should be read together with:

- `ADR-0001-Core-Boundary.md`;
- `ADR-0003-Capability-Model.md`;
- `GAIA_MODEL_v0.2.md`;
- `GLOSSARY_v0.2.md`;
- `CONTEXT_MODEL_v0.2.md`;
- `WORLD_MODEL_v0.2.md`;
- `FIRST_HOME_SCENARIO_VALIDATION.md`.

## 2. Concept-to-code mapping

### Core

The Core coordinates bounded requests and enforces architectural boundaries. It should live in a small central module such as `core`.

It may contain concepts such as request routing, execution coordination, context construction, policy-result enforcement, and structured outcome handling.

It must not contain Home-specific rules, Home Assistant calls, Telegram formatting, Memory implementation, provider SDK details, or world-state storage.

### Collaborator

A Collaborator represents a bounded digital responsibility. It may live under a Domain module, for example `domains/home`.

A Collaborator interprets a request within its responsibility, selects relevant Capabilities, asks the Domain to resolve Resource meaning, and produces a result or proposal.

It must not bypass the Core, call external APIs directly, own channel behaviour, or become a general assistant.

### Capability

A Capability describes what may be requested or performed. It is a semantic contract, not the implementation.

It may live in a shared capability module or close to the Domain that first defines it, but its meaning should remain independent from specific Tools or Adapters.

It must not contain Home Assistant entity IDs, HTTP calls, Telegram calls, approval workflows, audit history, or provider-specific schemas.

### Resource

A Resource is an identifiable subject of observation, reasoning, access, or action.

It may live in a Domain model or shared model layer, depending on whether it is Domain-specific or cross-Domain.

It must not call external systems, persist itself, execute actions, or hide ambiguous identity.

### Adapter

An Adapter translates between GAIA and an external boundary such as Telegram, Home Assistant, a model runtime, a file system, or another service.

It should live under an adapter/integration boundary.

It must not decide Domain meaning, own Capability semantics, or make business decisions. It translates, validates external protocol behaviour, and returns structured information.

### Registry

Registry is currently provisional. It may eventually catalogue known Collaborators, Capabilities, Tools, Adapters, or Resources.

Until real pressure exists, static configuration or explicit wiring is preferred.

It must not become a hidden service locator, dependency injection container, or orchestration brain.

### Event

Event is currently provisional. It may describe something that happened.

Until event semantics are accepted, use simple diagnostic or evidence records only when needed.

An Event should not execute logic, trigger hidden workflows, or become the default coordination mechanism.

### Memory

Memory is currently provisional and must be earned by demonstrated continuity value.

Do not create a general Memory subsystem for the first Home slice. Use authoritative source lookup, configuration, temporary Context, or operational persistence first.

Memory must not become a dump of conversation history, device state, logs, source data, or every model output.

### Domain

A Domain owns a coherent area of responsibility such as Home.

The Home Domain owns home concepts, labels, grouping, interpretation, freshness rules, and Resource resolution semantics.

A Domain must not become a platform, own unrelated concerns, or depend directly on channel details.

### World Model

World Model is a semantic foundation, not a runtime component.

It provides shared meaning for Resources, Observations, Assertions, Relationships, provenance, authority, time, uncertainty, and conflict.

It must not be implemented as a mandatory database, graph service, central state store, or universal source of truth in the first slice.

## 3. ADR-to-code mapping

### ADR-0001 Core Boundary

ADR-0001 means the Core should remain small, in-process, and focused on coordination and enforcement.

Code consequences:

- create clear request and outcome boundaries;
- route explicitly before introducing a Planner;
- delegate external execution to Adapters;
- keep Domain logic outside the Core;
- enforce Policy and Approval outcomes before execution;
- record only minimal evidence proportional to the scenario.

### ADR-0003 Capability Model

ADR-0003 means Capability must remain a small semantic contract.

Code consequences:

- keep Capability separate from execution binding;
- make Resource scope explicit;
- make Policy Result explicit;
- treat `Indeterminate` as non-executable;
- avoid a Capability Registry until real discovery pressure exists;
- test failure outcomes independently from natural-language response wording.

## 4. Request flow

A simple request should move through responsibilities in this shape:

```text
User
↓
Channel Adapter
↓
Core
↓
Collaborator
↓
Capability + Resource scope
↓
Policy / Approval result
↓
Execution Adapter
↓
Structured Outcome
↓
Channel Adapter
↓
User
```

The key rule is that receiving, deciding, executing, and formatting are separate responsibilities.

## 5. Where to write new code

Before writing a function, ask:

| Question | Likely location |
|---|---|
| Am I coordinating components? | Core |
| Am I applying Domain meaning? | Domain / Collaborator |
| Am I describing what may be done? | Capability |
| Am I identifying the target? | Resource model / Domain resolution |
| Am I calling an external system? | Adapter |
| Am I preserving evidence? | Minimal evidence / audit boundary |
| Am I retaining information across interactions? | Memory candidate, not automatic Memory |
| Am I cataloguing known items? | Registry candidate, if justified |
| Am I describing something that happened? | Event candidate, if justified |

If one function answers more than one row, split or relocate it.

## 6. Common implementation errors

- Domain logic in the Core.
- HTTP calls inside Collaborators.
- Capabilities implemented as concrete services.
- Telegram Adapter deciding application behaviour.
- Home Assistant entity IDs treated as canonical GAIA Resource identity.
- Resource objects invoking external systems.
- Registry introduced before static wiring fails.
- Event Bus introduced before event semantics are accepted.
- Memory introduced before retention value is validated.
- Natural-language response treated as the source of truth.

## 7. Future evolution

The model can grow from PoC to MVP to a broader system by adding more instances, not by moving responsibilities.

During PoC:

- one Core;
- one Home Collaborator;
- one read-only Capability;
- one Fake Home Assistant Adapter;
- one small Resource mapping.

During MVP:

- real Home Assistant Adapter;
- one channel Adapter;
- more read Capabilities;
- minimal evidence records;
- optional explicit configuration for aliases.

During system growth:

- additional Domains;
- more Collaborators;
- richer Adapters;
- Memory only if validated;
- Registry only if explicit wiring becomes insufficient;
- Event semantics only if required for correctness, coordination, or evidence.

## 8. Guided example

Scenario:

```text
Read the living room temperature.
```

Logical components:

- Channel Adapter receives the user message and creates a bounded Request.
- Core validates and routes the Request to Home.
- Home Collaborator interprets the intent as a read operation.
- Capability describes `ReadTemperature`.
- Home Domain resolves `living room temperature` to a Resource.
- Policy Result allows the low-risk read operation.
- Home Assistant Adapter retrieves the source-grounded observation.
- Home Domain interprets freshness and meaning.
- Core returns a structured outcome.
- Channel Adapter formats the message for the user.

Possible classes or records, conceptually:

```text
Core
RequestRouter
HomeCollaborator
ReadTemperatureCapability
HomeResourceReference
HomeAssistantAdapter
StructuredOutcome
ChannelResponseFormatter
```

No framework, library, or persistence choice is implied.

## 9. Relationship with examples document

Concrete examples, scenarios, anti-patterns, and future real cases are maintained in:

```text
ARCHITECTURE_TO_CODE_EXAMPLES_v0.1.md
```

This keeps the main bridge document stable and concise while allowing the examples document to grow as implementation evidence appears.
