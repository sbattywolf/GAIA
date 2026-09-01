# GAIA Baseline Candidate Manifest

## 1. Proposed Baseline Scope

This manifest defines the candidate files and directories intended for inclusion in the future GAIA documentation baseline, organized according to their classification status.

## 2. Files/Directories Included

### CANONICAL-DOCS
- README.md
- docs/adr/
- docs/gaia_knowledge_matrix/MASTER_DOCUMENTATION_ENTRY.md
- docs/gaia_knowledge_matrix/GAIA_KNOWLEDGE_MATRIX.md

### CANONICAL-ADR
- docs/adr/ADR-0001-Core-Boundary.md
- docs/adr/ADR-0002-Memory-Semantics.md
- docs/adr/ADR-0003-Capability-Model.md
- docs/adr/ADR-0004-HomeAssistant-Boundary.md
- docs/adr/ADR-0005-Communication-State.md
- docs/adr/ADR-0006-Tool-Trust.md
- docs/adr/ADR-0007-Event-Semantics.md

### CANONICAL-REFERENCE
- references/
- sprints/sprint-01/
- sprints/sprint-02/
- sprints/sprint-03/
- sprints/sprint-04/
- sprints/sprint-05/
- sprints/sprint-06/
- sprints/sprint-07/

### HISTORICAL-EVIDENCE
- docs/gaia_knowledge_matrix/KNOWLEDGE_MATRIX_AUDIT.md
- docs/gaia_knowledge_matrix/RECONCILIATION_STATUS_MODEL.md

### IMPLEMENTATION
- gaia_xxx directories (implementation sources)
- evidence/ directory

### OPERATIONAL
- gaia_1070_model_runtime/
- gaia_3090_model_stack/

### LEGACY-REFERENCE
- old repository forks and references

### EXCLUDE-FROM-BASELINE
- docs/gaia_knowledge_matrix/AD_HOC_RESEARCH_INVENTORY.md (secondary evidence only)
- Temporary files and backups
- Dockerfiles, compose files, test scripts that are implementation artifacts

### UNKNOWN
- Files that require further analysis or classification

## 3. Files/Directories Excluded

### EXCLUDE-FROM-BASELINE
- docs/gaia_knowledge_matrix/AD_HOC_RESEARCH_INVENTORY.md
- Temporary and backup files
- Implementation-specific runtime files (except for operational references)
- gaia_xxx directories (implementation sources)
- evidence/ directory (implementation evidence)
- Dockerfiles, compose files, test scripts that are implementation artifacts

## 4. Historical Evidence Retained but Not Canonical

The following historical evidence is retained but not considered canonical GAIA architecture:

- docs/gaia_knowledge_matrix/KNOWLEDGE_MATRIX_AUDIT.md
- docs/gaia_knowledge_matrix/RECONCILIATION_STATUS_MODEL.md

These documents represent the reconciliation process and methodology, not the core architectural definitions.

## 5. Implementation/Runtime Material

The following directories contain implementation/runtime material that should be classified separately:

- gaia_1070_model_runtime/
- gaia_3090_model_stack/
- evidence/

These are implementation artifacts and should not be included in the canonical documentation baseline.

## 6. Legacy/Secondary References

The following items are classified as legacy references and should not be considered canonical architecture:

- Old repository forks and branches
- Legacy reference documentation directories
- Historical evidence from previous versions that has been superseded

## 7. Unresolved/Unknown Items

- The exact contents of gaia_xxx directories require further classification 
- Some files in the sprints/ directory may need individual review
- Implementation artifacts in the evidence/ directory should be classified separately

## 8. Candidate Branches for Later Comparison

### main (Canonical baseline)
- SHA: 208d1735
- Purpose: Main repository baseline
- Contains material potentially useful to baseline

### import/copilot-current-state  
- SHA: d9e8e91a
- Purpose: Direct import from Copilot 
- Contains evolution path and state transitions

### backup/pre-copilot-import
- SHA: 9805a86f
- Purpose: First documentation
- Contains early documentation baseline

### backup/repository-consolidation-accidental
- SHA: cde5db28
- Purpose: Repository consolidation attempt
- May contain useful historical context

### AP6ST1_git_master_remote_repo
- SHA: 56d5baa3
- Purpose: External reference
- Contains remote master baseline

## 9. Rules for Synchronizing to Remote Repository

1. Only files explicitly classified as CANONICAL-* should be synchronized to the remote repository
2. Historical evidence should be preserved but marked separately from canonical documentation
3. Implementation artifacts should remain separate from documentation baseline
4. All synchronization must maintain file structure and naming conventions
5. Branch comparison should only occur after baseline finalization
6. No automatic merging of candidate branches should be performed
7. All changes to the baseline must be committed with clear descriptions

## 10. Repository Entry Point Update

The manifest is intentionally kept separate from the README to maintain a clean distinction between the documentation baseline and its own description.

This manifest represents the current state of candidate files for inclusion in the GAIA documentation baseline, based on the reconciliation work completed through Sprint 7.