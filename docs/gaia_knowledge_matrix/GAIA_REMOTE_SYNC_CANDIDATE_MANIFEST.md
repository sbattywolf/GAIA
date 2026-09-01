# GAIA Remote Sync Candidate Manifest

## Executive Summary

This document represents the final evidence-based curation of GAIA's documentation and implementation artifacts for remote synchronization. The goal is to identify exactly what belongs in the canonical GAIA baseline versus what should remain as historical, experimental, or local-only material.

The current repository contains both canonical GAIA documentation and implementation evidence that should be preserved, as well as temporary, vendor-specific, and experimental artifacts that should be excluded from the synchronized baseline.

## Proposed Canonical Remote Structure

```
gaia/
├── README.md
├── docs/
│   ├── adr/                    # Architecture Decision Records (canonical)
│   └── gaia_knowledge_matrix/  # Knowledge matrix documentation
├── reference/                  # GAIA semantic references (canonical)
└── gaia_3090_model_stack/      # Canonical implementation (3090 target environment)
```

## Canonical GAIA Documentation

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| README.md | Document | Project overview and identity | Core project description, design principles, current phase | High semantic value for GAIA identity and purpose | Low implementation value | Original | Active | README.md | CANONICAL_GAIA |
| docs/adr/ADR-0001-Core-Boundary.md | ADR | Core architectural boundaries | Definition of GAIA's minimal core boundary | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0001-Core-Boundary.md | CANONICAL_ADR |
| docs/adr/ADR-0002-Memory-Semantics.md | ADR | Memory handling semantics | Memory semantics and data handling requirements | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0002-Memory-Semantics.md | CANONICAL_ADR |
| docs/adr/ADR-0003-Capability-Model.md | ADR | Capability model definition | GAIA's capability model and execution semantics | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0003-Capability-Model.md | CANONICAL_ADR |
| docs/adr/ADR-0004-HomeAssistant-Boundary.md | ADR | Home Assistant integration boundary | Home Assistant integration constraints and approaches | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0004-HomeAssistant-Boundary.md | CANONICAL_ADR |
| docs/adr/ADR-0005-Communication-State.md | ADR | Communication state management | Communication and interaction state semantics | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0005-Communication-State.md | CANONICAL_ADR |
| docs/adr/ADR-0006-Tool-Trust.md | ADR | Tool trust mechanisms | Tool trust and security model | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0006-Tool-Trust.md | CANONICAL_ADR |
| docs/adr/ADR-0007-Event-Semantics.md | ADR | Event semantics | Event handling and processing semantics | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0007-Event-Semantics.md | CANONICAL_ADR |
| docs/gaia_knowledge_matrix/MASTER_DOCUMENTATION_ENTRY.md | Documentation | Master documentation entry | Complete overview of GAIA's architectural requirements and integration patterns | High semantic value for understanding GAIA architecture | Low implementation value | Sprint 5 | Active | docs/gaia_knowledge_matrix/MASTER_DOCUMENTATION_ENTRY.md | CANONICAL_GAIA |
| docs/gaia_knowledge_matrix/GAIA_KNOWLEDGE_MATRIX.md | Documentation | Knowledge matrix documentation | Evolution of GAIA concepts from research to implementation | High semantic value for understanding project evolution | Low implementation value | Sprint 5 | Active | docs/gaia_knowledge_matrix/GAIA_KNOWLEDGE_MATRIX.md | CANONICAL_GAIA |
| docs/reference/IDENTITY.md | Reference | Stable identity statement | Core GAIA identity declaration | High semantic value for project identity | Low implementation value | Original | Active | docs/reference/IDENTITY.md | GAIA_REFERENCE |
| docs/reference/MANIFESTO.md | Reference | Project manifesto | Foundational declaration of GAIA's purpose and principles | High semantic value for project direction | Low implementation value | Original | Active | docs/reference/MANIFESTO.md | GAIA_REFERENCE |
| docs/reference/DESIGN_PRINCIPLES.md | Reference | Design principles | Core design principles for the system | High semantic value for architecture guidance | Low implementation value | Sprint 1 | Active | docs/reference/DESIGN_PRINCIPLES.md | GAIA_REFERENCE |
| docs/reference/GAIA_MODEL.md | Reference | Canonical model | Official conceptual model of GAIA | High semantic value for understanding core concepts | Low implementation value | Sprint 3 | Active | docs/reference/GAIA_MODEL.md | GAIA_REFERENCE |
| docs/reference/NEXT_STEPS.md | Reference | Future roadmap | Current project maturity and next steps | High semantic value for future planning | Low implementation value | Sprint 5 | Active | docs/reference/NEXT_STEPS.md | GAIA_REFERENCE |

