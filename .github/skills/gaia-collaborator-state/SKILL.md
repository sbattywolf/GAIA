---
name: gaia-collaborator-state
description: Preserve and use relevant conversational state for GAIA collaborator multi-turn requests.
---

# GAIA Collaborator State

## Purpose

Maintain continuity across related collaborator turns without inventing state.

## Rules

- Preserve explicitly established entities and parameters.
- Resolve pronouns and references using recent unambiguous context.
- Do not silently change the active target.
- Do not carry state across unrelated requests without evidence.
- Distinguish conversation state from external system state.
- External state must be obtained from the appropriate tool when current state matters.
- Never assume that a previous action succeeded merely because it was requested.

## State Categories

Track separately:

- user intent
- referenced entity
- requested action
- known parameters
- tool-observed state
- action result
- unresolved ambiguity

## Rule

Conversation memory is not proof of current external state.
