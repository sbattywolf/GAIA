# GAIA Target Host Preflight Utility

This utility verifies that a target machine is ready to execute GAIA experimental test/runtime procedures without interactive privilege escalation.

## Purpose

- Verify host readiness for GAIA experiments
- Check essential prerequisites without modifying the system
- Provide structured, machine-readable evidence
- Maintain minimal implementation focused on experimental needs

## Usage

```bash
# Run preflight check
python3 gaia_preflight.py

# Run with verbose output
python3 gaia_preflight.py --verbose

# Generate JSON evidence file
python3 gaia_preflight.py --output evidence.json
```

## Checks Performed

- Host information (hostname, OS, kernel, architecture)
- User and group membership
- Docker availability and access
- NVIDIA GPU information (if available)
- Ollama host installation status
- Workspace and filesystem requirements
- Port availability for experiments