## Canonical ADRs

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| docs/adr/ADR-0001-Core-Boundary.md | ADR | Core architectural boundaries | Definition of GAIA's minimal core boundary | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0001-Core-Boundary.md | CANONICAL_ADR |
| docs/adr/ADR-0002-Memory-Semantics.md | ADR | Memory handling semantics | Memory semantics and data handling requirements | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0002-Memory-Semantics.md | CANONICAL_ADR |
| docs/adr/ADR-0003-Capability-Model.md | ADR | Capability model definition | GAIA's capability model and execution semantics | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0003-Capability-Model.md | CANONICAL_ADR |
| docs/adr/ADR-0004-HomeAssistant-Boundary.md | ADR | Home Assistant integration boundary | Home Assistant integration constraints and approaches | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0004-HomeAssistant-Boundary.md | CANONICAL_ADR |
| docs/adr/ADR-0005-Communication-State.md | ADR | Communication state management | Communication and interaction state semantics | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0005-Communication-State.md | CANONICAL_ADR |
| docs/adr/ADR-0006-Tool-Trust.md | ADR | Tool trust mechanisms | Tool trust and security model | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0006-Tool-Trust.md | CANONICAL_ADR |
| docs/adr/ADR-0007-Event-Semantics.md | ADR | Event semantics | Event handling and processing semantics | High semantic value for architecture | Low implementation value | Sprint 4 | Active | docs/adr/ADR-0007-Event-Semantics.md | CANONICAL_ADR |

## GAIA References

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| docs/reference/IDENTITY.md | Reference | Stable identity statement | Core GAIA identity declaration | High semantic value for project identity | Low implementation value | Original | Active | docs/reference/IDENTITY.md | GAIA_REFERENCE |
| docs/reference/MANIFESTO.md | Reference | Project manifesto | Foundational declaration of GAIA's purpose and principles | High semantic value for project direction | Low implementation value | Original | Active | docs/reference/MANIFESTO.md | GAIA_REFERENCE |
| docs/reference/DESIGN_PRINCIPLES.md | Reference | Design principles | Core design principles for the system | High semantic value for architecture guidance | Low implementation value | Sprint 1 | Active | docs/reference/DESIGN_PRINCIPLES.md | GAIA_REFERENCE |
| docs/reference/GAIA_MODEL.md | Reference | Canonical model | Official conceptual model of GAIA | High semantic value for understanding core concepts | Low implementation value | Sprint 3 | Active | docs/reference/GAIA_MODEL.md | GAIA_REFERENCE |
| docs/reference/NEXT_STEPS.md | Reference | Future roadmap | Current project maturity and next steps | High semantic value for future planning | Low implementation value | Sprint 5 | Active | docs/reference/NEXT_STEPS.md | GAIA_REFERENCE |

## S1-S7 Disposition

### Sprint 1
| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-01/ARCHITECTURAL_CRITIQUE.md | Document | Architectural critique | Initial architectural critique and concerns | Medium semantic value for historical context | Low implementation value | Sprint 1 | Historical | sprints/sprint-01/ARCHITECTURAL_CRITIQUE.md | HISTORICAL_EVIDENCE |
| sprints/sprint-01/GAIA_REUSE_ANALYSIS.md | Document | Reuse analysis | Analysis of potential reuse patterns | Medium semantic value for historical context | Low implementation value | Sprint 1 | Historical | sprints/sprint-01/GAIA_REUSE_ANALYSIS.md | HISTORICAL_EVIDENCE |

### Sprint 2
| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-02/SPRINT_02_SYNTHESIS.md | Document | Sprint synthesis | Synthesis of sprint 2 findings and approach | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/SPRINT_02_SYNTHESIS.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/01_World_Model_Review.md | Document | World model review | Review of world model approaches and constraints | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/01_World_Model_Review.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/02_Architectural_Stress_Test.md | Document | Architectural stress test | Stress testing approach for architectural decisions | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/02_Architectural_Stress_Test.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/03_AI_Architecture_Patterns.md | Document | AI architecture patterns | Analysis of AI architecture patterns and approaches | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/03_AI_Architecture_Patterns.md | HISTORICAL_EVIDENCE |

