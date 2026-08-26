#!/bin/bash

# GAIA Target Runner Interface
# This script demonstrates the minimal capability to execute 
# target validation via SSH transport

set -e

# Configuration
TARGET_ALIAS="gaia-1070"
VALIDATION_SCRIPT="./gaia_1070_physical_validation/validate.sh"

echo "=== GAIA Target Runner Interface ==="

# Get repository root directory (path-independent)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
REPO_ROOT="$SCRIPT_DIR/.."  # Go up one level from script location to repo root

# Verify we're in the right location by checking for required directories
if [[ ! -d "$REPO_ROOT/gaia_1070_physical_validation" ]]; then
    echo "Error: Repository root not found or gaia_1070_physical_validation directory missing" >&2
    echo "Script directory: $SCRIPT_DIR" >&2
    echo "Repository root: $REPO_ROOT" >&2
    exit 1
fi

# Execute validation on target
echo "Executing target validation via SSH transport..."
ssh -o BatchMode=yes -o ConnectTimeout=5 "$TARGET_ALIAS" "bash -c 'cd \"$REPO_ROOT\" && $VALIDATION_SCRIPT'" 2>&1

echo "=== Target execution completed ==="
