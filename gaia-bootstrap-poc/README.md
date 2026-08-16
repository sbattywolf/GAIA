# GAIA Bootstrap POC

Minimal, deterministic implementation of the Home read-only slice.

## Scope

- resolve one bounded Home resource label;
- read one opening-state observation through `OpeningStateProvider`;
- return a structured outcome;
- use only explicit in-process wiring and a fake adapter.

## Explicitly absent

Real Home Assistant communication, Telegram, batch reads, Memory, Registry,
Planner, Event Bus, plugin system, provider selection, distributed coordination,
and persistence.

## Run

```bash
python -m pytest
```

## Replacement seam

Replace `FakeHomeAssistantAdapter` with another `OpeningStateProvider`.
`RequestRouter`, `HomeResourceResolver`, `ReadOpeningStateCapability`, and
outcomes must remain unchanged.
