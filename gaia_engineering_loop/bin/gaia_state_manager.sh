#!/usr/bin/env bash
set -u

# GAIA Engineering Loop State Manager
# This script handles the state management protocol for engineering loops

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "ERROR: must run inside the GAIA repository." >&2
  exit 10
fi
cd "$ROOT"

# State file location
STATE_DIR="gaia_engineering_loop/states"
STATE_FILE="$STATE_DIR/state.json"

# Valid states and actions
VALID_STATES=(
    "READY_FOR_TARGET_RUN"
    "TARGET_RUN_STARTED" 
    "TARGET_RUN_COMPLETE"
    "BLOCKED"
    "FAILED"
    "PASS"
    "ENGINEERING_ACTION_REQUIRED"
    "FIX_COMMITTED"
    "FIX_PUSHED"
    "ESCALATE_REVIEW"
)

# Create state directory if it doesn't exist
mkdir -p "$STATE_DIR"

# Validate state
validate_state() {
    local state=$1
    for valid_state in "${VALID_STATES[@]}"; do
        if [ "$state" = "$valid_state" ]; then
            return 0
        fi
    done
    return 1
}

# Initialize state file
initialize_state() {
    local loop_id=$1
    local timestamp=$(date -u +%Y%m%dT%H%M%SZ)
    
    cat > "$STATE_FILE" << EOF
{
  "loop_id": "$loop_id",
  "iteration": 0,
  "execution_mode": "physical",
  "source": "$(git rev-parse HEAD)",
  "target": "",
  "commit": "$(git rev-parse HEAD)",
  "timestamp": "$timestamp",
  "result": "READY_FOR_TARGET_RUN",
  "evidence": "",
  "next_action": "START_EXECUTION"
}
EOF
}

# Update state
update_state() {
    local loop_id=$1
    local result=$2
    local evidence_file=$3
    local target=$4
    
    # Read current state
    if [ -f "$STATE_FILE" ]; then
        local current_state=$(cat "$STATE_FILE")
    else
        initialize_state "$loop_id"
        local current_state=$(cat "$STATE_FILE")
    fi
    
    # Update the state
    local updated_state=$(echo "$current_state" | \
        jq --arg result "$result" '.result = $result' | \
        jq --arg evidence_file "$evidence_file" '.evidence = $evidence_file' | \
        jq --arg target "$target" '.target = $target')
    
    echo "$updated_state" > "$STATE_FILE"
}

# Get current state
get_current_state() {
    if [ -f "$STATE_FILE" ]; then
        jq -r '.result' "$STATE_FILE"
    else
        echo "UNKNOWN"
    fi
}

# Get loop info
get_loop_info() {
    if [ -f "$STATE_FILE" ]; then
        jq -r '.' "$STATE_FILE"
    else
        echo "No state file found"
    fi
}

# Main execution
case "${1:-help}" in
    "init")
        initialize_state "$2"
        echo "State initialized for loop $2"
        ;;
    "update")
        update_state "$2" "$3" "$4" "$5"
        echo "State updated"
        ;;
    "get")
        get_current_state
        ;;
    "info")
        get_loop_info
        ;;
    *)
        echo "Usage: $(basename "$0") {init|update|get|info} [args...]"
        echo "  init <loop_id>       - Initialize state for a loop"
        echo "  update <loop_id> <result> <evidence_file> <target> - Update state"
        echo "  get                  - Get current state"
        echo "  info                 - Get full loop information"
        exit 1
        ;;
esac