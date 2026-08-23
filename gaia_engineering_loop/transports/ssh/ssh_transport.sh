#!/usr/bin/env bash
set -u

# GAIA SSH Transport Wrapper
# This script provides a shell interface to the Python SSH transport layer

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "ERROR: must run inside GAIA repository." >&2
  exit 10
fi

cd "$ROOT"

# Configuration
TRANSPORT_SCRIPT="gaia_engineering_loop/transports/ssh/transport.py"
LOG_FILE="gaia_engineering_loop/logs/ssh_transport.log"

# Create logs directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

# Function to execute SSH command and return structured result
execute_ssh_command() {
    local target=$1
    local command=$2
    
    # Validate inputs
    if [[ -z "$target" || -z "$command" ]]; then
        log "ERROR: Target and command must be provided"
        echo '{"event": "TRANSPORT_FAILURE", "layer": "transport", "retryable": false, "component": "ssh_transport", "reason": "invalid_parameters", "success": false}'
        return 1
    fi
    
    # Try to get target configuration from inventory
    local target_config_file="gaia_target_inventory/targets/$target/declared_config.json"
    if [[ ! -f "$target_config_file" ]]; then
        log "ERROR: Target configuration not found for $target"
        echo '{"event": "TRANSPORT_FAILURE", "layer": "transport", "retryable": false, "component": "ssh_transport", "reason": "target_not_found", "success": false}'
        return 1
    fi
    
    # Get hostname from target config (we'll need to parse this properly)
    local hostname=$(grep -o '"hostname": "[^"]*"' "$target_config_file" | cut -d'"' -f4)
    
    if [[ -z "$hostname" ]]; then
        log "ERROR: Hostname not found in target configuration for $target"
        echo '{"event": "TRANSPORT_FAILURE", "layer": "transport", "retryable": false, "component": "ssh_transport", "reason": "hostname_missing", "success": false}'
        return 1
    fi
    
    # Execute Python transport with hostname and command
    python3 "$TRANSPORT_SCRIPT" "$hostname" "$command"
}

# Main execution logic
if [[ $# -lt 2 ]]; then
    log "Usage: $0 <target> <command>"
    echo '{"event": "TRANSPORT_FAILURE", "layer": "transport", "retryable": false, "component": "ssh_transport", "reason": "insufficient_parameters", "success": false}'
    exit 1
fi

TARGET=$1
COMMAND=$2

# Execute the command
execute_ssh_command "$TARGET" "$COMMAND"