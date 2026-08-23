#!/bin/bash

# GAIA Target Runner Interface
# This script demonstrates the minimal capability to execute 
# target validation via SSH transport

set -e

# Configuration
TARGET_ALIAS="gaia-1070"
VALIDATION_SCRIPT="./gaia_1070_physical_validation/validate.sh"

echo "=== GAIA Target Runner Interface ==="

# Execute validation on target
echo "Executing target validation via SSH transport..."
ssh -o BatchMode=yes -o ConnectTimeout=5 "$TARGET_ALIAS" "bash -c 'cd ~/github_repos/GAIA && $VALIDATION_SCRIPT'" 2>&1

echo "=== Target execution completed ==="
