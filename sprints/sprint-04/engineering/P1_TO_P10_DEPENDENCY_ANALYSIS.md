# P1→P10 DEPENDENCY ANALYSIS

## EXECUTIVE SUMMARY

This document presents the dependency analysis for the GAIA 1070 physical validation process. Following the new dependency-aware validation loop approach, this analysis identifies which phases can execute independently, which are blocked by failures, and how evidence collection should proceed when failures occur.

## PARENT/CHILD DEPENDENCY MATRIX

| Phase | Parent | Child | Dependency | Can run if parent fails? | Evidence | Priority |
|-------|--------|-------|------------|--------------------------|----------|----------|
| P1 | - | P2, P3, P5 | Hardware detection requires runtime foundation | No | Hardware info | P0 |
| P2 | P1 | P4 | System configuration depends on hardware detection | No | Configuration | P0 |
| P3 | P1 | P6 | Filesystem checks depend on hardware profile | No | Filesystem status | P0 |
| P4 | P2 | P7 | Runtime checks depend on configuration | No | Runtime state | P0 |
| P5 | - | P4, P6 | Docker foundation is prerequisite for runtime checks | No | Docker info | P0 |
| P6 | P5, P3, P2 | P7 | Model inventory depends on runtime, filesystem and hardware | Yes (partial) | Model inventory | P0 |
| P7 | P6 | P8 | Inference test requires model availability | Yes (partial) | Inference capability | P1 |
| P8 | P7 | P9 | Resource validation depends on inference capability | Yes (partial) | Resource usage | P2 |
| P9 | P8 | P10 | Final hardware observation depends on resource validation | Yes (partial) | Hardware status | P2 |
| P10 | P9 | - | Integration check is final step | Yes (if previous steps executed) | Final integration | P1 |

## EXECUTION GRAPH

```
P1 (Hardware Detection)
   ├── P2 (System Configuration)
   │    └── P4 (Runtime Checks)
   ├── P3 (Filesystem Check)
   ├── P5 (Docker Foundation)
   │    ├── P4
   │    └── P6 (Model Inventory)
   │         └── P7 (Inference Test)
   │              └── P8 (Resource Validation)
   │                   └── P9 (Hardware Observation)
   │                        └── P10 (Final Integration)
```

## FAILURE ANALYSIS

### DIRECT BLOCKERS
- **P1**: Hardware detection failure blocks all dependent phases
- **P2**: System configuration failure blocks runtime checks 
- **P5**: Docker foundation failure blocks all runtime-dependent phases
- **P6**: Model inventory failure blocks inference tests (but not P9/P10)

### SOFT DEPENDENCIES  
- **P7**: Inference test can run even if model inventory has issues (partial evidence)
- **P8**: Resource validation can proceed with partial inference results
- **P9**: Hardware observation can collect basic info even without full inference

### INDEPENDENT PATHS
- **P1**: Can run alone to determine hardware profile
- **P2**: Can run independently after P1
- **P3**: Can run independently after P1  
- **P5**: Can run independently to verify Docker setup
- **P9**: Can collect hardware status without full inference
- **P10**: Can run final integration check with partial evidence

## DEPENDENCY GRAPH

### Critical Path: 
P1 → P2 → P4 → P5 → P6 → P7 → P8 → P9 → P10

### Alternative Paths:
- P1 → P3 → P6 → P7 (filesystem-focused)
- P1 → P2 → P5 → P6 → P7 → P8 (runtime-focused)  
- P9 → P10 (hardware-only path)

## PHASE FAILURE HANDLING

### P1 FAILURES
- **BLOCKED**: All downstream phases blocked
- **EVIDENCE**: Hardware profile, GPU info, VRAM info
- **RECOVERY**: Fix hardware detection logic

### P6 FAILURES  
- **DIRECT BLOCKER**: P7 blocked (inference test)
- **SOFT DEPENDENCY**: P8, P9 can still run independently
- **EVIDENCE**: Hardware info, Docker status, basic model presence
- **RECOVERY**: Fix model inventory extraction logic

### P7 FAILURES
- **DIRECT BLOCKER**: P8 blocked (resource validation)  
- **SOFT DEPENDENCY**: P9, P10 can still run independently
- **EVIDENCE**: Hardware info, Docker status, basic resource info
- **RECOVERY**: Fix model availability check

## MINI-MILESTONE STRATEGY

### M1: Fix P6 Model Inventory Producer
- **Change**: Correct hardcoded empty values in validate.sh
- **Evidence**: Runtime model inventory from Ollama API  
- **Risk**: Low
- **Effort**: Minimal
- **Status**: Complete

### M2: Validate JSON Schema Compliance  
- **Change**: Add proper JSON validation for model inventory
- **Evidence**: Schema-compliant evidence generation
- **Risk**: Low
- **Effort**: Medium
- **Status**: In Progress

### M3: Fix P7 Consumer Logic
- **Change**: Improve model availability checking
- **Evidence**: Complete inference test results
- **Risk**: Medium  
- **Effort**: Medium
- **Status**: Pending

## RECOVERY SEQUENCE

1. **Identify root cause** - Analyze failure patterns
2. **Prioritize recovery paths** - Fix highest-value dependencies first  
3. **Execute independent checks** - Collect available evidence
4. **Fix root causes** - Address shared infrastructure issues
5. **Revalidate descendants** - Test affected dependent phases
6. **Repeat cycle** - Continue until consolidated validation

## PRIORITY MATRIX

| Priority | Change | Root Cause | Phases Affected | Unblocks | Risk | Effort | Status |
|----------|--------|------------|-----------------|----------|------|--------|--------|
| P0 | Fix model inventory extraction | JSON parsing error | P6, P7 | All downstream | Low | Low | Complete |
| P1 | Improve inference test robustness | Incomplete validation | P8 | P9, P10 | Medium | Medium | In Progress |
| P2 | Add comprehensive evidence collection | Partial evidence | P9, P10 | All phases | Low | Medium | Planned |
| P3 | Implement JSON schema validation | Schema compliance | All phases | All phases | Low | High | Planned |

## FINAL EXECUTION ORDER

The actual execution order should be:
1. **P1** - Hardware detection (critical)
2. **P2** - System configuration  
3. **P3** - Filesystem checks
4. **P5** - Docker foundation
5. **P6** - Model inventory extraction (fixed)
6. **P7** - Inference test
7. **P8** - Resource validation
8. **P9** - Hardware observation  
9. **P10** - Final integration

This approach maximizes evidence collection while maintaining the minimum necessary dependencies for each phase.