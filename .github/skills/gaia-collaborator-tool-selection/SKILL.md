---
name: gaia-collaborator-tool-selection
description: Select the minimum appropriate GAIA tool for an understood collaborator intent.
---

# GAIA Collaborator Tool Selection

## Purpose

Select the smallest tool capability required to satisfy the user's intent.

## Rules

- Select tools only after intent is understood.
- Prefer the minimum sufficient tool set.
- Do not call tools speculatively.
- Do not call a tool merely to obtain information that is already available in context.
- Never invent a tool.
- Respect GAIA architectural boundaries.
- Do not bypass an adapter or boundary to reach an external system directly.
- A read operation must not become a state-changing operation.
- If the available tools cannot safely satisfy the request, stop and report the limitation.

## Safety

Before a state-changing operation verify:

1. target is identified;
2. required parameters are known;
3. requested operation matches the user's intent;
4. no unresolved ambiguity affects the action.

## Output

Select:

- tool
- arguments
- reason for selection
- whether confirmation is required
