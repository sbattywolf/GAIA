# ADR-0003: Capability Model

**Project:** GAIA  
**Document type:** Architecture Decision Record  
**Status:** Proposed  
**Version:** 0.1  
**Date:** 2026-08-03  
**Decision owner:** Human Owner  
**Phase:** Architecture Convergence

## 1. Decision summary

GAIA will represent a Capability as a small, implementation-neutral contract describing **what may be requested or performed** against an explicitly scoped Resource.

The initial Capability Model separates six concerns:

1. **Capability Definition:** what may be requested or performed;
2. **Resource Scope:** which Resource or Resource class may be targeted;
3. **Policy Result:** whether the request is allowed, denied, requires Approval, or cannot be determined;
4. **Approval Requirement:** whether Human Owner confirmation is required;
5. **Execution Binding:** which Adapter or Tool performs the work;
6. **Evidence:** the minimum diagnostic or Audit information required by risk.

For the first domestic slice, this model will be implemented with simple explicit records and rules. It does not require a Capability Registry, Policy engine, Workflow engine, Plugin system, or dynamic discovery.

## 2. Context

ADR-0001 establishes a minimal in-process Core that coordinates Requests, Context, Capability and Resource scope, required Policy and Approval outcomes, execution delegation, structured results, and minimal evidence.

The remaining question is how to describe a Capability without turning it into:

- an API endpoint;
- a Tool schema;
- a permission flag;
- a prompt instruction;
- an Approval Workflow;
- an execution implementation;
- an Audit history.

GAIA needs enough structure to prevent ambiguous or unauthorised action while remaining proportionate to a personal domestic project.

## 3. Decision drivers

- Capability describes **what**, never **how**.
- The first implementation must be small and direct.
- Read-only domestic value should reach production quickly.
- Resource ambiguity must not lead to consequential action.
- Policy, Approval, execution, and evidence must remain distinguishable.
- Home Assistant and model-provider details must stay outside the Capability Definition.
- One Human Owner must be able to inspect and understand the active Capability set.
- Future extension must not require a platform today.

## 4. Decision

### 4.1 Minimal Capability contract

The initial semantic contract contains only fields required by the first scenario:

| Element | Purpose | Required initially |
|---|---|---|
| Identifier | Stable name used by GAIA | Yes |
| Description | Human-readable statement of what it does | Yes |
| Resource scope | Allowed Resource type, set, or predicate | Yes |
| Operation kind | Read, propose, or act | Yes |
| Risk level | Simple risk classification used by Policy | Yes |
| Approval requirement | Whether explicit Human Owner confirmation is required | Yes |
| Input constraints | Minimum semantic constraints needed for a valid request | When needed |
| Output meaning | Meaning of success and relevant non-success outcomes | Yes |
| Version | Contract evolution reference | Yes |

This is a semantic checklist, not a mandatory class or serialisation schema.

### 4.2 Initial operation kinds

The first version uses three operation kinds:

- **Read:** observe or retrieve information without intentionally changing external state;
- **Propose:** prepare a possible change or decision without executing it;
- **Act:** intentionally change external state.

Do not add more kinds until a scenario demonstrates a distinct need.

### 4.3 Initial risk model

Use the smallest useful classification:

- **Low:** read-only operation with no meaningful side effect;
- **Moderate:** reversible domestic action with bounded scope;
- **High:** irreversible, safety-sensitive, security-sensitive, privacy-sensitive, or financially meaningful action.

Risk classification guides Policy and Approval but does not replace them.

### 4.4 Resource scope

Every Capability request must identify a Resource or an explicitly bounded Resource set.

Execution is not permitted when:

- the Resource cannot be resolved sufficiently;
- multiple plausible Resources remain for a consequential action;
- the Resource lies outside the Capability scope;
- required source information is unavailable or stale beyond the Domain rule.

A read-only query may return partial or uncertain information if that uncertainty is explicit.

### 4.5 Policy Result

The initial Policy Result is one of:

- `Allowed`;
- `Denied`;
- `ApprovalRequired`;
- `Indeterminate`.

`Indeterminate` does not permit execution.

Policy evaluation may initially be a small deterministic function or explicit rule set. A general Policy engine is not required.

### 4.6 Approval

Approval is separate from Capability Definition and Policy evaluation.

For the first slice:

- low-risk read operations normally require no Approval;
- moderate actions may require Approval based on the explicit rule;
- high-risk actions require explicit Human Owner Approval or remain unsupported;
- silence or timeout is not Approval;
- Approval applies only to the identified request, Capability, Resource scope, and relevant parameters.

A general Approval Workflow is not required.

### 4.7 Execution Binding

Execution Binding maps an accepted Capability request to an Adapter or Tool implementation.

It remains outside the Capability Definition so that Home Assistant, Telegram, model runtime, or another provider can be replaced without redefining what the Capability means.

One direct binding per initial Capability is acceptable. Dynamic provider selection is deferred.

### 4.8 Result semantics

The Capability outcome must distinguish at least:

- success;
- denied;
- Approval required;
- clarification required;
- Resource ambiguous;
- source unavailable;
- information stale or insufficient;
- execution failure;
- unsupported.

A model-generated natural-language response may explain the result, but it must not redefine the underlying outcome.

### 4.9 Evidence

Evidence is proportional to risk.

For the initial read-only scenario, retain only what is needed to diagnose behaviour:

- correlation reference;
- Capability identifier and version;
- target Resource references;
- Policy Result;
- Approval result when applicable;
- outcome and material failure reason.

