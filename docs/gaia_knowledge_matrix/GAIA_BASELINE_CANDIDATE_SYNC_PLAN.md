# GAIA Baseline Candidate Sync Plan

## 1. Overview

This document provides a detailed comparison of key documentation content across candidate branches to inform selection of the canonical GAIA documentation baseline. The analysis focuses on material that could affect future documentation and architectural decisions.

## 2. Key Documentation Analysis

### 2.1 ADR Content Comparison

| Artifact | Source Branch | Target Version | Difference | Provenance | Semantic Impact | Recommendation |
|----------|---------------|----------------|------------|------------|-----------------|----------------|
| ADR-0001-Core-Boundary.md | backup/pre-copilot-import | main | Different status (Proposed vs Accepted) and different content structure. Original version has a more open-ended approach while main has the finalized version. | backup/pre-copilot-import contains early draft; main has final accepted version | The main branch contains the correct, accepted version with proper structure. | KEEP_CURRENT |
| ADR-0001-Core-Boundary.md | import/copilot-current-state | main | Same as above - main has the final accepted version | import/copilot-current-state is an evolution of the documentation but main has the current canonical version | No difference, main is canonical | KEEP_CURRENT |
| ADR-0001-Core-Boundary.md | backup/repository-consolidation-accidental | main | Same as above - main has the final accepted version | backup/repository-consolidation-accidental contains a version that's consistent with main | No difference, main is canonical | KEEP_CURRENT |
| ADR-0001-Core-Boundary.md | AP6ST1_git_master_remote_repo | main | Same as above - main has the final accepted version | AP6ST1_git_master_remote_repo contains a version consistent with main | No difference, main is canonical | KEEP_CURRENT |
| ADR-0003-Capability-Model_Accepted.md | main | main | This is the same file | The file exists in main branch | No difference | KEEP_CURRENT |
| ADR-0003-Capability-Model.md | main | main | This is the same file | The file exists in main branch | No difference | KEEP_CURRENT |

### 2.2 Master Documentation Entry

| Artifact | Source Branch | Target Version | Difference | Provenance | Semantic Impact | Recommendation |
|----------|---------------|----------------|------------|------------|-----------------|----------------|
| MASTER_DOCUMENTATION_ENTRY.md | import/copilot-current-state | Not present in main | File exists only in import/copilot-current-state branch | import/copilot-current-state has a comprehensive master entry | This is important for understanding the overall documentation structure | IMPORT |
| MASTER_DOCUMENTATION_ENTRY.md | backup/pre-copilot-import | Not present in main | File exists only in backup/pre-copilot-import | backup/pre-copilot-import has an early version of master documentation | Provides historical context but not canonical | PRESERVE_HISTORICAL |

### 2.3 Knowledge Matrix and Reconciliation Status

| Artifact | Source Branch | Target Version | Difference | Provenance | Semantic Impact | Recommendation |
|----------|---------------|----------------|------------|------------|-----------------|----------------|
| GAIA_KNOWLEDGE_MATRIX.md | backup/repository-consolidation-accidental | Not present in main | File exists only in backup/repository-consolidation-accidental | backup/repository-consolidation-accidental contains reconciliation documentation | Important for understanding the reconciliation process | IMPORT |
| RECONCILIATION_STATUS_MODEL.md | backup/repository-consolidation-accidental | Not present in main | File exists only in backup/repository-consolidation-accidental | backup/repository-consolidation-accidental contains reconciliation status model | Provides insight into how reconciliation was approached | IMPORT |
| FINAL_RECONCILIATION_SUMMARY.md | backup/repository-consolidation-accidental | Not present in main | File exists only in backup/repository-consolidation-accidental | backup/repository-consolidation-accidental contains final reconciliation summary | Critical for understanding the reconciliation process and decisions made | IMPORT |

### 2.4 Architecture Decision Records

| Artifact | Source Branch | Target Version | Difference | Provenance | Semantic Impact | Recommendation |
|----------|---------------|----------------|------------|------------|-----------------|----------------|
| ADR-0002-Memory-Semantics.md | main | main | File exists in main branch | Main branch contains the current version | No difference | KEEP_CURRENT |
| ADR-0003-Capability-Model.md | main | main | File exists in main branch | Main branch contains the current version | No difference | KEEP_CURRENT |
| ADR-0004-HomeAssistant-Boundary.md | main | main | File exists in main branch | Main branch contains the current version | No difference | KEEP_CURRENT |
| ADR-0005-Communication-State.md | main | main | File exists in main branch | Main branch contains the current version | No difference | KEEP_CURRENT |
| ADR-0006-Tool-Trust.md | main | main | File exists in main branch | Main branch contains the current version | No difference | KEEP_CURRENT |
| ADR-0007-Event-Semantics.md | main | main | File exists in main branch | Main branch contains the current version | No difference | KEEP_CURRENT |

### 2.5 Implementation-to-Architecture Mappings