### Sprint 3
| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-03/MEMORY_ROLE_VALIDATION.md | Document | Memory role validation | Validation of memory roles and semantics | Medium semantic value for historical context | Low implementation value | Sprint 3 | Historical | sprints/sprint-03/MEMORY_ROLE_VALIDATION.md | HISTORICAL_EVIDENCE |
| sprints/sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md | Document | First home scenario validation | Validation of first home scenario approach | Medium semantic value for historical context | Low implementation value | Sprint 3 | Historical | sprints/sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md | HISTORICAL_EVIDENCE |

### Sprint 4
| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-04/ARCHITECT_UNBLOCKING_ASSESSMENT.md | Document | Architectural unblocking assessment | Assessment of architectural constraints and solutions | Medium-high semantic value for understanding blocking issues | Low implementation value | Sprint 4 | Historical | sprints/sprint-04/ARCHITECT_UNBLOCKING_ASSESSMENT.md | HISTORICAL_EVIDENCE |
| sprints/sprint-04/RECONSTRUCTION.md | Document | Reconstruction methodology | Methodology for project reconstruction | Medium-high semantic value for understanding process | Low implementation value | Sprint 4 | Historical | sprints/sprint-04/RECONSTRUCTION.md | HISTORICAL_EVIDENCE |

### Sprint 5
| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-05/GAIA_RECONSTRUCTION_CLEANUP_REPORT.md | Document | Cleanup report | Report on reconstruction cleanup activities | Medium semantic value for understanding process | Low implementation value | Sprint 5 | Historical | sprints/sprint-05/GAIA_RECONSTRUCTION_CLEANUP_REPORT.md | HISTORICAL_EVIDENCE |
| sprints/sprint-05/KWON_-_GAIA_PROJECT_KNOWLEDGE.md | Document | Project knowledge documentation | Comprehensive project knowledge documentation | High semantic value for understanding project context | Medium implementation value | Sprint 5 | Historical | sprints/sprint-05/KWON_-_GAIA_PROJECT_KNOWLEDGE.md | HISTORICAL_EVIDENCE |
| sprints/sprint-05/GAIA_FINAL_RECONCILIATION.md | Document | Final reconciliation | Final reconciliation summary | High semantic value for understanding process | Low implementation value | Sprint 5 | Historical | sprints/sprint-05/GAIA_FINAL_RECONCILIATION.md | HISTORICAL_EVIDENCE |

### Sprint 6 and 7
| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-06/ | Directory | Sprint 6 content | Various sprint 6 documents | Medium semantic value for historical context | Low implementation value | Sprint 6 | Historical | sprints/sprint-06/ | HISTORICAL_EVIDENCE |
| sprints/sprint-07/ | Directory | Sprint 7 content | Various sprint 7 documents | Medium semantic value for historical context | Low implementation value | Sprint 7 | Historical | sprints/sprint-07/ | HISTORICAL_EVIDENCE |

## Root-level Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| 1070_node_pairing_setup.md | Document | Pairing setup documentation | Documentation for 1070 node pairing | Medium semantic value for understanding integration | Medium implementation value | Sprint 5 | Implementation evidence | 1070_node_pairing_setup.md | IMPLEMENTATION_EVIDENCE |
| BACKWARD_RECONCILIATION_S1-S4_CONVERGENCE.md | Document | Backward reconciliation | Documentation of backward reconciliation work | Medium semantic value for understanding process | Low implementation value | Sprint 5 | Historical | BACKWARD_RECONCILIATION_S1-S4_CONVERGENCE.md | HISTORICAL_EVIDENCE |
| GAIA-DEV-OPENCLAW-MIGRATION-MANIFEST.md | Document | OpenClaw migration manifest | Migration documentation for OpenClaw | Medium semantic value for understanding integration | Low implementation value | Sprint 5 | Historical | GAIA-DEV-OPENCLAW-MIGRATION-MANIFEST.md | HISTORICAL_EVIDENCE |
| PRE_PROMOTION_CLEANUP_SUMMARY.md | Document | Pre-promotion cleanup | Summary of pre-promotion cleanup activities | Medium semantic value for understanding process | Low implementation value | Sprint 5 | Historical | PRE_PROMOTION_CLEANUP_SUMMARY.md | HISTORICAL_EVIDENCE |
| WORKTREE_INVENTORY.md | Document | Worktree inventory | Inventory of worktrees and related files | Low semantic value for core project | Medium implementation value | Sprint 5 | Historical | WORKTREE_INVENTORY.md | HISTORICAL_EVIDENCE |
| integration_report.md | Document | Integration report | Report on various integration activities | Medium semantic value for understanding integration | Low implementation value | Sprint 5 | Implementation evidence | integration_report.md | IMPLEMENTATION_EVIDENCE |

