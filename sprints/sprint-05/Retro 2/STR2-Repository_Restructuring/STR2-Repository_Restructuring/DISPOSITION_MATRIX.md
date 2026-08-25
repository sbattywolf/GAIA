STR2-Repository_Restructuring DISPOSITION MATRIX

This matrix outlines the disposition of repository items.

ITEMS TO KEEP (CANONICAL):
- docs/ - Documentation directory with ADRs and reference materials
- software/ - Software implementations 
- gaia-bootstrap-poc/ - Core bootstrap poc code
- README.md - Main repository documentation
- .gitignore - Git configuration
- AGENTS.md - Agent definitions
- MANIFEST.txt - Repository manifest

ITEMS TO MOVE:
- All root-level GAIA_* files and directories should be moved to appropriate locations
- oldRepoReferences/ should be moved to software/legacy/oldRepoReference/

ITEMS TO REMOVE:
- Empty directories: validation, reports, tools, src, scripts  
- Duplicate ADR files in docs/ and docs/adr/
- Uncommitted deletions from worktree (will be committed)

ITEMS TO BE CREATED:
- No new items required at this time

ITEMS TO REVIEW:
- All root-level items for proper categorization
- ADR structure to ensure semantic separation is maintained

ITEMS THAT ARE TEMPORARY:
- Files in sprint-05/STR2-Repository_Restructuring/ are temporary and will be cleaned up after final verification

NOTES:
1. The ADR files are duplicated - one set in docs/ and another in docs/adr/
2. Several empty directories should be removed
3. Root items that don't belong at root need to be moved to appropriate locations
4. The main repository structure is clean but needs minor cleanup
