# Memory Role Validation

**Project:** GAIA  
**Document type:** Validation Brief  
**Status:** Planned  
**Version:** 0.1  
**Phase:** Architecture Convergence  
**Date:** 2026-08-03  
**Validation owner:** Human Owner

## 1. Purpose

This brief defines the minimum evidence needed before deciding the architectural role of Memory in GAIA.

Memory is intentionally not yet part of the official first-class GAIA Model and is not treated as an established Domain. The project will not build a general Memory subsystem before a real domestic scenario demonstrates a retention need.

The objective is not to design perfect long-term personal memory. The objective is to determine whether the first useful production slice needs any information to survive beyond its original Context, and if so, why.

## 2. Validation question

> What information, if any, must GAIA intentionally retain across interactions to provide useful domestic continuity that cannot be provided adequately by the authoritative source, configuration, or temporary operational Context?

## 3. Current hypotheses

The validation starts with four competing hypotheses.

### H1: No GAIA Memory is required for the first slice

Home Assistant remains authoritative for selected home state. Static Resource mappings can be configuration. Request and Interaction Context can remain temporary.

### H2: Only explicit Human Owner preferences require retention

GAIA may need to retain selected preferences, aliases, or corrections that are not authoritative external state and that the Human Owner expects to persist.

### H3: Domain-specific retained knowledge is required

The Home Domain may need selected durable mappings or corrections beyond simple configuration, but this does not necessarily justify a general Memory subsystem.

### H4: A shared Memory concern is required

Multiple Collaborators or Domains may eventually need common retention, correction, inspection, and forgetting semantics. This hypothesis requires evidence from more than one active Domain and is not assumed for the first slice.

## 4. Scope

This validation covers only information relevant to the first domestic production slice and nearby follow-up interactions.

Candidate examples include:

- user-defined aliases for Resources;
- corrections to Resource resolution;
- preferences for response or notification behaviour;
- explicit choices that should apply to later interactions;
- continuity across restart or channel interruption;
- information already owned by Home Assistant or configuration.

## 5. Out of scope

This brief does not design:

- long-term conversation memory;
- personal Knowledge Graph;
- vector retrieval;
- embeddings;
- semantic search platform;
- autonomous learning;
- model training;
- cross-Domain Memory;
- Memory service or database;
- retention schedules for all future data;
- a general forgetting engine;
- psychological or human-like memory simulation.

## 6. Required distinctions

Every candidate retained item must be classified before it is called Memory.

| Concern | Question |
|---|---|
| Authoritative source | Is the information already owned by Home Assistant or another source? |
| Configuration | Is it an explicit stable setting that should be versioned or edited directly? |
| Context | Is it needed only for the current Request or Interaction? |
| Operational persistence | Must temporary Context survive restart without being reused later? |
| Knowledge | Is it reusable reference information rather than personal continuity? |
| Memory candidate | Is intentional retention across interactions required for user value? |
| Audit | Must it be retained as evidence of a consequential decision or action? |

The same underlying information may be referenced by several concerns, but each concern retains a distinct responsibility.

## 7. Minimal validation scenarios

### Scenario A: Resource alias

The Human Owner says that “the kitchen window” refers to a specific home Resource.

Questions:

- Can this remain explicit configuration?
- Is correction required through conversation?
- Should the alias apply to future interactions?
- Must the Human Owner be able to inspect and delete it?

### Scenario B: Temporary clarification

GAIA asks which of two similar windows the Human Owner meant, and the answer is needed only to complete the current Request.

Expected default:

- keep it in Request or Interaction Context;
- do not retain it as Memory automatically.

### Scenario C: Persistent preference

The Human Owner explicitly asks GAIA always to use a certain label or response preference.

Questions:

- is the request explicit enough to retain?
- where can the preference be inspected and corrected?
- what happens when the preference conflicts with a Domain source?

### Scenario D: Restart continuity

An Interaction is interrupted by restart before completion.

Expected distinction:

- operational persistence may preserve temporary Context;
- survival across restart does not automatically make it long-term Memory.

### Scenario E: External state

Home Assistant reports that a window is open.

Expected default:

- treat Home Assistant as the Authoritative Source for the selected reported state;
- do not copy current device state into long-term GAIA Memory merely for convenience.

## 8. Evidence to capture

For each scenario, record:

- information involved;
- original source;
- purpose of retention;
- expected lifetime;
- who may inspect it;
- who may correct it;
- who may delete it;
- whether it survives restart;
- whether it is reused in a later Interaction;
- whether configuration or source lookup is simpler;
- failure behaviour when the information is unavailable or stale;
- actual benefit to the Human Owner.

A simple Markdown table is sufficient. No Memory platform is required for the validation.

## 9. Decision rules

A candidate should be retained as Memory only when all applicable conditions hold:

1. reuse across interactions provides clear domestic value;
2. the authoritative source or explicit configuration is not the better owner;
3. the retention purpose is understandable;
4. the Human Owner can inspect and correct it;
5. the Human Owner can remove it;
6. provenance is sufficient;
7. retention does not silently expand Capability authority;
8. the implementation cost is proportionate to the value.

If these conditions are not met, do not retain the item as Memory.

## 10. Smallest acceptable implementation

If the first slice validates a Memory need, begin with the smallest direct mechanism that satisfies it.

Possible forms include:

- a small human-readable configuration file for explicit aliases or preferences;
- a simple local structured record with inspection and deletion support;
- an existing authoritative system when it already owns the information.

This brief does not select a storage format or technology.

Do not introduce a vector store, graph database, Memory service, background consolidation process, or general retention framework unless later evidence demonstrates a need.

## 11. Success criteria

The validation is complete when:

- each initial scenario has recorded evidence;
- configuration, Context, operational persistence, Knowledge, Memory, and Audit are distinguishable in practice;
- at least one real retention need is confirmed, or the first slice demonstrates that no GAIA Memory is yet required;
- correction and deletion expectations are clear for retained items;
- the result is sufficient to accept, defer, narrow, or reject `ADR-0002-Memory-Semantics.md`.

“No Memory required yet” is a valid successful outcome.

## 12. Stop conditions

Stop and simplify if the validation begins to require:

- a general Memory API;
- multiple storage engines;
- embeddings or vector search;
- background summarisation;
- autonomous retention decisions;
- cross-Domain ontology;
- complex privacy classification;
- migration infrastructure.

Those concerns belong to future validation, not the first domestic production slice.

## 13. Expected outputs

The validation should produce:

1. a short evidence table for the scenarios;
2. a recommendation selecting one of the current hypotheses;
3. a list of information that must not be retained;
4. the minimum correction and deletion behaviour;
5. a recommendation for `ADR-0002`: create, defer, or narrow.

## 14. Review trigger

Review the Memory role again when:

- two production Domains are active;
- repeated cross-interaction preferences become valuable;
- different Collaborators require shared retained information;
- retained information causes incorrect behaviour;
- inspection, correction, or deletion becomes difficult;
- the Human Owner no longer understands what GAIA retains and why.

## 15. Current recommendation

Proceed with the first read-only Home scenario without a general Memory subsystem.

Use authoritative source lookup, explicit configuration, and temporary Context first. Record any real continuity gap encountered during use. Promote only the smallest validated retention need.

**Memory should be earned by demonstrated continuity value, not assumed from the start.**