## 1070 Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_1070_evidence/ | Directory | 1070 evidence directory | Evidence of 1070 target system | Low semantic value for core project | High implementation value | Sprint 5 | Implementation evidence | gaia_1070_evidence/ | IMPLEMENTATION_EVIDENCE |
| gaia_1070_model_runtime/ | Directory | 1070 model runtime | Model runtime configuration for 1070 system | Low semantic value for core project | High implementation value | Sprint 5 | Implementation evidence | gaia_1070_model_runtime/ | IMPLEMENTATION_EVIDENCE |

## 3090 Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_3090_model_stack/ | Directory | 3090 model stack | Canonical configuration for 3090 target hardware | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/ | IMPLEMENTATION_EVIDENCE |

## Engineering-loop Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_engineering_loop/ | Directory | Engineering loop framework | Framework for engineering processes | Medium semantic value for understanding process | High implementation value | Sprint 5 | Implementation evidence | gaia_engineering_loop/ | IMPLEMENTATION_EVIDENCE |

## Experiments/Software/Tools/Tests Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| experiments/ | Directory | Experimental artifacts | Various experimental work | Low semantic value for core project | Medium implementation value | Various | Experimental | experiments/ | EXPERIMENTAL_ARTIFACT |
| software/ | Directory | Software artifacts | Various software tools and code | Low semantic value for core project | Medium implementation value | Various | Experimental | software/ | EXPERIMENTAL_ARTIFACT |
| tools/ | Directory | Tooling artifacts | Various tooling documentation | Low semantic value for core project | Medium implementation value | Various | Experimental | tools/ | EXPERIMENTAL_ARTIFACT |
| tests/ | Directory | Test artifacts | Various test files and reports | Low semantic value for core project | Medium implementation value | Various | Test/validation evidence | tests/ | TEST_VALIDATION_EVIDENCE |
| validation/ | Directory | Validation artifacts | Various validation documentation | Low semantic value for core project | Medium implementation value | Various | Test/validation evidence | validation/ | TEST_VALIDATION_EVIDENCE |
| scripts/ | Directory | Script files | Various automation scripts | Low semantic value for core project | Medium implementation value | Various | Implementation evidence | scripts/ | IMPLEMENTATION_EVIDENCE |
| prototypes/examples/harnesses/benchmarks/ | Directory | Prototype artifacts | Various prototype, example, harness, and benchmark materials | Low semantic value for core project | Medium implementation value | Various | Experimental | prototypes/examples/harnesses/benchmarks/ | EXPERIMENTAL_ARTIFACT |

## OpenClaw Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| docs/gaia_knowledge_matrix/OPENCLAW_GATEWAY_ACCESS_DIAGNOSIS.md | Document | OpenClaw gateway diagnosis | Diagnosis of OpenClaw gateway access issues | Medium semantic value for understanding integration | High implementation value | Sprint 5 | Implementation evidence | docs/gaia_knowledge_matrix/OPENCLAW_GATEWAY_ACCESS_DIAGNOSIS.md | IMPLEMENTATION_EVIDENCE |
| docs/gaia_knowledge_matrix/OPENCLAW_RUNTIME_PRIMITIVES.md | Document | OpenClaw runtime primitives | Documentation of OpenClaw runtime primitives | Medium semantic value for understanding integration | High implementation value | Sprint 5 | Implementation evidence | docs/gaia_knowledge_matrix/OPENCLAW_RUNTIME_PRIMITIVES.md | IMPLEMENTATION_EVIDENCE |
| gaia_3090_model_stack/ | Directory | 3090 model stack with OpenClaw | Configuration for OpenClaw integration | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/ | IMPLEMENTATION_EVIDENCE |

