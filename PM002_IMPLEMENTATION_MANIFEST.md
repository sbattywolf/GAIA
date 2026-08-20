# PM-002 Implementation Manifest

**Baseline:** `f01a13a8fd6258f0f568b1ceecea82c9b8a62aa8`
**Implementation status:** ENGINEER PACKAGE PREPARED
**Repository writes:** NONE
**Commit:** NONE
**Push:** NONE
**PR:** NONE

## Added files

```text
gaia-bootstrap-poc/scripts/pm002_start.sh
gaia-bootstrap-poc/scripts/pm002_stop.sh
gaia-bootstrap-poc/scripts/pm002_rollback.sh
gaia-bootstrap-poc/deployment/config/pm002.env.example
gaia-bootstrap-poc/tests/test_pm002_production_slice.py
gaia-bootstrap-poc/tests/test_pm002_operational.py
PM002_EVIDENCE.md
PM002_IMPLEMENTATION_MANIFEST.md
```

## Architectural source changes

```text
NONE
```

The W3 semantic production path is intentionally unchanged.

## Protected areas

```text
adr/ADR-0001-Core-Boundary.md
adr/ADR-0003-Capability-Model_Accepted.md
gaia-bootstrap-poc/src/gaia/core/**
gaia-bootstrap-poc/src/gaia/home/**
gaia-bootstrap-poc/src/gaia/adapters/**
gaia-bootstrap-poc/src/gaia/w3.py
gaia-bootstrap-poc/deployment/config/models.yaml
All Proposed v0.2 reference documents
PM-001 evidence/manifests
```

## Contracts preserved

- exactly one Resource: `home.light.living_room`;
- Home Assistant reference: `light.living_room`;
- operation: `Read Current Resource State`;
- read-only external execution;
- Policy/Approval gate remains upstream of the Home Collaborator;
- explicit ON/OFF/UNAVAILABLE/STALE Light semantics;
- no new Capability, Resource, Provider framework, Registry, Planner, Memory, Event Bus, Workflow, Plugin or write architecture.

## Engineer validation

Run from the package root with the reconstructed bounded test environment:

```text
PYTHONPATH=gaia-bootstrap-poc/src python3 -m pytest -q gaia-bootstrap-poc/tests/test_pm002_production_slice.py gaia-bootstrap-poc/tests/test_pm002_operational.py
```

Human Owner must additionally run the repository's authoritative W3 and PM-001 regression commands from the actual checkout.

## Human Owner validation

Not executed by Engineer.

## Governance

Engineer is not authorized to commit, push, merge or create/merge a PR under the current authorization. The package is delivered for application to the Human Owner's authoritative local checkout and subsequent Architect review.
