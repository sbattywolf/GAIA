#!/usr/bin/env bash
set -u
set -o pipefail

# GAIA Engineering Loop Orchestrator
# This script provides orchestration and supervision for the engineering loop
# including error classification, recovery, and retry logic

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "ERROR: must run inside the GAIA repository." >&2
  exit 10
fi
cd "$ROOT"

# Load configuration
source "$(dirname "$0")/../config/defaults.env"

# Load commit utilities
source "$(dirname "$0")/../lib/commit_utils.sh"

# Load target adapter
source "$(dirname "$0")/gaia_target_adapter.sh"

# Logging function
log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1"
}

# Function to verify commit binding between requested and observed commits
verify_commit_binding() {
    local requested_commit=$1
    local target=$2
    
    log "Verifying commit binding for target $target"
    
    # Get the repository root directory (path-independent)
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
    REPO_ROOT="${SCRIPT_DIR%/gaia_engineering_loop/bin}"  # Remove last path component to get repo root
    
    # Get the observed commit from the target
    local observed_commit=$(ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "cd \"$REPO_ROOT\" && git rev-parse HEAD" 2>/dev/null || echo "ERROR")
    
    if [[ "$observed_commit" == "ERROR" ]]; then
        log "Unable to determine observed commit from target $target"
        echo "{\"event\": \"TRANSPORT_FAILURE\", \"layer\": \"transport\", \"retryable\": false, \"component\": \"target_adapter\", \"reason\": \"commit_observation_failed\"}"
        return 255
    fi
    
    log "Requested commit: $requested_commit"
    log "Observed commit: $observed_commit"
    
    # Compare requested and observed commits
    if [[ "$requested_commit" == "$observed_commit" ]]; then
        log "Commit binding verified successfully"
        echo "{\"event\": \"COMMIT_BINDING_SUCCESS\", \"layer\": \"target\", \"commit\": \"$observed_commit\"}"
        return 0
    else
        log "Commit binding failed: requested $requested_commit != observed $observed_commit"
        echo "{\"event\": \"COMMIT_BINDING_FAILURE\", \"layer\": \"target\", \"requested\": \"$requested_commit\", \"observed\": \"$observed_commit\", \"reason\": \"stale_target\"}"
        return 1
    fi
}

# Function to classify and handle execution failures
classify_execution_failure() {
    local exit_code=$1
    local error_message=$2
    local component=$3
    
    log "Classifying execution failure: $error_message (exit code: $exit_code, component: $component)"
    
    # Return structured result for the orchestrator to process
    case "$exit_code" in
        255)
            # SSH connection error or timeout
            echo "{\"event\": \"TRANSPORT_FAILURE\", \"layer\": \"transport\", \"retryable\": true, \"component\": \"$component\", \"reason\": \"connection_error\"}"
            return 255
            ;;
        127)
            # Command not found - likely orchestration failure
            echo "{\"event\": \"ORCHESTRATION_FAILURE\", \"layer\": \"orchestration\", \"retryable\": true, \"component\": \"$component\", \"reason\": \"command_not_found\"}"
            return 127
            ;;
        *)
            # Other failures are typically target execution failures
            echo "{\"event\": \"TARGET_EXECUTION_FAILURE\", \"layer\": \"target\", \"retryable\": false, \"component\": \"$component\", \"exit_code\": $exit_code}"
            return $exit_code
            ;;
    esac
}