| Artifact | Source Branch | Target Version | Difference | Provenance | Semantic Impact | Recommendation |
|----------|---------------|----------------|------------|------------|-----------------|----------------|
| GAIA_ENGINEER_AS_IS_REVIEW.md | backup/repository-consolidation-accidental | Not present in main | File exists only in backup/repository-consolidation-accidental | backup/repository-consolidation-accidental contains engineer review documentation | Provides insight into the current state of implementation and architecture alignment | IMPORT |
| PHASE_2_DISCOVERY_REPORT.md | backup/repository-consolidation-accidental | Not present in main | File exists only in backup/repository-consolidation-accidental | backup/repository-consolidation-accidental contains phase 2 discovery report | Important for understanding the engineering approach | IMPORT |

### 2.6 References and Supporting Documentation

| Artifact | Source Branch | Target Version | Difference | Provenance | Semantic Impact | Recommendation |
|----------|---------------|----------------|------------|------------|-----------------|----------------|
| references/README.md | backup/pre-copilot-import | Not present in main | File exists only in backup/pre-copilot-import | backup/pre-copilot-import contains early reference documentation | Provides historical context for reference materials | PRESERVE_HISTORICAL |

## 3. Content Analysis Summary

### Content Already Incorporated into ING_3090
- All core ADRs (ADR-0001 through ADR-0007)
- Core architectural concepts and boundaries
- Basic documentation structure
- Master project guide references

### Content Duplicated Across Candidates
- Core ADR documents (particularly ADR-0001-Core-Boundary.md) - all branches contain similar content but main has the final accepted version
- Architecture decision indexes
- Basic documentation templates

### Content Genuinely Unique
- MASTER_DOCUMENTATION_ENTRY.md (import/copilot-current-state)
- GAIA_KNOWLEDGE_MATRIX.md (backup/repository-consolidation-accidental)
- RECONCILIATION_STATUS_MODEL.md (backup/repository-consolidation-accidental)
- FINAL_RECONCILIATION_SUMMARY.md (backup/repository-consolidation-accidental)
- GAIA_ENGINEER_AS_IS_REVIEW.md (backup/repository-consolidation-accidental)
- PHASE_2_DISCOVERY_REPORT.md (backup/repository-consolidation-accidental)
- references/README.md (backup/pre-copilot-import)

### Content That Conflicts with Current Reconciled Model
- ADR-0001-Core-Boundary.md in backup/pre-copilot-import branch has a different status and structure compared to the main branch version, but this is resolved by using the main branch's accepted version.

## 4. Recommended Sync Actions

### PROPOSED BASELINE SOURCE
The main branch represents the most current and complete canonical baseline with:
- Accepted ADRs
- Current documentation structure
- Integrated reconciliation work
- All core architectural elements

### PROPOSED IMPORTS
Based on analysis, the following content should be imported from other branches:

1. **MASTER_DOCUMENTATION_ENTRY.md** from import/copilot-current-state - Provides comprehensive master documentation entry that enhances understanding of the overall project structure.

2. **GAIA_KNOWLEDGE_MATRIX.md** from backup/repository-consolidation-accidental - Contains reconciliation documentation that provides context for how the knowledge matrix was developed.

3. **RECONCILIATION_STATUS_MODEL.md** from backup/repository-consolidation-accidental - Provides insight into how the reconciliation process was approached and managed.

4. **FINAL_RECONCILIATION_SUMMARY.md** from backup/repository-consolidation-accidental - Critical document that summarizes the reconciliation decisions and approach taken.

5. **GAIA_ENGINEER_AS_IS_REVIEW.md** from backup/repository-consolidation-accidental - Important for understanding current state of implementation-to-architecture alignment.

6. **PHASE_2_DISCOVERY_REPORT.md** from backup/repository-consolidation-accidental - Provides engineering discovery context for the approach taken.

### HISTORICAL MATERIAL TO PRESERVE
The following content should be preserved for historical reference:

1. **MASTER_DOCUMENTATION_ENTRY.md** from backup/pre-copilot-import - Early version of master documentation for understanding evolution.

2. **references/README.md** from backup/pre-copilot-import - Early reference documentation that provides historical context.

### UNRESOLVED ITEMS
1. The exact contents of the master documentation entry from import/copilot-current-state and backup/pre-copilot-import need to be compared in detail to ensure no conflicting information exists.
2. Some implementation-to-architecture mapping documents should be carefully reviewed for consistency with current baseline.
3. The specific reconciliation status model needs detailed review to understand how it differs from the current approach.

### HUMAN OWNER DECISIONS REQUIRED
1. Final approval on which version of MASTER_DOCUMENTATION_ENTRY.md to use (import/copilot-current-state vs backup/pre-copilot-import)
2. Confirmation that the imported documents don't introduce inconsistencies with the current baseline
3. Approval for preservation of historical references/README.md
4. Final verification that all reconciliation-related documentation is properly integrated and doesn't conflict with current state

## 5. Implementation Notes

This sync plan focuses on preserving canonical architecture while incorporating valuable reconciliation and documentation context without introducing conflicts or duplications. The main branch will remain the primary baseline, with selected content from other branches being imported to provide complete historical context and understanding.