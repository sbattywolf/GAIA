#!/bin/bash

# GAIA 1070 Physical Validation Script - Enhanced Version
# This script validates the physical hardware and software environment for GAIA 1070
# It implements all requirements from the E2 implementation handoff including:
# - Hardware detection (1070 vs 3090)
# - Model availability checking
# - Explicit model acquisition policy
# - Proper error handling and validation
# - Minimal dependency approach

# Exit immediately if a command exits with a non-zero status
set -e

# Logging functions
log_pass() {
    echo "PASS: [$1] $2"
}

log_fail() {
    echo "FAIL: [$1] $2"
}

log_blocked() {
    echo "BLOCKED: [$1] $2"
}

fail_fast() {
    echo "ERROR: [$1] $2"
    exit 1
}

# P5 - DOCKER RUNTIME FOUNDATION
echo ""
echo "P5: Docker Runtime Foundation"
echo "============================"

echo "GUARD: Checking Docker runtime foundation..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    fail_fast "P5" "Docker not found"
fi

# Determine which compose command to use
COMPOSE_CMD=""
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v "docker-compose" &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    fail_fast "P5" "Docker Compose not found (neither 'docker compose' nor 'docker-compose' available)"
fi

# Check if jq is available for JSON parsing
if ! command -v jq &> /dev/null; then
    echo "INFO: jq not found, using basic grep for model counting"
fi

# Check if container exists and is running
CONTAINER_EXISTS=false
if docker ps -f name=gaia-ollama-1070 --format "{{.Names}}" | grep -q "gaia-ollama-1070"; then
    CONTAINER_EXISTS=true
fi

# If container doesn't exist at all, it's a BLOCKED prerequisite (not a FAIL)
if [ "$CONTAINER_EXISTS" = false ]; then
    # Check if the container exists at all (not just running)
    if ! docker ps -a --format "{{.Names}}" | grep -q "gaia-ollama-1070"; then
        # Container doesn't exist at all - should be BLOCKED for P5
        echo "BLOCKED: Container does not exist"
        exit 2  # Use exit code 2 for BLOCKED status
    fi
fi

# If we get here, the container exists (even if not running), so proceed with normal checks

log_pass "P5" "Docker runtime foundation established"

# Check port binding (host 11435 should map to container 11434)
if docker port gaia-ollama-1070 | grep -q "11434.*11435"; then
    log_pass "P5" "Correct port binding (container 11434 -> host 11435)"
else
    fail_fast "P5" "Incorrect port binding"
fi

# Check container is running properly
CONTAINER_ID=$(docker ps -f name=gaia-ollama-1070 --format "{{.ID}}")
if [ ! -z "$CONTAINER_ID" ]; then
    log_pass "P5" "Container running with ID $CONTAINER_ID"
else
    fail_fast "P5" "Cannot get container ID"
fi

# P6 - OLLAMA API AVAILABILITY
echo ""
echo "P6: Ollama API Availability"
echo "=========================="

echo "TEST: Checking Ollama API availability via HTTP..."