## OpenCode Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_3090_model_stack/Dockerfile.opencode-git | Document | OpenCode Dockerfile | Docker configuration for OpenCode integration | Medium semantic value for understanding integration | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/Dockerfile.opencode-git | IMPLEMENTATION_EVIDENCE |
| gaia_3090_model_stack/opencode-build/ | Directory | OpenCode build artifacts | Build artifacts for OpenCode integration | Medium semantic value for understanding integration | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/opencode-build/ | IMPLEMENTATION_EVIDENCE |

## Ollama Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_3090_model_stack/ | Directory | 3090 model stack with Ollama | Configuration for Ollama integration | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/ | IMPLEMENTATION_EVIDENCE |

## OpenWebUI Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_3090_model_stack/ | Directory | 3090 model stack with OpenWebUI | Configuration for OpenWebUI integration | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/ | IMPLEMENTATION_EVIDENCE |

## Docker/Infrastructure Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_3090_model_stack/compose.yaml | Document | Docker Compose configuration | Canonical Docker Compose configuration for GAIA 3090 stack | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/compose.yaml | IMPLEMENTATION_EVIDENCE |
| gaia_3090_model_stack/scripts/ | Directory | Script files | Start/stop/status scripts for GAIA 3090 stack | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/scripts/ | IMPLEMENTATION_EVIDENCE |
| gaia_3090_model_stack/identity_files/ | Directory | Identity files | Identity and credential files | Medium semantic value for understanding integration | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/identity_files/ | IMPLEMENTATION_EVIDENCE |

## Git/Linear Tooling Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| e exec gaia-3090-openclaw openclaw gateway status --deep | Document | Gateway status command output | Command execution result showing gateway status | Low semantic value for core project | Medium implementation value | Sprint 5 | Generated/local-only | e exec gaia-3090-openclaw openclaw gateway status --deep | GENERATED_TEMPORARY |

## Scaricati/Downloads Disposition

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| Scaricati/ | Directory | Downloaded files | Various downloaded materials | Low semantic value for core project | Medium implementation value | Various | Generated/local-only | Scaricati/ | GENERATED_TEMPORARY |

## Duplicate/Conflict Analysis

| DUPLICATE PATHS | CONFLICT TYPE | RESOLUTION | NOTES |
|-----------------|---------------|------------|-------|
| docs/gaia_knowledge_matrix/MASTER_DOCUMENTATION_ENTRY.md vs. GAIA_MAIN_PROMOTION_PLAN.md | Content overlap | Keep MASTER_DOCUMENTATION_ENTRY as primary | Both contain master documentation but different perspectives |
| docs/adr/ADR-0003-Capability-Model.md vs. ADR-0003-Capability-Model_Accepted.md | File duplication | Keep ADR-0003-Capability-Model | This is the canonical version |
| Multiple OpenClaw diagnosis files | Content overlap | Keep OPENCLAW_GATEWAY_ACCESS_DIAGNOSIS.md | One primary file with better documentation |

