#!/bin/bash

# GAIA 1070 Physical Validation - Model Inventory Module
# This module inspects the currently reachable model inventory and produces 
# a structured validation result.

set -e  # Exit on any error

# Initialize variables
MODULE_NAME="model_inventory"
STATUS="NOT_RUN"
BLOCKING=false
REASON=""
OBSERVED={}
EXPECTED={}
EVIDENCE={}

# Function to log messages
log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1"
}

# Function to fail-fast with error and cleanup
fail_fast() {
    local message=$1
    log "ERROR: $message"
    STATUS="FAIL"
    BLOCKING=true
    REASON="$message"
    exit 1
}

# Function to create structured output
create_output() {
    cat << EOF
{
  "module": "$MODULE_NAME",
  "target": "1070",
  "status": "$STATUS",
  "blocking": $BLOCKING,
  "reason": "$REASON",
  "observed": $OBSERVED,
  "expected": $EXPECTED,
  "evidence": $EVIDENCE
}
EOF
}

# Function to determine actual host target
determine_target() {
    # In a real implementation, this would detect the physical hardware
    # For now we just return that we expect 1070 but don't fabricate identity
    
    # We check if we can determine the physical environment via system commands
    if command -v nvidia-smi >/dev/null 2>&1; then
        # If we can detect NVIDIA hardware, check for 1070 specifically
        GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits)
        if [[ "$GPU_INFO" == *"GeForce RTX 3070"* ]] || [[ "$GPU_INFO" == *"RTX 3070"* ]]; then
            # This is a 1070 target - but we still need to be cautious about fabricating identity
            echo "1070"
        else
            # We found NVIDIA hardware but not the expected 1070, so we can't confirm target
            echo "unknown"
        fi
    else
        # No NVIDIA hardware detected or nvidia-smi not available
        echo "unknown"
    fi
}

# Main execution logic
log "Starting model inventory module validation"

# Check if Ollama is available
if ! command -v curl >/dev/null 2>&1; then
    STATUS="FAIL"
    BLOCKING=true
    REASON="curl is not available to query Ollama API"
    create_output
    exit 1
fi

# Try to get model inventory from Ollama API
MODEL_INVENTORY_JSON=""
if command -v curl >/dev/null 2>&1; then
    # Attempt to fetch models from Ollama API
    MODEL_INVENTORY_JSON=$(curl -s http://localhost:11434/api/tags 2>/dev/null)
    
    if [ -z "$MODEL_INVENTORY_JSON" ]; then
        STATUS="FAIL"
        BLOCKING=true
        REASON="Failed to connect to Ollama API at localhost:11434"
        create_output
        exit 1
    fi
    
    # Validate JSON
    if ! echo "$MODEL_INVENTORY_JSON" | jq empty >/dev/null 2>&1; then
        STATUS="FAIL"
        BLOCKING=true
        REASON="Invalid JSON response from Ollama API"
        create_output
        exit 1
    fi
    
    # Extract model names and count
    MODEL_COUNT=$(echo "$MODEL_INVENTORY_JSON" | jq -r '.models | length')
    
    if [ "$MODEL_COUNT" = "0" ]; then
        STATUS="FAIL"
        BLOCKING=false
        REASON="No models found in Ollama inventory"
        create_output
        exit 1
    fi
    
    # Create model list array for observed data
    MODEL_LIST=$(echo "$MODEL_INVENTORY_JSON" | jq -r '.models[].name')
    
    # Build observed data structure - we don't fabricate hardware identity here
    OBSERVED="{\"model_count\": $MODEL_COUNT, \"models\": [$(echo "$MODEL_LIST" | sed 's/.*/"&"/' | paste -sd ',')]}"

    STATUS="PASS"
    BLOCKING=false
    REASON="Successfully retrieved model inventory from Ollama API"
else
    # Fallback when curl is not available
    STATUS="FAIL"
    BLOCKING=true
    REASON="curl command not found to query Ollama API"
    create_output
    exit 1
fi

# Create and output structured result
create_output