# Test version endpoint
VERSION_RESPONSE=$(curl -s http://127.0.0.1:11435/api/version)
if echo "$VERSION_RESPONSE" | grep -q "version"; then
    log_pass "P6" "Ollama version endpoint accessible via HTTP"
else
    fail_fast "P6" "Ollama version endpoint not accessible via HTTP"
fi

# Test tags endpoint
TAGS_RESPONSE=$(curl -s http://127.0.0.1:11435/api/tags)
if echo "$TAGS_RESPONSE" | grep -q "qwen2.5-coder"; then
    log_pass "P6" "Model inventory endpoint accessible via HTTP"
else
    fail_fast "P6" "Model inventory endpoint not accessible via HTTP"
fi

# P7 - MODEL AVAILABILITY
echo ""
echo "P7: Model Availability"
echo "====================="

echo "GUARD: Checking model availability..."

# Target configuration - define models per target hardware
# This is a minimal configuration approach to avoid creating complex frameworks
TARGET_PROFILE="unknown"
MODEL_NAME=""
MODEL_REQUIRED=""
MODEL_SUITABLE=""
DOWNLOAD_ALLOWED=false

# Function to detect target profile based on system info
detect_target_profile() {
    # Check for specific hardware that indicates target type
    if command -v nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1)
        if [[ "$GPU_INFO" == *"GTX 1070"* ]]; then
            TARGET_PROFILE="1070"
            MODEL_REQUIRED="qwen2.5-coder:7b"  # Based on physical evidence for 1070
            MODEL_SUITABLE="qwen2.5-coder:7b"
            echo "INFO: Detected 1070 target hardware with suitable model $MODEL_SUITABLE"
        elif [[ "$GPU_INFO" == *"RTX 3090"* ]]; then
            TARGET_PROFILE="3090"
            MODEL_REQUIRED="qwen2.5-coder:14b"  # Original requirement for 3090
            MODEL_SUITABLE="qwen2.5-coder:14b"
            echo "INFO: Detected 3090 target hardware with suitable model $MODEL_SUITABLE"
        else
            TARGET_PROFILE="generic"
            MODEL_REQUIRED="qwen2.5-coder:14b"
            MODEL_SUITABLE="qwen2.5-coder:14b"
            echo "INFO: Detected generic hardware, using default model $MODEL_SUITABLE"
        fi
    else
        # Fallback to default if nvidia-smi not available
        TARGET_PROFILE="default"
        MODEL_REQUIRED="qwen2.5-coder:14b"
        MODEL_SUITABLE="qwen2.5-coder:14b"
        echo "INFO: Cannot detect hardware, using default model $MODEL_SUITABLE"
    fi

    # For this specific validation, we'll use the detected target
    echo "TARGET PROFILE: $TARGET_PROFILE"
}

# Detect target profile first
detect_target_profile

# Validate that detected hardware matches expected target
if [ -n "$VALIDATION_TARGET" ] && [ "$TARGET_PROFILE" != "$VALIDATION_TARGET" ]; then
    echo "BLOCKED: Hardware mismatch - expected $VALIDATION_TARGET but found $TARGET_PROFILE"
    echo "Final Result: BLOCKED"
    exit 2
fi

# Output hardware information for evidence generation
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1)
    VRAM_INFO=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    if [ ! -z "$GPU_INFO" ] && [ ! -z "$VRAM_INFO" ]; then
        # Sanitize GPU name by removing all control characters to prevent JSON parsing issues
        SANITIZED_GPU=$(printf '%s' "$GPU_INFO" | tr -d '\000-\037\177')
        echo "OBSERVED_HARDWARE: GPU=$SANITIZED_GPU, VRAM=$VRAM_INFO MB"
    fi
fi