## Historical Evidence to Preserve

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| sprints/sprint-01/ARCHITECTURAL_CRITIQUE.md | Document | Architectural critique | Initial architectural critique and concerns | Medium semantic value for historical context | Low implementation value | Sprint 1 | Historical | sprints/sprint-01/ARCHITECTURAL_CRITIQUE.md | HISTORICAL_EVIDENCE |
| sprints/sprint-01/GAIA_REUSE_ANALYSIS.md | Document | Reuse analysis | Analysis of potential reuse patterns | Medium semantic value for historical context | Low implementation value | Sprint 1 | Historical | sprints/sprint-01/GAIA_REUSE_ANALYSIS.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/SPRINT_02_SYNTHESIS.md | Document | Sprint synthesis | Synthesis of sprint 2 findings and approach | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/SPRINT_02_SYNTHESIS.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/01_World_Model_Review.md | Document | World model review | Review of world model approaches and constraints | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/01_World_Model_Review.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/02_Architectural_Stress_Test.md | Document | Architectural stress test | Stress testing approach for architectural decisions | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/02_Architectural_Stress_Test.md | HISTORICAL_EVIDENCE |
| sprints/sprint-02/03_AI_Architecture_Patterns.md | Document | AI architecture patterns | Analysis of AI architecture patterns and approaches | Medium semantic value for historical context | Low implementation value | Sprint 2 | Historical | sprints/sprint-02/03_AI_Architecture_Patterns.md | HISTORICAL_EVIDENCE |
| sprints/sprint-03/MEMORY_ROLE_VALIDATION.md | Document | Memory role validation | Validation of memory roles and semantics | Medium semantic value for historical context | Low implementation value | Sprint 3 | Historical | sprints/sprint-03/MEMORY_ROLE_VALIDATION.md | HISTORICAL_EVIDENCE |
| sprints/sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md | Document | First home scenario validation | Validation of first home scenario approach | Medium semantic value for historical context | Low implementation value | Sprint 3 | Historical | sprints/sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md | HISTORICAL_EVIDENCE |
| sprints/sprint-04/ARCHITECT_UNBLOCKING_ASSESSMENT.md | Document | Architectural unblocking assessment | Assessment of architectural constraints and solutions | Medium-high semantic value for understanding blocking issues | Low implementation value | Sprint 4 | Historical | sprints/sprint-04/ARCHITECT_UNBLOCKING_ASSESSMENT.md | HISTORICAL_EVIDENCE |
| sprints/sprint-04/RECONSTRUCTION.md | Document | Reconstruction methodology | Methodology for project reconstruction | Medium-high semantic value for understanding process | Low implementation value | Sprint 4 | Historical | sprints/sprint-04/RECONSTRUCTION.md | HISTORICAL_EVIDENCE |
| sprints/sprint-05/GAIA_RECONSTRUCTION_CLEANUP_REPORT.md | Document | Cleanup report | Report on reconstruction cleanup activities | Medium semantic value for understanding process | Low implementation value | Sprint 5 | Historical | sprints/sprint-05/GAIA_RECONSTRUCTION_CLEANUP_REPORT.md | HISTORICAL_EVIDENCE |
| sprints/sprint-05/KWON_-_GAIA_PROJECT_KNOWLEDGE.md | Document | Project knowledge documentation | Comprehensive project knowledge documentation | High semantic value for understanding project context | Medium implementation value | Sprint 5 | Historical | sprints/sprint-05/KWON_-_GAIA_PROJECT_KNOWLEDGE.md | HISTORICAL_EVIDENCE |
| sprints/sprint-05/GAIA_FINAL_RECONCILIATION.md | Document | Final reconciliation | Final reconciliation summary | High semantic value for understanding process | Low implementation value | Sprint 5 | Historical | sprints/sprint-05/GAIA_FINAL_RECONCILIATION.md | HISTORICAL_EVIDENCE |
| docs/gaia_knowledge_matrix/KNOWLEDGE_MATRIX_AUDIT.md | Document | Knowledge matrix audit | Audit of knowledge matrix development process | Medium semantic value for understanding process | Low implementation value | Sprint 5 | Historical | docs/gaia_knowledge_matrix/KNOWLEDGE_MATRIX_AUDIT.md | HISTORICAL_EVIDENCE |
| docs/gaia_knowledge_matrix/RECONCILIATION_STATUS_MODEL.md | Document | Reconciliation status model | Model of how reconciliation process was approached | Medium semantic value for understanding process | Low implementation value | Sprint 5 | Historical | docs/gaia_knowledge_matrix/RECONCILIATION_STATUS_MODEL.md | HISTORICAL_EVIDENCE |

## Implementation Evidence to Preserve

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| gaia_3090_model_stack/ | Directory | 3090 model stack | Canonical configuration for 3090 target hardware | High semantic value for understanding target system | High implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/ | IMPLEMENTATION_EVIDENCE |
| gaia_1070_evidence/ | Directory | 1070 evidence directory | Evidence of 1070 target system | Low semantic value for core project | High implementation value | Sprint 5 | Implementation evidence | gaia_1070_evidence/ | IMPLEMENTATION_EVIDENCE |
| gaia_1070_model_runtime/ | Directory | 1070 model runtime | Model runtime configuration for 1070 system | Low semantic value for core project | High implementation value | Sprint 5 | Implementation evidence | gaia_1070_model_runtime/ | IMPLEMENTATION_EVIDENCE |
| gaia_engineering_loop/ | Directory | Engineering loop framework | Framework for engineering processes | Medium semantic value for understanding process | High implementation value | Sprint 5 | Implementation evidence | gaia_engineering_loop/ | IMPLEMENTATION_EVIDENCE |
| integration_report.md | Document | Integration report | Report on various integration activities | Medium semantic value for understanding integration | Low implementation value | Sprint 5 | Implementation evidence | integration_report.md | IMPLEMENTATION_EVIDENCE |
| pairing_report.md | Document | Pairing report | Report on GAIA-3090 ↔ 1070 pairing process | Medium semantic value for understanding integration | Low implementation value | Sprint 5 | Implementation evidence | gaia_3090_model_stack/pairing_report.md | IMPLEMENTATION_EVIDENCE |

