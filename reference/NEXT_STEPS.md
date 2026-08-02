# Next Steps

## Current status

GAIA is in Research and Architectural Validation. The documentation foundation exists; final architecture, framework, memory, orchestration, deployment, and plugin decisions remain intentionally open.

## Phase 0: Research foundation

**Complete when:** canonical reference documents exist, vocabulary and model are clear, duplicate research is consolidated, and uncertainties are not hidden.

## Phase 1: Architectural validation

Create proposed ADRs for Core boundary, memory semantics, capability model, Home Assistant boundary, communication state, tool trust, and event semantics. Execute the validation briefs in `validation/`.

## Phase 2: Core prototype

Create the smallest replaceable prototype of Collaborator, Capability, Resource, Shared Context, execution trace, and audit. Explicitly exclude full memory, general planner, plugin ecosystem, full UI, and production security.

## Phase 3: First-domain validation

Validate bounded Home automation through Home Assistant, Telegram, and a local runtime. Include approval, failure modes, degraded operation, explicit capability allow-list, and domain-state boundaries.

## Phase 4: Production readiness

Threat model, capability governance, tool trust, audit and observability, backup and recovery, secrets, upgrade and rollback, regression testing, and operational documentation.

## Phase 5: Ecosystem expansion

Evaluate a second domain, cross-domain capabilities, Shared Context, memory strategy, collaborator lifecycle, registry need, and domain onboarding.

## Phase 6: Long-term evolution

Periodic architecture and principle reviews, glossary evolution, ADR supersession, dependency review, collaborator deprecation, memory governance, security review, and incubator review.

## Progress rule

Advance based on reduced uncertainty and evidence, not perceived feature completeness.
