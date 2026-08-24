# ADR-0007: Event and Run Semantics

- **Status:** Proposed
- **Decision:** Not yet made
- **Recovery status:** Individual ADR reconstructed from surviving ADR candidate lists, Sprint materials and reference documents
- **Confidence:** Medium
- **Rule:** This file preserves the decision topic and analysis space. It does not invent an accepted decision.

## Context

What constitutes an event and a bounded run, and how should causality, status and audit be represented?

This question is repeatedly identified as architecturally significant in the surviving GAIA material. It must be resolved explicitly rather than being decided accidentally by the first implementation or by an adopted framework.

## Decision drivers

- Identifiers and correlation
- Causality and timestamps
- Lifecycle and terminal states
- Errors and partial completion
- Retention, replay and migration

## Alternatives to evaluate

- No first-class event model initially
- Minimal immutable event envelope
- Run-centric trace
- Event bus model
- Framework-native checkpoints behind an adapter

## Required evidence before decision

- Evidence from bounded first-domain scenarios.
- State ownership and failure-mode analysis.
- Operational burden for a very small team.
- Human-control and observability consequences.
- Replacement, migration and rollback path.
- Impact on GAIA-native vocabulary and identity tests.

## Questions that must remain open

- What is the smallest decision that reduces uncertainty?
- Which assumptions are facts, observations, external practices or opinions?
- What implementation evidence is valid, and what is merely prototype bias?
- What would cause this ADR to be rejected or superseded?

## Decision outcome

Not decided. Do not populate this section until review explicitly accepts an alternative.

## Consequences

Not yet applicable. Consequences must be recorded only with an accepted decision.

## Related material

- `../reference/IDENTITY.md`
- `../reference/GAIA_MODEL.md`
- `../reference/DESIGN_PRINCIPLES.md`
- `../sprint-01/04_Architectural_Critique.md`
- `../sprint-01/05_Architecture_Discussion_Guide.md`
- `../sprint-02/02_Architectural_Stress_Test.md`
- `../sprint-02/06_Sprint2_Synthesis.md`
