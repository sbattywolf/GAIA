# ADR-0002-Memory-Semantics: Memory Semantics

- **Status:** Proposed
- **Decision date:** Not decided
- **Owners:** Project owner / architect
- **Related validation:** See `validation/`

## Context

What is memory, who owns it, and how is it corrected, exported, retained, and forgotten?

## Decision drivers

- Human control
- Local-first ownership
- Simplicity and sustainable complexity
- Explicit boundaries
- Replaceability
- Observability and recovery

## Options considered

1. Minimal internal implementation.
2. Reuse behind a GAIA-owned adapter or contract.
3. Adopt an external framework abstraction.
4. Defer until evidence exists.

## Current evidence

Documentation identifies this as an open architectural concern. Evidence from representative prototypes is still required.

## Decision

**Not decided.** This ADR remains Proposed.

## Consequences

To be completed after validation and decision.

## Validation required before acceptance

- representative scenario;
- failure and degraded-mode behaviour;
- ownership and boundary test;
- replacement or exit test;
- operational cost for a very small team;
- security and audit implications.