# Function to simulate a target execution with various failure modes
simulate_target_execution() {
    local target=$1
    local mode=$2
    local test_case=$3
    
    log "Simulating target execution for $target in mode $mode with test case $test_case"
    
    # This would normally delegate to the transport adapter, but we simulate here
    case "$test_case" in
        "pass")
            log "Simulating PASS result"
            echo "{\"event\": \"TARGET_RESULT\", \"layer\": \"target\", \"result\": \"PASS\", \"exit_code\": 0}"
            return 0
            ;;
        "fail")
            log "Simulating FAIL result"
            echo "{\"event\": \"TARGET_RESULT\", \"layer\": \"target\", \"result\": \"FAIL\", \"exit_code\": 1}"
            return 1
            ;;
        "blocked")
            log "Simulating BLOCKED result"
            echo "{\"event\": \"TARGET_RESULT\", \"layer\": \"target\", \"result\": \"BLOCKED\", \"exit_code\": 2}"
            return 2
            ;;
        "unknown")
            log "Simulating UNKNOWN result"
            echo "{\"event\": \"TARGET_RESULT\", \"layer\": \"target\", \"result\": \"UNKNOWN\", \"exit_code\": 3}"
            return 3
            ;;
        "invalid")
            log "Simulating INVALID result"
            echo "{\"event\": \"TARGET_RESULT\", \"layer\": \"target\", \"result\": \"INVALID\", \"exit_code\": 4}"
            return 4
            ;;
        "transport_timeout")
            log "Simulating transport timeout failure"
            classify_execution_failure 255 "SSH connection timeout" "ssh_transport"
            return 255
            ;;
        "command_not_found")
            log "Simulating command not found failure"
            classify_execution_failure 127 "Command not found" "target_runner"
            return 127
            ;;
        "runner_crash")
            log "Simulating runner crash"
            classify_execution_failure 134 "Runner process crashed" "target_runner"
            return 134
            ;;
        *)
            log "Simulating unknown failure"
            echo "{\"event\": \"ORCHESTRATION_FAILURE\", \"layer\": \"orchestration\", \"retryable\": true, \"component\": \"simulation\", \"reason\": \"unknown_test_case\"}"
            return 1
            ;;
    esac
}

