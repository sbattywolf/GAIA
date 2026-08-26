# STR-3 — A/B Engineer — Controlled Comparison

## Status
OPEN / INVESTIGATION

## Authority
AI Architect authorization following STR-2 closure

## Baseline
STR-2 — ACCEPTED / CLOSED

## Objective
Determine, through a controlled comparison, whether two Engineer implementations/contexts exhibit the same durable Engineer semantics when evaluated against the accepted STR-2 contract.

## Non-goals
- no new Engineer architecture
- no Agent framework
- no model selection
- no host/runtime architecture
- no Remote Master implementation
- no repository redesign
- no automatic promotion of one Engineer as canonical
- no assumption that 3090 or 1070 defines Engineer identity

## Comparison dimensions
Start by identifying candidate dimensions only.

At minimum consider:
- scope handling
- authority handling
- capability use
- boundary preservation
- STOP/escalation behavior
- evidence discipline
- validation/acceptance distinction
- uncertainty handling

## Evidence model
Define what would count as:
- OBSERVED
- VERIFIED
- INFERRED
- PROPOSED
- UNKNOWN

## Comparison boundary
Explicitly separate:
- Engineer semantics
- vs model
- vs host
- vs runtime
- vs mission
- vs tooling.

## Success / failure semantics
Do not define implementation yet.
Define what evidence would allow the comparison to conclude:
- equivalent
- materially different
- insufficient evidence

## Open questions
Record unresolved questions before designing the experiment.

## First checkpoint
Produce a controlled-comparison proposal for Architect review
BEFORE executing or implementing the experiment.