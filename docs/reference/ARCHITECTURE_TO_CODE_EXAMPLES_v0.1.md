# Architecture to Code Examples

**Project:** GAIA  
**Document type:** Foundation Examples Draft  
**Status:** Proposed  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Date:** 2026-08-03  
**Companion document:** `ARCHITECTURE_TO_CODE_v0.1.md`

## 1. Purpose

This document is the practical examples companion to `ARCHITECTURE_TO_CODE_v0.1.md`.

Its purpose is to collect concrete examples showing how GAIA architectural concepts should be translated into code-level responsibilities.

It is intentionally a draft. It should be updated when real implementation evidence appears from the Home Domain, Fake Adapter, Home Assistant Adapter, Telegram Adapter, tests, or future Domains.

The examples are conceptual. They are not implementation instructions and do not select a framework, language, library, or folder structure.

## 2. How to use this document

Use this document when a developer asks:

```text
I know the architecture, but where should this code go?
```

Each example should answer:

- what the user wants;
- which GAIA concepts participate;
- which component receives the request;
- which component decides meaning;
- which component executes externally;
- which component formats the response;
- what must not be mixed.

## 3. Example A: read whether a kitchen window is open

### User request

```text
Is the kitchen window open?
```

### Components involved

| Responsibility | Component |
|---|---|
| Receive message | Channel Adapter |
| Normalise request | Channel Adapter |
| Route request | Core |
| Interpret Home meaning | Home Collaborator / Home Domain |
| Define operation | `ReadOpeningState` Capability |
| Identify target | `KitchenWindow` Resource |
| Read source state | Home Assistant Adapter |
| Interpret result | Home Domain |
| Return structured outcome | Core |
| Render response | Channel Adapter |

### Correct responsibility split

The Home Domain may know that `kitchen window` is an alias for a specific Home Resource.

The Home Assistant Adapter may know that this Resource maps to an external Home Assistant entity reference.

The Core must not know either the alias or the Home Assistant entity ID.

### Possible conceptual objects

```text
Request
HomeCollaborator
ReadOpeningStateCapability
HomeResourceReference
OpeningStateObservation
StructuredOutcome
```

### Common mistake

Putting this in Core:

```text
if request.contains("kitchen window"):
    call Home Assistant entity binary_sensor.kitchen_window
```

Why wrong:

- Core now knows Home vocabulary;
- Core knows Home Assistant representation;
- Resource resolution and external execution are mixed.

## 4. Example B: read all upstairs windows

### User request

```text
Are any upstairs windows open?
```

### What changes compared with Example A

This is no longer a single Resource lookup. It is a scoped Resource set.

The Home Domain must resolve:

```text
upstairs windows
```

into a bounded set of known Resources.

### Correct flow

```text
Channel Adapter
↓
Core
↓
Home Collaborator
↓
Home Domain resolves upstairs + windows
↓
ReadOpeningState Capability applies to Resource set
↓
Home Assistant Adapter reads each mapped source reference
↓
Home Domain aggregates result
↓
Structured Outcome
```

### Possible outcomes

```text
Success
PartialSuccess
ResourceAmbiguous
SourceUnavailable
InformationStale
```

### Key lesson

Aggregation belongs to the Domain or Collaborator responsibility, not to the Adapter.

The Adapter can read multiple external states, but it should not decide what `upstairs` means.

## 5. Example C: turn on a kitchen light

### User request

```text
Turn on the kitchen light.
```

### Operation kind

```text
Act
```

### Risk level

Usually:

```text
Moderate
```

because it changes physical state, even if reversible.

### Required responsibility split

| Concern | Owner |
|---|---|
| User message | Channel Adapter |
| Routing | Core |
| Home interpretation | Home Collaborator / Home Domain |
| Capability meaning | `TurnOnLight` Capability |
| Resource identity | Home Domain |
| Policy Result | Policy evaluation boundary |
| Approval requirement | Capability / Policy decision |
| Execution | Home Assistant Adapter |
| Evidence | Minimal evidence boundary |

### Important distinction

A read-only operation may be `Allowed` by default.

A state-changing action may require:

```text
ApprovalRequired
```

or may remain unsupported in the first slice.

### Common mistake

Adding this method to a Resource:

```text
KitchenLight.turn_on()
```

Why wrong:

- Resource becomes active infrastructure;
- execution bypasses Capability and Policy;
- external binding leaks into the model.

## 6. Example D: open the garage

### User request

```text
Open the garage.
```

### Why this is more sensitive

Opening a garage may have physical security implications.

Even if technically simple, architecturally it should not be treated like reading temperature.

### Expected policy posture

In an early GAIA implementation, this should probably return:

```text
Unsupported
```

or:

```text
ApprovalRequired
```

not direct execution.

### Correct outcome example

```text
I can identify the garage door, but opening it is not enabled in this GAIA slice.
```

Underlying structured outcome:

```text
Unsupported
```

### Key lesson

Technical ability is not architectural permission.

If Home Assistant can open the garage, that does not mean GAIA should expose that action immediately.

## 7. Example E: send a Telegram message

### User request

```text
Send me a Telegram summary of open windows.
```

### Two possible interpretations

#### Interpretation 1: Telegram is just the current channel

If the user is already talking through Telegram, the Channel Adapter simply formats the response.

#### Interpretation 2: Telegram is a target communication Capability

If the user asks GAIA to send a message through Telegram as an action, this may become a Communication Domain concern.

### Correct distinction