## Generated/Local-only Material

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| e exec gaia-3090-openclaw openclaw gateway status --deep | Document | Gateway status command output | Command execution result showing gateway status | Low semantic value for core project | Medium implementation value | Sprint 5 | Generated/local-only | e exec gaia-3090-openclaw openclaw gateway status --deep | GENERATED_TEMPORARY |
| Scaricati/ | Directory | Downloaded files | Various downloaded materials | Low semantic value for core project | Medium implementation value | Various | Generated/local-only | Scaricati/ | GENERATED_TEMPORARY |

## Ambiguous Items

| CURRENT PATH | TYPE | PURPOSE | WHAT IT ACTUALLY CONTAINS | GAIA SEMANTIC VALUE | IMPLEMENTATION / TOOL VALUE | PROVENANCE | CURRENT STATUS | PROPOSED REMOTE PATH | DISPOSITION |
|--------------|------|---------|---------------------------|---------------------|------------------------------|------------|----------------|----------------------|-------------|
| docs/gaia_knowledge_matrix/AD_HOC_RESEARCH_INVENTORY.md | Document | Ad-hoc research inventory | Inventory of ad-hoc research materials | Low semantic value for core project | Low implementation value | Various | Ambiguous review | docs/gaia_knowledge_matrix/AD_HOC_RESEARCH_INVENTORY.md | AMBIGUOUS_REVIEW |
| gaia_3090_model_stack/compose.yaml.backup | Document | Docker Compose backup | Backup of compose configuration | Low semantic value for core project | Medium implementation value | Sprint 5 | Ambiguous review | gaia_3090_model_stack/compose.yaml.backup | AMBIGUOUS_REVIEW |
| gaia_3090_model_stack/compose.yaml.pre-pin | Document | Docker Compose pre-pinning | Pre-pinning compose configuration | Low semantic value for core project | Medium implementation value | Sprint 5 | Ambiguous review | gaia_3090_model_stack/compose.yaml.pre-pin | AMBIGUOUS_REVIEW |

## EXACT REMOTE INCLUDE SET

CURRENT PATH → REMOTE PATH → DISPOSITION → REASON

1. README.md → README.md → CANONICAL_GAIA → Core project identity documentation
2. docs/adr/ADR-0001-Core-Boundary.md → docs/adr/ADR-0001-Core-Boundary.md → CANONICAL_ADR → Core architectural boundary definition
3. docs/adr/ADR-0002-Memory-Semantics.md → docs/adr/ADR-0002-Memory-Semantics.md → CANONICAL_ADR → Memory semantics requirements
4. docs/adr/ADR-0003-Capability-Model.md → docs/adr/ADR-0003-Capability-Model.md → CANONICAL_ADR → Capability model definition
5. docs/adr/ADR-0004-HomeAssistant-Boundary.md → docs/adr/ADR-0004-HomeAssistant-Boundary.md → CANONICAL_ADR → Home Assistant integration constraints
6. docs/adr/ADR-0005-Communication-State.md → docs/adr/ADR-0005-Communication-State.md → CANONICAL_ADR → Communication state semantics
7. docs/adr/ADR-0006-Tool-Trust.md → docs/adr/ADR-0006-Tool-Trust.md → CANONICAL_ADR → Tool trust mechanisms
8. docs/adr/ADR-0007-Event-Semantics.md → docs/adr/ADR-0007-Event-Semantics.md → CANONICAL_ADR → Event handling semantics
9. docs/gaia_knowledge_matrix/MASTER_DOCUMENTATION_ENTRY.md → docs/gaia_knowledge_matrix/MASTER_DOCUMENTATION_ENTRY.md → CANONICAL_GAIA → Master documentation entry with comprehensive overview
10. docs/gaia_knowledge_matrix/GAIA_KNOWLEDGE_MATRIX.md → docs/gaia_knowledge_matrix/GAIA_KNOWLEDGE_MATRIX.md → CANONICAL_GAIA → Knowledge matrix documentation showing evolution of concepts
11. docs/reference/IDENTITY.md → docs/reference/IDENTITY.md → GAIA_REFERENCE → Stable identity statement
12. docs/reference/MANIFESTO.md → docs/reference/MANIFESTO.md → GAIA_REFERENCE → Project manifesto
13. docs/reference/DESIGN_PRINCIPLES.md → docs/reference/DESIGN_PRINCIPLES.md → GAIA_REFERENCE → Core design principles
14. docs/reference/GAIA_MODEL.md → docs/reference/GAIA_MODEL.md → GAIA_REFERENCE → Official conceptual model
15. docs/reference/NEXT_STEPS.md → docs/reference/NEXT_STEPS.md → GAIA_REFERENCE → Future roadmap
16. gaia_3090_model_stack/ → gaia_3090_model_stack/ → IMPLEMENTATION_EVIDENCE → Canonical configuration for 3090 target hardware

