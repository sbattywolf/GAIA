# Repository Structure

> Recovery status: Recovered in substance and conservatively normalised  
> Source basis: surviving Microsoft 365 GAIA reference artefacts and conversation history  
> Confidence: High  
> Preservation rule: This file retains its original role. Reconstructed passages are not presented as verbatim recovery.

## Purpose

The repository preserves clarity, discoverability, architectural traceability, history and long-term maintainability. Stable working truth is separated from chronological research and from future decisions.

## Structure

```text
reference/   current working truth
sprint-01/   chronological research and critique
sprint-02/   stress testing and synthesis
adr/         explicit architecture decisions
incubator/   unapproved ideas
assets/      diagrams and reusable figures
reports/     reconstruction and audit records
prompts/     bounded restart prompts
```

## Rules

1. Documentation precedes large implementation commitments.
2. Sprint material is never rewritten to make later decisions look inevitable.
3. Reference documents may evolve, but must not erase critique or open questions.
4. Decisions become ADRs; unresolved ideas stay in Sprint material or the incubator.
5. Diagrams are stored both as Mermaid source and rendered PNG where Word/PDF compatibility matters.
6. Every replacement pack includes a manifest and checksums.
