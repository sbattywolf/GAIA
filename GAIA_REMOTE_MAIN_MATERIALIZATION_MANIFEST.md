# GAIA REMOTE MAIN MATERIALIZATION MANIFEST

## File Classification and Disposition

### CANONICAL
- README.md - Core repository documentation and identity
- docs/ - Documentation directory with architectural and design information
- .github/ - GitHub workflows and configuration for governance
- AGENTS.md - Engineering agent definitions and authority semantics
- .github/instructions/ - Instructional materials for contributors
- .github/skills/ - Skills required for collaboration

### IMPLEMENTATION
- gaia_engineering_loop/ - Engineering loop infrastructure
- gaia_target_inventory/ - Target inventory documentation
- gaia_target_preflight/ - Preflight checks and validation

### EVIDENCE
- gaia_3090_model_stack/ - GAIA 3090 model stack implementation
- gaia_1070_model_runtime/ - GAIA 1070 model runtime components
- gaia_1070_evidence/ - Evidence and testing for GAIA 1070

### EXPERIMENT/SOFTWARE/TOOL
- software/ - Software components and tools related to GAIA
- experiments/ - Experimental implementations and research work
- tools/ - Development, testing, and operational tools

### HISTORICAL/LEGACY
- oldRepoReference/ - Historical reference material only (no promotion)

### EXCLUDE
- sprint directories - Source material for provenance/reconciliation, not core content
- .env files - Runtime secrets excluded
- runtime directories - Generated/cached material excluded
- build directories - Generated output excluded
- cache directories - Temporary files excluded
- logs and temporary files - Private information excluded
- private infrastructure - Machine-specific configurations excluded
- model data - Large binary files excluded
- credentials - Security-sensitive information excluded

## Disposition Summary

### Promote (Include in Remote Main)
- CANONICAL: 4 files/directories
- IMPLEMENTATION: 3 files/directories  
- EVIDENCE: 3 files/directories
- EXPERIMENT/SOFTWARE/TOOL: 3 files/directories

### Exclude (Not Include in Remote Main)
- HISTORICAL/LEGACY: 1 directory
- EXCLUDE: Multiple categories of files

## Provenance and Source

All materials are derived from the GAIA reconciliation state established during ING_3090 work. The baseline represents a coherent set of artifacts required to make the GAIA baseline self-contained and understandable.

This materialization reflects the accepted architectural authority (ADR references) and governance semantics that define the core identity and operational framework of the GAIA project.