## EXACT REMOTE EXCLUDE SET

CURRENT PATH → REMOTE PATH → DISPOSITION → REASON

1. sprints/sprint-01/ → sprints/sprint-01/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
2. sprints/sprint-02/ → sprints/sprint-02/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
3. sprints/sprint-03/ → sprints/sprint-03/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
4. sprints/sprint-04/ → sprints/sprint-04/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
5. sprints/sprint-05/ → sprints/sprint-05/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
6. sprints/sprint-06/ → sprints/sprint-06/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
7. sprints/sprint-07/ → sprints/sprint-07/ → HISTORICAL_EVIDENCE → Sprint-level historical research and documentation
8. gaia_1070_evidence/ → gaia_1070_evidence/ → IMPLEMENTATION_EVIDENCE → 1070 target system evidence (implementation)
9. gaia_1070_model_runtime/ → gaia_1070_model_runtime/ → IMPLEMENTATION_EVIDENCE → 1070 model runtime configuration (implementation)
10. experiments/ → experiments/ → EXPERIMENTAL_ARTIFACT → Experimental artifacts
11. software/ → software/ → EXPERIMENTAL_ARTIFACT → Software artifacts
12. tools/ → tools/ → EXPERIMENTAL_ARTIFACT → Tooling artifacts
13. tests/ → tests/ → TEST_VALIDATION_EVIDENCE → Test artifacts
14. validation/ → validation/ → TEST_VALIDATION_EVIDENCE → Validation artifacts
15. prototypes/examples/harnesses/benchmarks/ → prototypes/examples/harnesses/benchmarks/ → EXPERIMENTAL_ARTIFACT → Prototype, example, harness, and benchmark materials
16. e exec gaia-3090-openclaw openclaw gateway status --deep → e exec gaia-3090-openclaw openclaw gateway status --deep → GENERATED_TEMPORARY → Command execution result showing gateway status
17. Scaricati/ → Scaricati/ → GENERATED_TEMPORARY → Downloaded files and materials
18. docs/gaia_knowledge_matrix/AD_HOC_RESEARCH_INVENTORY.md → docs/gaia_knowledge_matrix/AD_HOC_RESEARCH_INVENTORY.md → AMBIGUOUS_REVIEW → Ad-hoc research inventory with unclear value
19. gaia_3090_model_stack/compose.yaml.backup → gaia_3090_model_stack/compose.yaml.backup → AMBIGUOUS_REVIEW → Backup compose configuration
20. gaia_3090_model_stack/compose.yaml.pre-pin → gaia_3090_model_stack/compose.yaml.pre-pin → AMBIGUOUS_REVIEW → Pre-pinning compose configuration

## Human Owner Decisions Required

1. Whether to include the 1070 evidence directories in the baseline (they are implementation evidence but may be valuable for complete understanding)
2. Whether to preserve all historical sprint documentation or selectively retain only key artifacts
3. Whether to include experimental and prototype materials for reference purposes
4. Final confirmation on the disposition of ambiguous items like AD_HOC_RESEARCH_INVENTORY.md