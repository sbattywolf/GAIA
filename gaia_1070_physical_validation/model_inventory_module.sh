#!/bin/bash

# GAIA 1070 Physical Validation - Model Inventory Module
# This module inspects the currently reachable model inventory and produces 
# a structured validation result.

set -e  # Exit on any error

# Initialize variables
MODULE_NAME="model_inventory"
TARGET_HOST="1070"
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
  "target": "$TARGET_HOST",
  "status": "$STATUS",
  "blocking": $BLOCKING,
  "reason": "$REASON",
  "observed": $OBSERVED,
  "expected": $EXPECTED,
  "evidence": $EVIDENCE
}
EOF
}

# Main execution logic
log "Starting model inventory module validation"

# Check if we're running on the correct target host
if [ "$TARGET_HOST" != "1070" ]; then
    STATUS="NOT_RUN"
    BLOCKING=false
    REASON="Target mismatch: This script should only run on 1070 target"
    create_output
    exit 0
fi

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
    
    # Build observed data structure
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