#!/usr/bin/env bash
set -u

# GAIA Target Adapter
# This script provides a generic interface for different target execution modes

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "ERROR: must run inside the GAIA repository." >&2
  exit 10
fi
cd "$ROOT"

# Load configuration
source "$(dirname "$0")/../config/defaults.env"

# Load inventory utilities
source "$(dirname "$0")/../lib/inventory_utils.sh"

# Target execution function
execute_target() {
    local target=$1
    local mode=$2
    
    log "Executing target $target in $mode mode"
    
    case "$mode" in
        "physical")
            execute_physical "$target"
            ;;
        "simulated")
            execute_simulated "$target"
            ;;
        *)
            echo "ERROR: Unknown execution mode '$mode'" >&2
            return 1
            ;;
    esac
}

# Physical execution
execute_physical() {
    local target=$1
    
    log "Physical execution for target $target"
    
    # This would normally execute the actual validation runner
    # For now, we'll use a placeholder that mimics what the real runner does
    
    # Check if the target runner exists
    if [ ! -f "$RUNNER" ]; then
        echo "ERROR: Runner script not found at $RUNNER" >&2
        return 1
    fi
    
    # Execute with proper environment
    export VALIDATION_TARGET="$target"
    
    # Run the validation script (this is where the actual validation happens)
    if bash "$RUNNER"; then
        echo "Physical execution successful for target $target"
        return 0
    else
        echo "Physical execution failed for target $target"
        return 1
    fi
}

# Simulated execution - this calls our orchestrator for testing
execute_simulated() {
    local target=$1
    
    log "Simulated execution for target $target"
    
    # For simulated mode, we can:
    # 1. Mock the validation process 
    # 2. Run with different parameters
    # 3. Use pre-defined test scenarios
    
    # In a real implementation, this would call the orchestrator or transport layer
    # For now, let's simulate by calling our orchestrator directly for testing
    
    echo "Simulated execution completed for target $target"
    
    # Return success to simulate successful execution
    return 0
}

# Load target inventory and configuration
load_target_inventory() {
    local target_id=$1
    
    log "Loading inventory for target $target_id"
    
    # This would normally load from gaia_target_inventory/targets/$target_id/declared_config.json
    # For now, we'll just return a mock configuration
    echo "{\"target_id\": \"$target_id\", \"hostname\": \"gaia-1070.local\"}"
}

# Log function
log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1"
}

# Main execution
main() {
    local target=${1:-$VALIDATION_TARGET}
    local mode=${2:-$TARGET_MODE}
    
    execute_target "$target" "$mode"
}

# Run main function if script is called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi