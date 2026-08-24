# First Home Scenario Validation Brief

**Project:** GAIA  
**Document type:** Validation Brief  
**Status:** Planned  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Date:** 2026-08-03  
**Validation owner:** Human Owner

## 1. Purpose

This brief defines the first end-to-end scenario used to validate the accepted Core and Capability boundaries before building a broader GAIA platform.

The scenario is deliberately narrow, read-only, domestic, and useful. It must produce evidence about the architecture while remaining small enough to implement directly and discard or refactor later.

## 2. Scenario

The Human Owner asks GAIA whether selected windows or doors are currently open.

Representative requests include:

```text
Are any upstairs windows open?
Is the kitchen window open?
Which external doors are currently open?
```

GAIA returns confirmed state where available and clearly distinguishes ambiguous, stale, unavailable, unsupported, or partially known information.

## 3. User value

The scenario provides immediate domestic value by reducing the effort required to inspect multiple Home Assistant entities.

It is suitable as the first slice because it exercises useful architecture without introducing physical state changes or a general automation platform.

## 4. Architectural questions under validation

The scenario should answer:

1. Can a small in-process Core coordinate the request without a Planner, Registry, Event Bus, or Workflow engine?
2. Can the Home Domain contain all home-specific interpretation?
3. Can Home Assistant remain the Authoritative Source for selected reported state?
4. Can Resources be described without leaking Home Assistant identifiers into Core contracts?
5. Can the Capability remain independent of its execution binding?
6. Can Context remain bounded and temporary?
7. Can uncertainty and failures remain structured beneath natural-language output?
8. Can the same result be formatted by another channel without changing Domain logic?
9. Can the scenario run without a general Memory subsystem?
10. Is the resulting implementation understandable and operable by one Human Owner?

## 5. Capability under validation

The scenario uses one conceptual Capability:

```text
Read current opening state for a bounded set of home entry Resources.
```

### Initial classification

| Element | Value |
|---|---|
| Operation kind | Read |
| Risk level | Low |
| Approval requirement | None by default |
| Resource scope | Explicitly selected window or door Resources |
| Policy result | Allowed when scope and source access are valid; otherwise Indeterminate or Denied as appropriate |
| Execution binding | Direct Home Assistant Adapter |
| Evidence | Correlation, Capability version, Resource references, Policy Result, outcome, material failure reason |

This table is validation input, not a final serialisation schema.

## 6. Resource scope

The initial Resource set should be intentionally small.

Recommended scope:

- two or three windows;
- one or two external doors;
- one or two locations needed to test grouping;
- at least one deliberately ambiguous label;
- at least one unavailable or stale test case.

Do not import every Home Assistant entity.

### Resource rules

- A GAIA Resource is distinct from a Home Assistant entity identifier.
- The Home Domain owns labels, grouping, and location interpretation.
- The Home Assistant Adapter owns translation to and from Home Assistant representations.
- The Core handles only Resource References and structured outcomes required by coordination.
- Similar labels do not prove Resource identity.

## 7. Authoritative source

Home Assistant is the Authoritative Source for the selected reported opening state in this scenario.

GAIA may interpret, aggregate, or explain the reported information, but it must not silently replace source state with model inference or retained Memory.

If Home Assistant is unavailable, GAIA returns an explicit unavailable outcome rather than guessing.

## 8. Expected conceptual flow

```text
Channel input
    ↓
Channel Adapter translates to bounded Request
    ↓
Core validates and correlates Request
    ↓
Core routes to Home Collaborator
    ↓
Home Domain resolves labels and bounded Resource scope
    ↓
Core obtains Policy Result for read Capability
    ↓
Execution Binding invokes Home Assistant Adapter
    ↓
Adapter retrieves source-grounded Observations
    ↓
Home Domain interprets freshness and grouping
    ↓
Core returns structured outcome
    ↓
Channel Adapter renders the response
```

This flow does not require every step to become a separate class or service.

## 9. Request and Context

### Request Context

May contain:

- normalised user intent;
- originating channel reference;
- requested location or label;
- relevant Resource References;
- correlation reference;
- uncertainty requiring clarification.

### Collaborator Context view

Contains only the subset needed by the Home Collaborator.

### Interaction Context

Use only when clarification or follow-up is required.

### Shared Context

Do not introduce Shared Context unless more than one bounded responsibility demonstrably requires the same information.

### Memory

Do not retain request details, source state, or clarification automatically. Record real continuity gaps separately for `MEMORY_ROLE_VALIDATION.md`.

## 10. Structured outcomes

The implementation must distinguish at least:

