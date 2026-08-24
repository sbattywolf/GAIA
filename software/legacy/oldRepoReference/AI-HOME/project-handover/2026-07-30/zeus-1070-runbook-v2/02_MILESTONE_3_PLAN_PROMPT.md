# Next agent prompt: Milestone 3

You are continuing Zeus Edge after Milestones 1 and 2.

## Confirmed status

- Deterministic fast path works.
- Semantic formatter works.
- Aggregate counts and home report work.
- 34 unit tests passed.
- One `get_states()` snapshot is used per aggregate/report request.
- Home Assistant runs separately on Raspberry Pi 4.
- Zeus Edge runs on Ubuntu GTX 1070 under `zeus-edge.service`.
- Never start a second `telegram_agent.py` while systemd is active.

## Invariants

1. Preserve Milestones 1 and 2.
2. Do not change action behaviour in this milestone.
3. No Home Assistant writes.
4. Do not invent registry commands. Verify them against the installed Home Assistant version.
5. Do not assume labels propagate from area/device to entity.
6. Do not log tokens or sensitive Home Assistant attributes.
7. Make small reversible changes with unittest coverage.
8. Do not commit, push, reset or clean automatically.

## Task

Plan Milestone 3 only: a read-only Home Assistant Inventory Provider.

The plan must cover:

- runtime `/api/states` preservation;
- minimal WebSocket authentication and command correlation;
- read-only Entity, Device and Area Registry retrieval;
- alias retrieval;
- label retrieval only if verified supported;
- explicit metadata join rules;
- `InventoryEntity` contract;
- in-memory TTL cache and forced refresh;
- reconnect, timeout and partial-failure strategy;
- redacted snapshot export;
- synthetic fixtures and contract tests;
- no Telegram integration in the first implementation tranche;
- no semantic-control actions;
- no MCP, QNAP, Redis, PostgreSQL or 3090 runtime dependency.

First inspect the real repository and installed Home Assistant version. Produce a plan only. Do not modify files until the plan is approved.
