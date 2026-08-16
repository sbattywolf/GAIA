# World Model Review

## Question

What must GAIA know about itself, the user, domains and resources without creating an unbounded “world model”?

## Layers

- stable identity and principles;
- explicit resource inventory;
- current runtime state;
- scoped shared context;
- intentional long-term memory;
- provenance and confidence;
- domain-specific semantic models.

## Findings

A single world-state object is attractive but dangerous. It mixes facts, observations, preferences, inferences and transient state. GAIA should preserve provenance and scope, separate current state from memory and avoid turning Shared Context into a universal database.

## Open questions

How are stale facts identified? Which layer owns correction? Can a collaborator rely on inferred preferences? How are contradictions represented? What can be forgotten without breaking audit?