Do not build an enterprise Audit platform.

## 5. First production Capability

The recommended first Capability is conceptually:

```text
Read current opening state for a bounded set of home entry Resources.
```

It should:

- be read-only;
- accept an explicit or resolvable Resource scope;
- rely on Home Assistant as Authoritative Source for selected reported state;
- expose stale, unavailable, or ambiguous information;
- avoid Approval when risk is low;
- not contain Home Assistant entity IDs in its semantic definition;
- return structured outcome before channel-specific formatting.

The exact identifier and implementation schema belong to the prototype.

## 6. Explicit exclusions

The initial Capability Model does not include:

- dynamic Capability discovery;
- central Registry;
- Plugin packaging;
- Workflow composition;
- Capability marketplace;
- delegation chains;
- autonomous Capability creation;
- model-generated permissions;
- generic condition language;
- complex role-based access control;
- multi-user grants;
- provider selection;
- persistence platform;
- universal taxonomy.

## 7. Alternatives considered

### A. Treat Tools as Capabilities

**Benefit:** minimal modelling.  
**Problem:** couples semantic intent to implementation and provider schemas.  
**Decision:** rejected.

### B. Put Policy, Approval, and execution inside Capability

**Benefit:** one object contains everything.  
**Problem:** creates an overloaded contract that is difficult to replace and test.  
**Decision:** rejected.

### C. Build a full Capability Registry and Policy platform

**Benefit:** dynamic extensibility and central governance.  
**Problem:** disproportionate to one Human Owner and the first domestic scenario.  
**Decision:** rejected for now.

### D. Minimal separated contract

**Benefit:** explicit safety boundaries, direct implementation, and future replaceability.  
**Cost:** some mappings and rules remain manual initially.  
**Decision:** selected.

## 8. Consequences

### Positive

- Capabilities remain stable when Tools or providers change.
- Policy and Approval can evolve independently.
- Resource scope becomes explicit before execution.
- The first implementation can use simple records and deterministic rules.
- Read-only value can reach production without a governance platform.
- Failure semantics remain visible beneath natural-language responses.

### Negative

- Initial Capability definitions and bindings may be configured manually.
- Additional operation kinds or risk levels may be needed later.
- A second Domain may expose missing common fields.
- Contract versioning requires discipline.

### Risks and mitigation

| Risk | Mitigation |
|---|---|
| Capability explosion | Create only Capabilities required by validated scenarios. |
| Vague Resource scope | Refuse consequential execution until scope is explicit. |
| Risk labels become subjective | Keep three levels and document concrete Domain examples. |
| Approval becomes annoying | Require it only when risk justifies it. |
| Tool schema leaks into contract | Translate at Execution Binding. |
| Model bypasses Policy | Core enforcement from ADR-0001 remains mandatory. |
| Manual mapping becomes permanent | Review after two active Domains. |

## 9. Validation plan

Validate with the first read-only Home scenario:

1. define one read Capability;
2. bind it directly to the Home Assistant Adapter;
3. demonstrate Resource scope without exposing provider identifiers in the semantic contract;
4. return `Indeterminate` or a non-success outcome for ambiguity or insufficient source information;
5. verify that execution cannot bypass Policy Result;
6. render the same structured outcome through another channel formatter;
7. test deterministic Policy, Resource scope, and result mapping;
8. record only minimal evidence.

## 10. Review triggers

Review this ADR when:

- two production Domains are active;
- more than one implementation serves the same Capability;
- Capability discovery becomes necessary;
- Policy rules become difficult to express with explicit deterministic rules;
- users other than the Human Owner are introduced;
- high-risk actions are enabled;
- Capability composition or long-running execution becomes necessary;
- manual mapping creates material maintenance cost.

Compatible clarifications may amend this ADR. A materially different contract should supersede it.

## 11. Documentation impact

If accepted, update:

- `GAIA_MODEL_v0.2.md` with the accepted Capability responsibility;
- `GLOSSARY_v0.2.md` with accepted separation and result terminology;
- `ARCHITECTURE_CONVERGENCE_v0.2.md` to mark ADR-0003 accepted;
- `NEXT_STEPS_v0.2.md` to complete the minimum pre-prototype ADR set;
- prototype documentation with the first concrete Capability definition.

No immediate change is required to `WORLD_MODEL_v0.2.md` or `CONTEXT_MODEL_v0.2.md`.

## 12. Relationship with ADR-0001

ADR-0001 assigns the Core responsibility for enforcing required Policy and Approval outcomes and delegating execution.

This ADR defines the semantic pieces that the Core coordinates. It does not add a Capability platform to the Core.

## 13. Acceptance checklist

Before changing status to `Accepted`, confirm:

- Capability still describes what, not how;
- Resource scope is mandatory before consequential execution;
- Policy, Approval, Execution Binding, and Evidence remain separate;
- the first read-only scenario can use one simple contract and one direct binding;
- no Registry, Plugin system, Workflow engine, or Policy platform is required;
- failure outcomes are explicit;
- the model remains understandable and operable by one Human Owner;
- the design can be reviewed after two active Domains.

## 14. Final decision statement

GAIA will use a small Capability contract that defines what may be requested, against which Resource scope, with explicit risk and Approval requirements.

Policy evaluation, Approval, execution binding, and evidence remain separate, simple, and proportionate to the current domestic scenario.

**A Capability defines intent and boundaries. It does not become the implementation.**
