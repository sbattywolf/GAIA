#!/usr/bin/env bash

# Test script for SSH transport functionality
# This simulates the transport behavior without requiring actual SSH connection

set -u
set -o pipefail

echo "=== SSH Transport Test ==="

# Mock function to simulate SSH command execution
mock_ssh_execute() {
    local target=$1
    local command=$2
    
    echo "Mock: Executing command '$command' on target '$target'"
    
    # Simulate different outcomes based on command
    case "$command" in
        "whoami")
            echo "{\"run_id\": \"test-$(date +%s)\", \"target_id\": \"$target\", \"transport\": \"ssh\", \"target_host\": \"10.16.20.13\", \"target_user\": \"sbatta\", \"command\": \"$command\", \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"finished_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"transport_status\": \"SUCCESS\", \"exit_code\": 0, \"stdout_reference\": \"mock_stdout\", \"stderr_reference\": \"mock_stderr\"}"
            return 0
            ;;
        "hostname")
            echo "{\"run_id\": \"test-$(date +%s)\", \"target_id\": \"$target\", \"transport\": \"ssh\", \"target_host\": \"10.16.20.13\", \"target_user\": \"sbatta\", \"command\": \"$command\", \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"finished_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"transport_status\": \"SUCCESS\", \"exit_code\": 0, \"stdout_reference\": \"mock_stdout\", \"stderr_reference\": \"mock_stderr\"}"
            return 0
            ;;
        "fail_command")
            echo "{\"run_id\": \"test-$(date +%s)\", \"target_id\": \"$target\", \"transport\": \"ssh\", \"target_host\": \"10.16.20.13\", \"target_user\": \"sbatta\", \"command\": \"$command\", \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"finished_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"transport_status\": \"FAILURE\", \"exit_code\": 1, \"stdout_reference\": \"mock_stdout\", \"stderr_reference\": \"mock_stderr\"}"
            return 1
            ;;
        *)
            echo "{\"run_id\": \"test-$(date +%s)\", \"target_id\": \"$target\", \"transport\": \"ssh\", \"target_host\": \"10.16.20.13\", \"target_user\": \"sbatta\", \"command\": \"$command\", \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"finished_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"transport_status\": \"SUCCESS\", \"exit_code\": 0, \"stdout_reference\": \"mock_stdout\", \"stderr_reference\": \"mock_stderr\"}"
            return 0
            ;;
    esac
}

# Test different scenarios
echo "1. Testing basic command execution..."
result=$(mock_ssh_execute "gaia-1070" "whoami")
echo "Result: $result"

echo "2. Testing hostname command..."
result=$(mock_ssh_execute "gaia-1070" "hostname") 
echo "Result: $result"

echo "3. Testing failure scenario..."
result=$(mock_ssh_execute "gaia-1070" "fail_command")
echo "Result: $result"

echo "=== Transport Test Complete ==="