| Situation | Responsibility |
|---|---|
| Reply in the same Telegram chat | Channel Adapter formatting |
| Send a new Telegram notification | Communication Capability + Telegram Adapter |

### Common mistake

Letting the Telegram Adapter fetch Home state.

Why wrong:

- channel and Domain logic become coupled;
- Telegram becomes the application;
- Home cannot be reused with another channel.

## 8. Example F: remember a preferred alias

### User request

```text
When I say garage, I mean the external garage.
```

### Possible classification

This may be:

```text
Configuration
```

or:

```text
Memory candidate
```

It is not automatically Memory.

### Questions before implementation

- Is the preference explicit?
- Should it apply across future interactions?
- Can the Human Owner inspect it?
- Can the Human Owner correct it?
- Can the Human Owner delete it?
- Is configuration a simpler owner?

### Correct early implementation bias

Prefer a human-readable configuration entry before a general Memory subsystem.

### Common mistake

Storing every clarification as Memory.

Why wrong:

- temporary Context becomes long-term state;
- incorrect assumptions persist;
- Memory grows without governance.

## 9. Example G: source unavailable

### User request

```text
Is the front door open?
```

### External condition

Home Assistant is unavailable.

### Correct behaviour

The Adapter reports source unavailability.

The Domain does not invent state.

The Core returns a structured outcome:

```text
SourceUnavailable
```

The response may say:

```text
I cannot check the front door right now because Home Assistant is unavailable.
```

### Common mistake

Returning the last known state as if current.

Why wrong:

- stale or retained data is presented as authority;
- Home Assistant authority is bypassed;
- user may make a wrong physical-world decision.

## 10. Example H: ambiguous resource

### User request

```text
Is the bedroom window open?
```

### Problem

The Home Domain knows two bedroom windows:

```text
Bedroom east window
Bedroom west window
```

### Correct behaviour

Return:

```text
ResourceAmbiguous
```

Ask a focused clarification:

```text
Do you mean the east bedroom window or the west bedroom window?
```

### Common mistake

Pick the first match.

Why wrong:

- ambiguity is hidden;
- future state-changing actions become unsafe;
- user trust is degraded.

## 11. Example I: model interpretation conflicts with source

### Situation

A model-generated response says:

```text
The garage is closed.
```

But Home Assistant reports:

```text
open
```

### Correct authority rule

Home Assistant is the Authoritative Source for selected reported state.

Model output is not Authority.

### Correct behaviour

Use the source-grounded Observation and optionally record the conflict as a diagnostic issue.

### Common mistake

Trusting fluent natural language over structured source data.

Why wrong:

- model output becomes false authority;
- deterministic boundaries become meaningless.

## 12. Example J: where a class belongs

### Candidate class

```text
HomeAssistantOpeningStateClient
```

### Likely location

Adapter boundary.

### Why

It talks to Home Assistant and retrieves external state.

### It should not

- resolve user labels;
- decide whether a Resource is in scope;
- enforce Approval;
- format Telegram messages.

## 13. Example K: where another class belongs

### Candidate class

```text
HomeResourceResolver
```

### Likely location

Home Domain.

### Why

It maps user-facing Home concepts such as `kitchen window` or `upstairs windows` to GAIA Resource References.

### It should not

- call Home Assistant;
- call Telegram;
- store secrets;
- perform policy enforcement.

## 14. Example L: where an outcome belongs

### Candidate record

```text
StructuredOutcome
```

### Likely location

Core or shared contract layer.

### Why

Structured outcomes are needed across Domain, Core, and Channel formatting.

### Required examples

```text
Success
PartialSuccess
ClarificationRequired
ResourceAmbiguous
SourceUnavailable
InformationStale
Denied
Indeterminate
Unsupported
Failure
```

### It should not

Contain UI formatting, Telegram markup, or Home Assistant raw payloads.

## 15. Example case template for future real evidence

Use this template when a real implementation case appears.

```text
## Real Case: <short title>

Date:
Source:
Scenario:
User request:
Implemented components:
Architectural decision involved:
Accepted ADRs affected:
Responsibility split:
What worked:
What failed:
Unexpected coupling:
Tests added:
Documentation update needed:
ADR review needed: yes/no
Recommendation:
```

## 16. Candidate real cases to add later

After implementation starts, add real examples for:

- first Fake Adapter request;
- first Home Assistant unavailable response;
- first ambiguous Resource label;
- first unsupported action request;
- first real Telegram rendering;
- first configuration alias;
- first test failure caused by boundary leakage;
- first case where ADR-0001 or ADR-0003 needs clarification.

## 17. Versioning guidance

This examples document should be versioned because it will grow with implementation evidence.

Recommended current filename:

```text
ARCHITECTURE_TO_CODE_EXAMPLES_v0.1.md
```

When real examples are added substantially, create:

```text
ARCHITECTURE_TO_CODE_EXAMPLES_v0.2.md
```

Minor typo fixes can update the active file without a new version.

## 18. Relationship with repository structure

Recommended location during Architecture Convergence:

```text
reference/ARCHITECTURE_TO_CODE_v0.1.md
reference/ARCHITECTURE_TO_CODE_EXAMPLES_v0.1.md
```

After convergence closes and Git history resumes, the canonical names may become:

```text
reference/ARCHITECTURE_TO_CODE.md
reference/ARCHITECTURE_TO_CODE_EXAMPLES.md
```

## 19. Final statement

The examples document exists to protect the architecture during implementation.

It should remain practical, concrete, and easy to update.

When real code teaches something new, add the lesson here before changing the Foundation or creating a new ADR.
