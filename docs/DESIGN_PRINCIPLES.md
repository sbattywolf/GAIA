# Design Principles

> Recovery status: Recovered in substance and conservatively normalised  
> Source basis: surviving Microsoft 365 GAIA reference artefacts and conversation history  
> Confidence: High  
> Preservation rule: This file retains its original role. Reconstructed passages are not presented as verbatim recovery.

1. **Human First** - Important actions and sensitive decisions remain visible, governable and correctable.
2. **Local First** - Prefer local ownership, local control and local execution when practical. Cloud use must be explicit and replaceable.
3. **Simplicity** - Complexity needs demonstrated value and a clear boundary.
4. **Replaceability** - Models, frameworks, runtimes, channels and adapters must not define GAIA's identity.
5. **Bounded Collaborators** - A collaborator has a named responsibility and must not become an unbounded assistant.
6. **Explicit Capabilities** - Authority is expressed through enforceable capabilities, not implied by prompts.
7. **Intentional Memory** - Remembered information is inspectable, correctable and forgettable.
8. **Observable Behaviour** - Important interpretation, retrieval, approval, action, denial and failure are explainable.
9. **Sustainable Complexity** - A very small team must remain able to understand, operate and replace the system.
10. **Identity Over Implementation** - Architecture protects the durable identity; implementation does not redefine it.
11. **Reuse Before Build** - When a suitable external technology already solves a bounded problem, evaluate reuse before creating GAIA-specific infrastructure. Reuse is not automatic adoption: the technology must remain bounded, replaceable where practical, and subordinate to GAIA's semantic and authority boundaries.

## Authority and provenance

GAIA applies the governance principle:

> **ONE AUTHORITY PER RESPONSIBILITY**

For project governance, this means:

- Git/repository is the durable project Source of Truth for committed project state.
- Accepted ADRs are authoritative for the architectural decisions they explicitly own.
- Project Knowledge is contextual/supporting and does not become architectural authority merely by containing a copy or synthesis.
- QNAP is a storage/archive role unless a separate governance decision explicitly assigns another responsibility.
- Derived copies, exports, indexes and delivery packages must preserve provenance and must not silently become authoritative.

This is a governance boundary, not a new runtime architecture. It does not define synchronization, lifecycle taxonomy, metadata requirements, QNAP-primary artifact classes, or automated ingestion.

## Decision test

A proposal should identify the problem solved, the new state owned, the failure mode introduced, the replacement path and the operational burden. It should also answer whether an existing suitable technology can satisfy the bounded need before new infrastructure is created. If these are unclear, the proposal remains experimental.
