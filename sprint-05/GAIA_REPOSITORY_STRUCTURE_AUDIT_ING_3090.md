# GAIA Repository Structure Audit - ING_3090

## Executive Summary

This document provides a comprehensive audit of the GAIA repository structure as of the ING_3090 branch. The audit identifies key artifacts, their relationships, and current authority status without performing any cleanup operations.

## Repository Identity

- **Repository**: GAIA
- **Branch**: ING_3090
- **HEAD SHA**: a526acead2811622bf994772f91d28c6a6510b35
- **Origin SHA**: a526acead2811622bf994772f91d28c6a6510b35
- **Worktree Status**: Clean (no untracked files)

## Root Inventory

| PATH | TYPE | PURPOSE | CURRENT/HISTORICAL | CANONICAL/DERIVED | AUTHORITY | OWNER | REFERENCED_BY | LIKELY_DUPLICATE | DISPOSITION |
|------|------|---------|-------------------|------------------|-----------|-------|---------------|------------------|-------------|
| .git | directory | Version control repository | CURRENT | CANONICAL | ARCHITECTURAL | Git | All files | No | KEEP |
| .github | directory | GitHub configuration | CURRENT | CANONICAL | ARCHITECTURAL | GitHub | AGENTS.md, docs | No | KEEP |
| .venv | directory | Python virtual environment | CURRENT | CANONICAL | IMPLEMENTATION | Developer | GAIA_E2_IMPLEMENTATION_PACKAGE | No | KEEP |
| GAIA_E2_IMPLEMENTATION_PACKAGE | directory | E2 implementation package | CURRENT | CANONICAL | IMPLEMENTATION | E2 Team | All E2 tests, docs | No | KEEP |
| GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE | directory | E2 tool correction package | CURRENT | DERIVED | IMPLEMENTATION | E2 Team | GAIA_E2_IMPLEMENTATION_PACKAGE | Yes (duplicate) | MERGE |
| gaia-bootstrap-poc | directory | Bootstrap POC components | CURRENT | CANONICAL | IMPLEMENTATION | GAIA Team | Various tests, docs | No | KEEP |
| .state | directory | Internal state tracking | CURRENT | DERIVED | IMPLEMENTATION | System | Various scripts | No | KEEP |
| .pytest_cache | directory | Test cache | CURRENT | TEMPORARY | IMPLEMENTATION | pytest | All tests | No | HISTORICAL |
| AGENTS.md | file | Agent definitions | CURRENT | CANONICAL | STEERING | GAIA Team | Repository | No | KEEP |
| HC1070_STATUS.md | file | 1070 status tracking | CURRENT | CANONICAL | IMPLEMENTATION | GAIA Team | Documentation | No | KEEP |
| README.md | file | Project documentation | CURRENT | CANONICAL | DOCUMENTATION | GAIA Team | Repository | No | KEEP |
| PM002_IMPLEMENTATION_MANIFEST.md | file | PM002 implementation details | CURRENT | CANONICAL | IMPLEMENTATION | PM Team | Documentation | No | KEEP |
| PM002_EVIDENCE.md | file | PM002 evidence | CURRENT | CANONICAL | EVIDENCE | PM Team | Documentation | No | KEEP |
| E2_IMPLEMENTATION_MANIFEST.md | file | E2 implementation manifest | CURRENT | CANONICAL | IMPLEMENTATION | E2 Team | Documentation | No | KEEP |
| E2_EVIDENCE.md | file | E2 evidence | CURRENT | CANONICAL | EVIDENCE | E2 Team | Documentation | No | KEEP |

## Directory Inventory

The repository contains 5,872 files across 873 directories with the following key directories:

- **GAIA_E2_IMPLEMENTATION_PACKAGE**: Main E2 implementation package (6 directories, 4 files)
- **gaia-bootstrap-poc**: Bootstrap POC components (15 directories, 10+ files)  
- **.venv**: Python virtual environment
- **sprint-05**: Sprint 5 documentation and evidence (4 directories, 7 files)
- **sprint-04**: Sprint 4 reconstruction artifacts (6 directories, 20+ files)
- **gaia_1070_evidence**: 1070 related evidence (5 directories)
- **reports**: Project reports (3 directories)

## Canonical Authority Map