| Outcome | Meaning |
|---|---|
| Success | Requested state is known with sufficient authority and freshness. |
| PartialSuccess | Some requested Resources are known and others are unavailable, stale, or unresolved. |
| ClarificationRequired | Resource or scope cannot be resolved safely. |
| ResourceAmbiguous | Multiple plausible Resources remain. |
| SourceUnavailable | Home Assistant cannot provide the required information. |
| InformationStale | Available information is too old for the Domain rule. |
| Denied | Policy does not permit the request. |
| Indeterminate | Required Policy or scope decision cannot be completed. |
| Unsupported | The requested Resource or operation is outside the implemented slice. |
| Failure | An unexpected execution or mapping error occurred. |

Names may change during implementation, but the semantic distinctions must remain.

## 11. Response rules

The user-facing response should:

- answer directly when state is confirmed;
- identify which Resources are open when requested;
- state when some results are unavailable or stale;
- ask a focused clarification when identity is ambiguous;
- never present inference as confirmed state;
- avoid exposing internal Home Assistant identifiers unless diagnostic mode explicitly requires them;
- remain channel-neutral before final formatting.

## 12. Required failure cases

The prototype must test:

1. Home Assistant unavailable;
2. unknown Resource label;
3. ambiguous Resource label;
4. entity present but state unavailable;
5. stale information according to the chosen Domain rule;
6. one failed Resource in a multi-Resource request;
7. unsupported action request such as opening or closing a Resource;
8. malformed Adapter response;
9. model-generated interpretation conflicting with source data;
10. Policy Result is Indeterminate.

## 13. Test strategy

### Deterministic unit tests

Test:

- Request validation;
- explicit routing;
- Resource-scope checks;
- Policy Result handling;
- ambiguity handling;
- freshness interpretation;
- structured outcome mapping;
- prevention of unsupported Act operations.

### Adapter integration tests

Test:

- source translation;
- unavailable or malformed responses;
- mapping between GAIA Resource References and Home Assistant identifiers;
- timeout and dependency failure behaviour.

### End-to-end tests

Test representative requests through one channel Adapter and the complete structured result path.

Model wording quality is not a substitute for deterministic boundary tests.

## 14. Minimal evidence to record

For each validation run, retain only:

- scenario identifier;
- request category;
- Capability identifier and version;
- target Resource references;
- Policy Result;
- structured outcome;
- material failure or ambiguity reason;
- test result;
- architectural observation.

No general Audit platform is required.

## 15. Implementation bias

Prefer:

- one process;
- direct object or function calls;
- explicit configuration;
- a small Resource mapping;
- one direct Home Assistant Adapter;
- one channel Adapter;
- deterministic routing;
- simple language-native records;
- focused tests;
- clear logs.

Do not introduce:

- Planner;
- Registry;
- Event Bus;
- Workflow engine;
- Plugin system;
- graph database;
- vector store;
- general Memory;
- microservices;
- provider abstraction;
- multi-Domain coordination.

## 16. Deliverables

The validation should produce:

1. a short implementation README;
2. the concrete Capability definition used by the prototype;
3. the small Resource mapping used by the Home Domain;
4. deterministic Core and Domain tests;
5. Home Assistant Adapter integration tests;
6. a scenario evidence table;
7. a list of architecture observations;
8. any continuity gaps copied into `MEMORY_ROLE_VALIDATION.md`;
9. recommendations for keeping, amending, or revisiting ADR-0001 and ADR-0003.

## 17. Success criteria

The scenario is successful when:

- it provides useful read-only domestic information end to end;
- Domain logic does not leak into the Core;
- external identifiers do not define GAIA Resource identity;
- Resource scope and Policy Result are explicit;
- ambiguity and unavailable information do not become false certainty;
- no general Planner, Registry, Event Bus, Workflow, Plugin, or Memory platform is required;
- deterministic boundaries are tested;
- the implementation is understandable by the Human Owner;
- at least one real architectural lesson is recorded.

## 18. Stop conditions

Stop and simplify if implementation starts requiring:

- a generic orchestration framework;
- dynamic discovery;
- a global shared state container;
- broad import of Home Assistant entities;
- persistent conversation history;
- general-purpose permission infrastructure;
- distributed deployment;
- extensive abstractions serving no current test case.

## 19. Review decision after validation

After evidence is collected, choose one outcome:

- **Proceed:** architecture is sufficient for the first production slice;
- **Amend:** a compatible clarification is needed in an ADR or Foundation Document;
- **Supersede:** a material boundary decision is incorrect;
- **Narrow:** the production slice must be reduced;
- **Defer production:** correctness or operational risk is unresolved.

## 20. Current recommendation

Proceed with this read-only scenario as the first implementation target.

Do not add state-changing operations until the read path, Resource resolution, failure semantics, and Policy enforcement are proven.

**The first prototype should prove boundaries and deliver one useful domestic answer, not prove that GAIA can become a platform.**
