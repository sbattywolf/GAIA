# GAIA 1070 Physical Validation Package

This package contains all necessary components to perform a complete validation of the physical 1070 target host.

## Overview

This self-contained package enables the Human Owner to validate that the physical 1070 target host is properly configured and ready for GAIA model deployment. The validation process includes:

1. Target Host Preflight (automatic guard)
2. Hardware and resource discovery
3. Docker / Compose / NVIDIA verification
4. Ollama discovery and availability check
5. Model inventory inspection
6. Isolated runtime validation
7. Resource observation
8. Cleanup and evidence generation

## Usage

To run the validation on the physical 1070 target host:

```bash
./run_1070_validation.sh
```

The script will:
- Automatically execute all preflight checks
- Validate system prerequisites
- Check Ollama availability 
- Inspect model inventory
- Run isolated runtime validation
- Generate machine-readable evidence
- Clean up after execution

## Requirements

- Python 3.x
- Docker Engine
- NVIDIA drivers with nvidia-smi available
- Ollama service running on localhost:11434

## Output

The validation will generate:
- `validation_evidence.json` - Machine-readable evidence file
- Console output with human-readable summary

## Important Notes

- This package must be copied from the 3090 engineering host to the physical 1070 target
- No model downloads or pulls are performed automatically
- Only existing models in the Ollama inventory are validated
- The script will fail-fast if any prerequisite is not met
- All cleanup is limited to experiment runtime only

## Validation Result

The final result will be one of:
- **PASS**: All validations passed successfully
- **FAIL**: Validation failed with specific error message  
- **BLOCKED**: Prerequisites not met requiring Human Owner action

## Evidence Structure

Generated evidence distinguishes between:
- **OBSERVED**: Directly measured data
- **HISTORICAL**: Previously validated information
- **RECOMMENDED**: Next steps or actions
- **NOTES**: Additional contextual information

## Transferability

This package is completely self-contained and does not require Git or any repository access on the target host.