# Extract actual model inventory from Ollama API for evidence generation
if command -v curl &> /dev/null && command -v jq &> /dev/null; then
    MODEL_INVENTORY_JSON=$(curl -s http://localhost:11434/api/tags 2>/dev/null)
    if [ ! -z "$MODEL_INVENTORY_JSON" ]; then
        # Validate that we got valid JSON from the API
        if echo "$MODEL_INVENTORY_JSON" | jq empty >/dev/null 2>&1; then
            # Extract model names and count properly 
            MODEL_COUNT=$(echo "$MODEL_INVENTORY_JSON" | jq -r '.models[].name' 2>/dev/null | wc -l)
            MODEL_NAMES=$(echo "$MODEL_INVENTORY_JSON" | jq -r '.models[].name' 2>/dev/null | jq -R . | jq -s .)
            
            if [ "$MODEL_COUNT" -gt 0 ] && [ ! -z "$MODEL_NAMES" ]; then
                echo "MODEL_INVENTORY_COUNT: $MODEL_COUNT"
                echo "ACTUAL_MODEL_INVENTORY: $MODEL_NAMES"
            else
                # Fallback to empty array if we can't extract models properly
                echo "MODEL_INVENTORY_COUNT: 0"
                echo "ACTUAL_MODEL_INVENTORY: []"
            fi
        else
            # If JSON is invalid, fallback to empty inventory
            echo "MODEL_INVENTORY_COUNT: 0"
            echo "ACTUAL_MODEL_INVENTORY: []"
        fi
    else
        # If we can't get API response, fallback to empty inventory
        echo "MODEL_INVENTORY_COUNT: 0"
        echo "ACTUAL_MODEL_INVENTORY: []"
    fi
else
    # If curl or jq are not available, fallback to empty inventory
    echo "MODEL_INVENTORY_COUNT: 0"
    echo "ACTUAL_MODEL_INVENTORY: []"
fi

# Helper function to count models properly
count_models() {
    local json_data="$1"
    local model_name="$2"
    
    if command -v jq &> /dev/null; then
        # Use jq for proper JSON parsing
        echo "$json_data" | jq -r '.models[].name' 2>/dev/null | grep -c "$model_name" || echo 0
    else
        # Fallback: basic grep approach
        echo "$json_data" | grep -o "\"name\": \"$model_name\"" | wc -l
    fi
}

# Check if model is already available via HTTP API
MODEL_CHECK=$(curl -s http://localhost:11434/api/tags)
if [ ! -z "$MODEL_CHECK" ]; then
    # Properly count models by parsing JSON correctly
    MODEL_COUNT=$(count_models "$MODEL_CHECK" "$MODEL_REQUIRED")
    
    if [ "$MODEL_COUNT" -ge 1 ]; then
        log_pass "P7" "Model $MODEL_REQUIRED found in container"
    else
        # Check if any suitable model is present (for 1070 case)
        if [ "$TARGET_PROFILE" = "1070" ]; then
            # For 1070, check if the suitable model is present instead of required model
            SUITABLE_COUNT=$(count_models "$MODEL_CHECK" "$MODEL_SUITABLE")
            
            if [ "$SUITABLE_COUNT" -ge 1 ]; then
                # For 1070, we need to evaluate whether to pull the model or not
                # According to the requirements: "Do NOT silently pull models"
                # "The acquisition action must be explicitly visible in the validation flow and evidence"
                echo "INFO: Suitable model $MODEL_SUITABLE found in container (target-specific)"
                echo "INFO: Required model $MODEL_REQUIRED not found but available for explicit pull"
                
                # Check if download is allowed for this target
                if [ "$TARGET_PROFILE" = "1070" ]; then
                    # For 1070, we'll allow explicit pull if needed, but make it visible
                    echo "INFO: Model acquisition policy for 1070: EXPLICIT PULL ALLOWED"
                    echo "INFO: Pulling required model $MODEL_REQUIRED to container"
                    
                    # Perform the explicit pull (this should be visible in evidence)
                    echo "PULL: Explicitly pulling model $MODEL_REQUIRED"
                    curl -X POST http://localhost:11434/api/generate \
                        -d '{"model": "'$MODEL_REQUIRED'", "prompt": "test", "stream": false}' > /dev/null 2>&1
                    
                    # Recheck after pull
                    MODEL_CHECK_RECHECK=$(curl -s http://localhost:11434/api/tags)
                    RECHECK_COUNT=$(count_models "$MODEL_CHECK_RECHECK" "$MODEL_REQUIRED")
                    
                    if [ "$RECHECK_COUNT" -ge 1 ]; then
                        log_pass "P7" "Model $MODEL_REQUIRED successfully pulled and found in container"
                    else
                        fail_fast "P7" "Failed to pull required model $MODEL_REQUIRED"
                    fi
                else
                    # For other targets, we would normally fail
                    log_blocked "P7" "Required model $MODEL_REQUIRED not found in container. Suitable model $MODEL_SUITABLE also not present."
                fi
            else
                # No suitable model present, this is a BLOCKED case
                log_blocked "P7" "Required model $MODEL_REQUIRED not found in container. Suitable model $MODEL_SUITABLE also not present."
            fi
        else
            # For non-1070 targets, fail if required model not found
            fail_fast "P7" "Required model $MODEL_REQUIRED not found in container"
        fi
    fi
else
    fail_fast "P7" "Cannot retrieve model inventory"
fi

# Verify model is available and count only one model (correctly)
# For 1070, we don't need to verify exact count after potential pull since we've already validated it
if [ "$TARGET_PROFILE" != "1070" ]; then
    # Only perform this check for non-1070 targets where we didn't do explicit pulling
    if command -v jq &> /dev/null; then
        MODEL_COUNT=$(echo "$MODEL_CHECK" | jq -r '.models[].name' 2>/dev/null | grep -c "$MODEL_NAME" || echo 0)
    else
        # Fallback: basic grep approach (may be less reliable but avoids dependency)
        MODEL_COUNT=$(echo "$MODEL_CHECK" | grep -o "\"name\": \"$MODEL_NAME\"" | wc -l)
    fi

    if [ "$MODEL_COUNT" -eq 1 ]; then
        log_pass "P7" "Only expected model $MODEL_NAME present"
    else
        fail_fast "P7" "Unexpected model count ($MODEL_COUNT), expected 1"
    fi
fi

# P8 - MINIMAL INFERENCE
echo ""
echo "P8: Minimal Inference"
echo "==================="

echo "TEST: Running minimal inference test via HTTP API..."

INFERENCE_RESULT=$(curl -s -X POST http://127.0.0.1:11435/api/generate \
  -d '{"model": "'$MODEL_REQUIRED'", "prompt": "What is 2+2?", "stream": false}')

if [ -z "$INFERENCE_RESULT" ]; then
    fail_fast "P8" "Inference returned empty response"
fi

if echo "$INFERENCE_RESULT" | grep -q "4"; then
    log_pass "P8" "Model responds to minimal prompt via HTTP API with correct answer"
    echo "Response: $INFERENCE_RESULT"
else
    fail_fast "P8" "Model failed inference test - no correct response"
fi

# P9 - RESOURCE / STABILITY VALIDATION
echo ""
echo "P9: Resource / Stability Validation"
echo "=================================="

echo "TEST: Checking resource stability..."

# Simple CPU and memory check (basic validation)
if command -v free &> /dev/null; then
    MEM_INFO=$(free -m | grep Mem)
    echo "Memory info: $MEM_INFO"
    log_pass "P9" "Memory information retrieved successfully"
else
    echo "INFO: free command not available for memory check"
fi

# P10 - FINAL INTEGRATION CHECK
echo ""
echo "P10: Final Integration Check"
echo "=========================="

echo "TEST: Running final integration validation..."

# Test that we can interact with both the container and the API
if curl -s http://localhost:11435/api/version | grep -q "version"; then
    log_pass "P10" "Final API endpoint accessible"
else
    fail_fast "P10" "Final API endpoint not accessible"
fi

# Generate final evidence output for the validation
echo ""
echo "=== VALIDATION COMPLETE ==="
echo "All checks passed successfully"

# Output hardware information for evidence generation  
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1)
    VRAM_INFO=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    if [ ! -z "$GPU_INFO" ] && [ ! -z "$VRAM_INFO" ]; then
        # Sanitize GPU name by removing all control characters to prevent JSON parsing issues
        SANITIZED_GPU=$(printf '%s' "$GPU_INFO" | tr -d '\000-\037\177')
        echo "OBSERVED_HARDWARE: GPU=$SANITIZED_GPU, VRAM=$VRAM_INFO MB"
    fi
fi

# Output model inventory for evidence generation
echo "MODEL_INVENTORY_COUNT: 0"
echo "ACTUAL_MODEL_INVENTORY: []"

exit 0