# GAIA Glossary and Model Reconciliation v0.2

## Files

- `GLOSSARY_v0.2.md`
- `GAIA_MODEL_v0.2.md`

## Change classification

**Type:** Substantial but compatible semantic reconciliation.  
**Status:** Proposed.  
**Previous versions:** Preserve `GLOSSARY_v0.1.md` and `GAIA_MODEL_v0.1.md` unchanged until review.  
**ADR impact:** No new ADR. Open decisions are explicitly deferred to existing ADR candidates.

## Principal reconciliation

- Memory is no longer presented as an established Domain.
- World Model remains a semantic foundation, not a component or first-class model element.
- Context terms are classified as three primary scopes and two bounded views.
- Resource receives a clearer identity boundary; Resource Reference remains supporting semantics.
- Observation is a source-grounded kind of Assertion.
- Human Owner, Steward, Authoritative Source, and Domain Responsibility remove ambiguity from generic `owner` terminology.
- Capability is separated from Resource scope, Policy, Approval, execution binding, and Audit evidence.
- The Core/Policy question remains open for ADR-0001 rather than being silently decided.
- The official GAIA Model remains exactly seven first-class concepts.

## Saving

Save both files under `GAIA/reference/`. Do not delete or overwrite the v0.1 versions yet.
