# Architecture and decisions

## Core rule

```text
Deterministic Python -> Home Assistant -> LLM only when required
```

## Semantic control model

```text
Human intent -> Area -> Capability -> Canonical target -> Home Assistant service
```

Do not equate `lighting` with `domain=light`. In this home, physical lighting may be controlled by wall switches, smart bulbs, groups, scripts or automations.

## Important implementation boundaries

- Parser understands requests.
- Resolver produces pure query plans and performs no network calls.
- Aggregate service fetches one immutable Home Assistant state snapshot and filters locally.
- Formatter only creates user-facing text.
- Inventory provider will join runtime state with entity, device, area, alias and label metadata.
- Home Assistant remains authoritative.
- Do not invent entity IDs.

## Smart-bulb exceptions

Corridoio, ingresso and two spot lights require special treatment because wall switches and smart bulbs interact with existing automations. Do not mark both relay and smart bulb as unrestricted canonical targets until the desired control policy is documented.

## 1070/3090 boundary

The 1070 is for reliable real-time edge behaviour. The 3090 is for heavier coding and engineering tasks. The 1070 must continue operating when the 3090 and QNAP are off.