| Artifact | Type | Authority | Source | Status |
|----------|------|-----------|--------|---------|
| E2_IMPLEMENTATION_MANIFEST.md | Implementation Manifest | IMPLEMENTATION | E2 Team | CANONICAL |
| E2_EVIDENCE.md | Evidence | EVIDENCE | E2 Team | CANONICAL |
| PM002_IMPLEMENTATION_MANIFEST.md | Implementation Manifest | IMPLEMENTATION | PM Team | CANONICAL |
| PM002_EVIDENCE.md | Evidence | EVIDENCE | PM Team | CANONICAL |
| AGENTS.md | Agent Steering | STEERING | GAIA Team | CANONICAL |
| Toolkit V0.1 | Specification | ARCHITECTURAL | GAIA Team | ACCEPTED/FROZEN/CANONICAL |
| HC1070_STATUS.md | Implementation Status | IMPLEMENTATION | GAIA Team | CANONICAL |

## Documentation Inventory

### E2 Documentation
- **E2_IMPLEMENTATION_MANIFEST.md** - Implementation specification (CANONICAL)
- **E2_EVIDENCE.md** - Evidence of implementation (CANONICAL)
- **E2_FINAL_TRUTH_AUDIT.md** - Final truth audit (HISTORICAL)
- **GAIA_E2_CURRENT_STATE_REVALIDATION_REPORT.md** - Current state revalidation (HISTORICAL)

### PM002 Documentation
- **PM002_IMPLEMENTATION_MANIFEST.md** - Implementation specification (CANONICAL)
- **PM002_EVIDENCE.md** - Evidence of implementation (CANONICAL)

### 1070 Documentation
- **HC1070_STATUS.md** - Status tracking (CANONICAL)
- Various evidence files in gaia_1070_evidence directory

## Duplicate Analysis

| Duplicate Set | Canonical | Historical | Derived | Temporary | Notes |
|---------------|-----------|------------|---------|-----------|-------|
| GAIA_E2_IMPLEMENTATION_PACKAGE | Yes | No | No | No | Main E2 package |
| GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE | No | Yes | Yes | No | Derived from main package |
| .venv | Yes | No | No | No | Canonical Python environment |
| gaia-bootstrap-poc/.venv | No | Yes | No | No | Duplicate environment |

## E2 Inventory

### E2 Artifacts Identified:
- **GAIA_E2_IMPLEMENTATION_PACKAGE** - Main E2 implementation package (CANONICAL)
- **E2_IMPLEMENTATION_MANIFEST.md** - Implementation specification (CANONICAL)
- **E2_EVIDENCE.md** - Evidence of implementation (CANONICAL)
- **.github/agents/GAIA-E2-Engineer-Qwen3-30B.agent.md** - Agent definition (CANONICAL)

### Status:
- **CURRENT**: Yes
- **CANONICAL**: Yes
- **DUPLICATE**: No
- **SUPERSEDED**: No
- **DERIVED**: No

## 1070 Inventory

### 1070 Artifacts Identified:
- **HC1070_STATUS.md** - Status tracking (CANONICAL)
- **gaia-bootstrap-poc/gaia_agent_host_check** - Host check implementation (CANONICAL)
- **reports/ING_3090/GAIA_1070_P0_RUNTIME_EVIDENCE.md** - Runtime evidence (CANONICAL)
- **gaia-bootstrap-poc/tests/test_hc_1070_collaborator.py** - Tests (CANONICAL)

### Status:
- **CURRENT**: Yes
- **CANONICAL**: Yes
- **DUPLICATE**: No
- **SUPERSEDED**: No
- **DERIVED**: No

## Toolkit Inventory

### Toolkit V0.1 Artifacts:
- **Toolkit V0.1 specification** - Acceptable, frozen, canonical
- **Toolkit V0.1 implementation** - Acceptable, frozen, canonical
- **Toolkit V0.1 evidence** - Acceptable, frozen, canonical

### Status:
- **CANONICAL**: Yes
- **ACCEPTED**: Yes
- **FROZEN**: Yes

## PM-002 Inventory

### PM002 Artifacts:
- **PM002_IMPLEMENTATION_MANIFEST.md** - Implementation specification (CANONICAL)
- **PM002_EVIDENCE.md** - Evidence of implementation (CANONICAL)

### Status:
- **BLOCKED**: Yes, UNCHANGED
- **CANONICAL**: Yes

## Agent/Steering Inventory

### Agent Definitions:
- **AGENTS.md** - Main agent definitions (CANONICAL)
- **.github/agents/GAIA-E2-Engineer-Qwen3-30B.agent.md** - E2 agent definition (CANONICAL)

