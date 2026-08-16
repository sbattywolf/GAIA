---
name: gaia-collaborator-intent
description: Interpret GAIA collaborator requests and identify the intended operation without inventing missing context.
---

# GAIA Collaborator Intent

## Purpose

Identify what the user is asking GAIA to accomplish before selecting tools or executing actions.

## Rules

- Interpret the user's request using the current conversation context.
- Prefer explicit user intent over inferred intent.
- Do not invent entities, devices, locations, parameters, or permissions.
- Distinguish information requests from action requests.
- Distinguish read operations from state-changing operations.
- Preserve relevant context across turns.
- If the intent is sufficiently clear, continue to tool selection.
- If a required parameter is missing and cannot be safely inferred, use ambiguity resolution.
- Do not execute an action merely because a similar action was discussed previously.

## Output

Produce an internal intent representation containing:

- operation
- target
- parameters
- required context
- whether the request is actionable
- unresolved ambiguity, if any
