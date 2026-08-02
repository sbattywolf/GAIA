# GAIA Idea Incubator

- **Version:** 0.1
- **Status:** Idea-only
- **Decision authority:** None

## Purpose

The incubator preserves potentially useful ideas without treating them as roadmap commitments, architectural decisions, or implementation priorities. Its purpose is to protect the Core and the active roadmap from speculative complexity while keeping ideas discoverable.

## Entry rules

An idea may enter the incubator when:

- it is relevant to GAIA's identity or future evolution;
- the problem is not yet validated;
- the correct boundary or owner is uncertain;
- implementation would be premature;
- losing the idea would reduce future context.

An incubator item must not be described as approved, planned, or required.

## Promotion criteria

An item may leave the incubator only when:

1. it addresses a validated problem;
2. evidence shows why existing concepts are insufficient;
3. its responsibility and boundary can be stated clearly;
4. an owner and lifecycle are identifiable;
5. complexity and dependency costs are justified;
6. it does not duplicate an existing capability or document;
7. it can be moved into a validation brief, ADR candidate, or approved implementation milestone.

## Idea register

### Memory Inspector

**Intent:** allow the owner to inspect, correct, remove, and export retained memory.  
**Open question:** is this a product capability, an administrative tool, or part of the memory subsystem?  
**Promotion trigger:** memory semantics and retention policies are defined.

### Capability Simulator

**Intent:** evaluate capability, resource, policy, and approval rules without executing real actions.  
**Open question:** does a simulator reduce risk enough to justify a separate component?  
**Promotion trigger:** the first-domain capability model exists.

### Planner Red-Team Exercise

**Intent:** test whether implicit or explicit planning exceeds user intent or creates unsafe sequences.  
**Open question:** is Planner a first-class concept or simply behaviour within a run?  
**Promotion trigger:** representative multi-step tasks exist.

### MCP Kill-Switch Test

**Intent:** prove that an MCP integration can be removed or disabled without changing GAIA's identity or corrupting state.  
**Open question:** which MCP dependency is important enough to test?  
**Promotion trigger:** an MCP-based adapter enters a validation prototype.

### Event Chaos Testing

**Intent:** test missing, duplicated, delayed, reordered, or conflicting external events.  
**Open question:** does GAIA require first-class event semantics?  
**Promotion trigger:** multiple event-producing adapters exist.

### Research Collaborator

**Intent:** create a bounded collaborator for source discovery, comparison, and evidence tracking.  
**Open question:** how are provenance, freshness, and personal versus enterprise sources separated?  
**Promotion trigger:** a repeatable research workflow is defined.

### Voice Domain

**Intent:** explore voice as an additional interaction domain or channel.  
**Open question:** is voice a channel adapter, a domain, or both?  
**Promotion trigger:** communication state is independent of Telegram.

### Auto-Generated Domains

**Intent:** derive domain scaffolding from declarative contracts.  
**Open question:** would generation reduce effort or hide architecture and increase drift?  
**Promotion trigger:** at least two manually validated domains exist.

### Local Runtime Scorecard

**Intent:** compare local runtimes and models on GAIA-specific scenarios.  
**Open question:** which quality, latency, memory, tool-use, and operational metrics matter?  
**Promotion trigger:** the local runtime validation brief defines acceptance criteria.

### Home Assistant Replay Sandbox

**Intent:** replay Home domain events and actions without affecting the live household.  
**Open question:** can existing Home Assistant tooling provide sufficient isolation?  
**Promotion trigger:** failure and regression testing require repeatable domain traces.

### Collaborator Version Diff

**Intent:** show semantic changes in collaborator responsibility, capabilities, prompts, policies, and dependencies.  
**Open question:** what constitutes the versioned definition of a collaborator?  
**Promotion trigger:** collaborator lifecycle is formalised.

### Boundary Violation Detector

**Intent:** identify framework types, channel state, or domain-specific logic leaking into the Core.  
**Open question:** can ordinary architecture tests and dependency rules solve this more simply?  
**Promotion trigger:** implementation boundaries exist.

### Personal Knowledge Provenance Viewer

**Intent:** show where knowledge came from, when it was obtained, and whether it remains valid.  
**Open question:** how does knowledge differ from memory and source artefacts?  
**Promotion trigger:** knowledge and memory semantics are separated.

### Long-Term Memory Review Assistant

**Intent:** periodically propose corrections, expiry, consolidation, or deletion of retained memory.  
**Open question:** how can recommendations avoid autonomous retention decisions?  
**Promotion trigger:** memory governance and approval rules are defined.

## Rejected or deferred ideas

Record rejected ideas here only when preserving the reason prevents repeated discussion. Include:

- idea;
- disposition date;
- reason;
- evidence or ADR reference;
- condition under which reconsideration would be justified.

## Review cadence

Review the incubator at phase boundaries or when new evidence directly affects an item. Do not promote ideas merely because they have remained in the file for a long time.