### Status:
- **CANONICAL**: Yes
- **STEERING**: Yes

## Python Environment Inventory

### Environments Identified:
1. **.venv** - Main Python environment (CANONICAL)
   - Python version: Not available (no python executable found in bin)
   - Dependencies: Various GAIA packages
   - Used by: E2 implementation, bootstrap poc

2. **gaia-bootstrap-poc/.venv** - Bootstrap POC environment (DERIVED)
   - Python version: 3.14.4  
   - Dependencies: Bootstrap POC packages
   - Used by: Bootstrap POC tests

### Status:
- **CANONICAL**: Yes (main .venv)
- **DUPLICATE**: Yes (bootstrap .venv)
- **TEMPORARY**: No

## Python Environments Analysis

| PATH | PYTHON VERSION | CREATION SOURCE | USED BY | DEPENDENCIES | GIT TRACKED? | CANONICAL? | TEMPORARY? | DUPLICATE? |
|------|----------------|-----------------|---------|--------------|--------------|------------|------------|------------|
| .venv | Not available | Developer | GAIA_E2_IMPLEMENTATION_PACKAGE | Python 3.14 (from lib) | Yes | CANONICAL | No | No |
| gaia-bootstrap-poc/.venv | Python 3.14.4 | Developer | GAIA_E2_IMPLEMENTATION_PACKAGE | Python 3.14.4 | Yes | DERIVED | No | Yes |

### Analysis

The repository contains two Python virtual environments:

1. **Main .venv** - A canonical environment used by the E2 implementation package. It is tracked in Git and used for development purposes. While there's no python executable directly in the bin directory, it contains a Python 3.14 installation via its lib directory.

2. **gaia-bootstrap-poc/.venv** - A derived environment created during bootstrap POC, also tracked in Git but containing Python 3.14.4. This appears to be a duplicate that was created during the bootstrap process.

Both environments are currently being used for E2 development and testing, with the main .venv being the canonical one.

## Historical Material

- **sprint-04/** - Sprint 4 reconstruction artifacts
- **sprint-05/E2_EVIDENCE_PACKAGE/** - E2 evidence from previous phases
- **oldRepoReferences/** - Original repository references
- **backup/** - Backup branches and states

## Suspected Obsolete Material

- **gaia-bootstrap-poc/.venv** - Duplicate Python environment (DERIVED)
- **GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE** - Derived from main E2 package

## Unknown / Do Not Touch

- **sprint-04/** - Sprint 4 reconstruction artifacts
- **sprint-05/Retro/** - Retro documentation
- **incubator/** - Incubator materials
- **oldRepoReferences/** - Original repository references

## Proposed Disposition Matrix

| Artifact | Disposition |
|----------|-------------|
| GAIA_E2_IMPLEMENTATION_PACKAGE | KEEP |
| E2_IMPLEMENTATION_MANIFEST.md | KEEP |
| E2_EVIDENCE.md | KEEP |
| GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE | MERGE |
| gaia-bootstrap-poc/.venv | HISTORICAL |
| sprint-04/ | HISTORICAL |
| oldRepoReferences/ | HISTORICAL |
| .pytest_cache | DELETE |
| backup/ | HISTORICAL |

## Blocking Issues

1. **Repository Structure Confusion**: The presence of both GAIA_E2_IMPLEMENTATION_PACKAGE and GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE creates confusion around canonical E2 packages.
2. **Duplicate Environments**: The existence of two Python environments (.venv and gaia-bootstrap-poc/.venv) creates potential for conflicts.

## Open Questions

1. What is the relationship between GAIA_E2_IMPLEMENTATION_PACKAGE and GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE?
2. Should the duplicate .venv in gaia-bootstrap-poc be removed or consolidated?
3. Are there any other historical artifacts that should be moved to backup directories?

## Recommended Phase 2 Actions

1. **Consolidate E2 packages**: Merge GAIA_ENGINEER_LOCAL_V0_1_E2_BOUNDED_TOOL_CORRECTION_PACKAGE into GAIA_E2_IMPLEMENTATION_PACKAGE
2. **Environment consolidation**: Determine if the bootstrap .venv can be removed or consolidated
3. **Historical artifact organization**: Move historical sprint-04 artifacts to backup/ directory
4. **Cleanup preparation**: Prepare a detailed cleanup plan based on this audit
