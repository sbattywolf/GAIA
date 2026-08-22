#!/bin/bash

# GAIA 1070 Physical Validation - Evidence Assembler
# This module reads structured validation results and produces 
# the final validation_evidence.json file.

set -e  # Exit on any error

# Initialize variables
OVERALL_STATUS="UNKNOWN"
BLOCKING=false

# Function to log messages
log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1"
}

# Function to fail-fast with error
fail_fast() {
    local message=$1
    log "ERROR: $message"
    echo "Validation FAILED: $message" >&2
    exit 1
}

# Function to validate JSON input
validate_json() {
    local json_file=$1
    
    if [ ! -f "$json_file" ]; then
        fail_fast "Input file not found: $json_file"
    fi
    
    if ! jq empty "$json_file" >/dev/null 2>&1; then
        fail_fast "Invalid JSON in input file: $json_file"
    fi
}

# Function to check module status and determine overall status
check_module_status() {
    local json_file=$1
    local module_status
    local module_blocking
    local module_target
    
    module_status=$(jq -r '.status' "$json_file")
    module_blocking=$(jq -r '.blocking' "$json_file")
    module_target=$(jq -r '.target' "$json_file")
    
    # Validate status values
    if [[ ! "$module_status" =~ ^(PASS|FAIL|BLOCKED|NOT_RUN)$ ]]; then
        fail_fast "Invalid status value in $json_file: $module_status"
    fi
    
    # Determine overall status based on module results
    case "$OVERALL_STATUS" in
        "UNKNOWN")
            OVERALL_STATUS="$module_status"
            BLOCKING="$module_blocking"
            ;;
        "PASS")
            if [ "$module_status" = "FAIL" ] || [ "$module_status" = "BLOCKED" ]; then
                OVERALL_STATUS="$module_status"
                BLOCKING="$module_blocking"
            fi
            ;;
        "BLOCKED")
            if [ "$module_status" = "FAIL" ]; then
                OVERALL_STATUS="$module_status"
                BLOCKING="$module_blocking"
            fi
            ;;
        "FAIL")
            # FAIL takes precedence, no change needed
            ;;
    esac
}

# Function to create final evidence structure
create_evidence() {
    local module_files=("$@")
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Initialize the overall result with actual module data
    echo "{"
    echo '  "target": "1070",'
    echo '  "validation_type": "1070_PHYSICAL",'
    echo '  "timestamp": "'$timestamp'",'
    echo '  "modules": ['

    # Add each module result
    for i in "${!module_files[@]}"; do
        if [ "$i" -gt 0 ]; then
            echo "    ,"
        fi
        cat "$module_files[$i]"
    done
    
    echo "  ],"
    echo '  "overall_status": "'$OVERALL_STATUS'",'
    echo '  "provenance": {'
    echo '    "generated_by": "evidence_assembler",'
    echo '    "runtime_observation": true'
    echo '  }'
    echo '}'
}

# Main execution logic
log "Starting evidence assembly"

# Check if input files are provided
if [ $# -eq 0 ]; then
    log "No module results provided, creating empty validation result"
    OVERALL_STATUS="NOT_RUN"
    BLOCKING=false
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Create minimal valid output
    echo "{"
    echo '  "target": "1070",'
    echo '  "validation_type": "1070_PHYSICAL",'
    echo '  "timestamp": "'$timestamp'",'
    echo '  "modules": [],'
    echo '  "overall_status": "NOT_RUN",'
    echo '  "provenance": {'
    echo '    "generated_by": "evidence_assembler",'
    echo '    "runtime_observation": true'
    echo '  }'
    echo '}'
    exit 0
fi

# Process all input files
for module_file in "$@"; do
    validate_json "$module_file"
    check_module_status "$module_file"
done

# Create the final evidence file with actual module data
create_evidence "$@"