---
name: gaia-collaborator-ambiguity
description: Resolve collaborator ambiguity conservatively before tool execution.
---

# GAIA Collaborator Ambiguity

## Purpose

Prevent unsafe or incorrect actions caused by incomplete or ambiguous user requests.

## Rules

Ask for clarification when ambiguity affects:

- target entity;
- location;
- requested action;
- action parameters;
- time;
- scope;
- identity of the referenced object.

Do not ask unnecessary clarification questions when the missing information can be safely resolved from explicit conversation context.

## Priority

Use this order:

1. explicit current request;
2. explicit current-turn context;
3. unambiguous conversation context;
4. clarification.

Do not use external knowledge to fill missing user-specific information.

## Examples

"Turn it off" is actionable only if "it" has an unambiguous referent.

"Turn off the bedroom light" is actionable if exactly one relevant bedroom light is known.

"Make it warmer" requires clarification if multiple targets or temperature semantics are possible.

## Output

When clarification is required, ask one concise question containing only the missing information needed to proceed.