# Main orchestrator function that handles the complete loop execution
orchestrate_loop() {
    local requested_commit="$1"
    local iteration="$2"
    
    log "Starting orchestration for commit $requested_commit, iteration $iteration"
    
    # First verify commit binding
    local binding_result=$(verify_commit_binding "$requested_commit" "gaia-1070")
    local binding_exit_code=$?
    
    # Check if commit binding was successful
    local binding_event=$(echo "$binding_result" | jq -r '.event' 2>/dev/null || echo "UNKNOWN")
    
    if [[ "$binding_event" == "COMMIT_BINDING_FAILURE" ]]; then
        log "Commit binding failed, generating STALE_TARGET evidence"
        # Create evidence file for stale target
        local timestamp=$(date -u +%Y%m%dT%H%M%SZ)
        local evidence_file="evidence/stale_target_${requested_commit}_${timestamp}.json"
        
        # Create structured evidence for STALE_TARGET
        cat > "$evidence_file" << EOF
{
  "event": "STALE_TARGET",
  "layer": "target",
  "requested_commit": "$requested_commit",
  "observed_commit": "$(echo "$binding_result" | jq -r '.observed' 2>/dev/null || echo 'unknown')",
  "target": "gaia-1070",
  "timestamp": "$timestamp",
  "reason": "stale_target"
}
EOF
        
        # Update state with STALE_TARGET result
        "$(dirname "$0")/../bin/gaia_state_manager.sh" update "loop_$(date +%s)" "STALE_TARGET" "$evidence_file" "gaia-1070"
        
        log "STALE_TARGET evidence created: $evidence_file"
        echo "$binding_result"
        return 1
    elif [[ "$binding_event" == "TRANSPORT_FAILURE" ]]; then
        log "Transport failure during commit observation"
        echo "$binding_result"
        return $binding_exit_code
    fi
    
    # Initialize variables
    local result="UNKNOWN"
    local attempt=0
    local max_attempts=3
    local retryable=false
    
    # Execute target validation (only if commit binding was successful)
    while [[ $attempt -lt $max_attempts ]]; do
        attempt=$((attempt + 1))
        log "Attempt $attempt/$max_attempts for commit $requested_commit"
        
        # Execute physical target validation via target adapter
        local execution_result=$(execute_target "gaia-1070" "physical")
        local exit_code=$?
        
        log "Execution result: $execution_result"
        
        # Parse the result to determine if it's a structured event
        local event_type=$(echo "$execution_result" | jq -r '.event' 2>/dev/null || echo "TARGET_RESULT")
        
        case "$event_type" in
            "TRANSPORT_FAILURE")
                local retryable=$(echo "$execution_result" | jq -r '.retryable')
                if [[ "$retryable" == "true" ]]; then
                    log "Recoverable transport failure, attempting retry..."
                    sleep 1  # Brief delay before retry
                    continue  # Retry the execution
                else
                    log "Non-recoverable transport failure"
                    echo "$execution_result"
                    return 255
                fi
                ;;
            "TARGET_RESULT")
                # This is a successful target result - process and create evidence
                result=$(echo "$execution_result" | jq -r '.result')
                log "Target execution completed with result: $result"
                
                # Create evidence file for the result
                local timestamp=$(date -u +%Y%m%dT%H%M%SZ)
                local evidence_file="evidence/target_${result}_${requested_commit}_${timestamp}.json"
                
                # Create structured evidence based on result type
                cat > "$evidence_file" << EOF
{
  "event": "TARGET_RESULT",
  "layer": "target",
  "result": "$result",
  "requested_commit": "$requested_commit",
  "target": "gaia-1070",
  "timestamp": "$timestamp",
  "exit_code": $exit_code
}
EOF
                
                # Update state with the result and evidence file path
                "$(dirname "$0")/../bin/gaia_state_manager.sh" update "loop_$(date +%s)" "$result" "$evidence_file" "gaia-1070"
                
                log "Evidence created: $evidence_file"
                echo "$execution_result"
                return 0
                ;;
            *)
                # Handle other types of results
                log "Got unclassified result: $execution_result"
                echo "$execution_result"
                return $exit_code
                ;;
        esac
    done
    
    # If we get here, all retries failed
    log "All attempts failed after $max_attempts tries"
    echo "{\"event\": \"ORCHESTRATION_FAILURE\", \"layer\": \"orchestration\", \"retryable\": false, \"reason\": \"max_retries_exceeded\"}"
    return 1
}

# Function to run a complete loop iteration
run_loop_iteration() {
    local requested_commit="$1"
    local iteration="$2"
    
    log "Running loop iteration $iteration for commit $requested_commit"
    
    # Run the orchestrated execution
    local result=$(orchestrate_loop "$requested_commit" "$iteration")
    local exit_code=$?
    
    log "Iteration $iteration completed with result: $result"
    
    # Process the result to determine next action
    local event_type=$(echo "$result" | jq -r '.event' 2>/dev/null || echo "TARGET_RESULT")
    
    case "$event_type" in
        "TARGET_RESULT")
            local semantic_result=$(echo "$result" | jq -r '.result')
            log "Final semantic result: $semantic_result"
            
            # Return appropriate exit code based on result
            case "$semantic_result" in
                "PASS") return 0 ;;
                "FAIL") return 1 ;;  
                "BLOCKED") return 2 ;;
                "UNKNOWN") return 3 ;;
                "STALE_TARGET") return 4 ;;
                *) return 1 ;;
            esac
            ;;
        "COMMIT_BINDING_FAILURE")
            # For stale target, return exit code 4 to indicate this specific failure
            log "Returning exit code 4 for STALE_TARGET result"
            return 4
            ;;
        *)
            # For failures, return error code based on classification
            log "Returning error due to orchestration failure"
            return 1
            ;;
    esac
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <requested_commit> <iteration>" >&2
        exit 1
    fi
    
    REQUESTED_COMMIT="$1"
    ITERATION="$2"
    
    run_loop_iteration "$REQUESTED_COMMIT" "$ITERATION"
fi