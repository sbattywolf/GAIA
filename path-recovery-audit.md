# GAIA Repository Path Recovery Audit

## 1. Migration/Path Problem Summary

The repository migration has caused several scripts and configurations to reference obsolete paths, particularly those that hard-code absolute paths to the old repository location.

## 2. Old → Current Path Mappings

| OLD PATH | CURRENT PATH | STATUS |
|----------|--------------|--------|
| /home/sbatta/github_repos/GAIA | /home/sbatta/github_repos/GAIA | VALID (same) |
| ~/github_repos/GAIA | ~/github_repos/GAIA | VALID (same) |

## 3. Broken References

### PATH-BROKEN References
- `./gaia_engineering_loop/lib/target_runner.sh`: Line 17 - `cd ~/github_repos/GAIA`
- `./gaia_engineering_loop/bin/gaia_orchestrator.sh`: Line 38 - `cd ~/github_repos/GAIA`
- `./gaia_target_preflight/gaia_preflight.py`: Line 34 - `workspace_path = "/home/sbatta/github_repos/GAIA"`

## 4. Repaired References

No references have been repaired yet. This is a pre-recovery audit.

## 5. Obsolete/Unused References

- `./software/legacy/oldRepoReference/` - This directory contains old repository material and should be left as-is for reference only.

## 6. Unresolved References

- All broken references need to be fixed to use relative paths or environment variables.
- The workspace path in gaia_preflight.py needs to be made dynamic.

## 7. Tests Performed

None - this is an audit document before any changes are made.

## 8. Files Whose Logic Was NOT Changed

This document only records the current state and does not modify any existing files.

## 9. Remaining Blockers

- Need to identify all scripts that reference the old paths
- Need to determine the correct approach for path resolution (relative vs environment variables)
- The repository structure should be maintained in a way that allows for future migrations without breaking paths