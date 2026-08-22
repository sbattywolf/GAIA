# GAIA — Senior Engineer P1→P10 Dependency Analysis

## Purpose

Independent dependency review of the ING_3090 physical-validation path.

## Gate model

| Phase | Dependency | Review status |
|---|---|---|
| P1 | host/preflight evidence | executable, physical proof required |
| P2 | runtime/container readiness | endpoint ownership must be explicit |
| P3 | hardware/runtime evidence | physical evidence required |
| P4 | model/runtime inventory | runtime evidence required |
| P5 | validation preparation | dependency-aware |
| P6 | model inventory/evidence generation | fixed in ING_3090 |
| P7 | physical model validation | pending real hardware execution |
| P8 | inference/behaviour evidence | pending |
| P9 | consolidated evidence | pending |
| P10 | final physical gate | pending |

## Key dependency rule

A later phase must never manufacture success when a required earlier physical dependency is unavailable.

Required distinction:

- `PASS` = observed and gate conditions satisfied;
- `FAIL` = observed and gate condition failed;
- `BLOCKED` = prerequisite unavailable;
- `UNKNOWN` = insufficient evidence.

## Main dependency risks

1. Runtime endpoint mismatch can invalidate model/runtime evidence.
2. Empty inventory must not equal unavailable inventory.
3. Historical model names must not be used as current observations.
4. A generated evidence file is not itself proof of physical execution.
5. P7–P10 cannot be marked complete from static repository inspection.

## Required closure evidence

Before the physical gate is frozen, collect:

- target host identity;
- GPU identity and VRAM;
- Docker/runtime state;
- Ollama endpoint actually used;
- actual model inventory from runtime;
- model pull/load state;
- real inference execution;
- latency/resource observations;
- failure/blocked states where applicable;
- final consolidated evidence;
- immutable run timestamp and commit reference.

## Review conclusion

The dependency-aware direction introduced by ING_3090 is correct in principle. The remaining work is to make the dependency states executable and evidentially unambiguous, then run the complete sequence on the actual 1070.
