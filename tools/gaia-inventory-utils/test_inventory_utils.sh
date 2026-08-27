#!/usr/bin/env bash

# Test script for inventory utilities extraction validation

echo "=== Testing Original Implementation ==="
cd /home/sbatta/github_repos/GAIA

# Source the original implementation
source gaia_engineering_loop/lib/inventory_utils.sh

echo ""
echo "--- Test 1: Valid target configuration ---"
result1=$(load_target_config "gaia-1070")
exit_code1=$?
echo "Exit code: $exit_code1"
echo "Output:"
echo "$result1"

echo ""
echo "--- Test 2: Missing target configuration ---"
result2=$(load_target_config "nonexistent")
exit_code2=$?
echo "Exit code: $exit_code2"
echo "Output:"
echo "$result2"

echo ""
echo "--- Test 3: Valid transport configuration ---"
result3=$(load_transport_config "gaia-1070" "ssh")
exit_code3=$?
echo "Exit code: $exit_code3"
echo "Output:"
echo "$result3"

echo ""
echo "--- Test 4: Missing transport configuration ---"
result4=$(load_transport_config "gaia-1070" "nonexistent")
exit_code4=$?
echo "Exit code: $exit_code4"
echo "Output:"
echo "$result4"

echo ""
echo "--- Test 5: Target readiness ---"
result5=$(is_target_ready "gaia-1070")
exit_code5=$?
echo "Exit code: $exit_code5"
echo "Output:"
echo "$result5"

echo ""
echo "--- Test 6: Get target readiness ---"
result6=$(get_target_readiness "gaia-1070")
exit_code6=$?
echo "Exit code: $exit_code6"
echo "Output:"
echo "$result6"

echo ""
echo "=== Testing Extracted Implementation ==="

# Source the extracted implementation
source tools/gaia-inventory-utils/inventory_utils.sh

echo ""
echo "--- Test 1: Valid target configuration ---"
result1_extract=$(load_target_config "gaia-1070")
exit_code1_extract=$?
echo "Exit code: $exit_code1_extract"
echo "Output:"
echo "$result1_extract"

echo ""
echo "--- Test 2: Missing target configuration ---"
result2_extract=$(load_target_config "nonexistent")
exit_code2_extract=$?
echo "Exit code: $exit_code2_extract"
echo "Output:"
echo "$result2_extract"

echo ""
echo "--- Test 3: Valid transport configuration ---"
result3_extract=$(load_transport_config "gaia-1070" "ssh")
exit_code3_extract=$?
echo "Exit code: $exit_code3_extract"
echo "Output:"
echo "$result3_extract"

echo ""
echo "--- Test 4: Missing transport configuration ---"
result4_extract=$(load_transport_config "gaia-1070" "nonexistent")
exit_code4_extract=$?
echo "Exit code: $exit_code4_extract"
echo "Output:"
echo "$result4_extract"

echo ""
echo "--- Test 5: Target readiness ---"
result5_extract=$(is_target_ready "gaia-1070")
exit_code5_extract=$?
echo "Exit code: $exit_code5_extract"
echo "Output:"
echo "$result5_extract"

echo ""
echo "--- Test 6: Get target readiness ---"
result6_extract=$(get_target_readiness "gaia-1070")
exit_code6_extract=$?
echo "Exit code: $exit_code6_extract"
echo "Output:"
echo "$result6_extract"

echo ""
echo "=== Comparison Results ==="
echo "Test 1 (valid target config): $(if [[ "$result1" == "$result1_extract" && $exit_code1 -eq $exit_code1_extract ]]; then echo "PASS"; else echo "FAIL"; fi)"
echo "Test 2 (missing target config): $(if [[ "$result2" == "$result2_extract" && $exit_code2 -eq $exit_code2_extract ]]; then echo "PASS"; else echo "FAIL"; fi)"
echo "Test 3 (valid transport config): $(if [[ "$result3" == "$result3_extract" && $exit_code3 -eq $exit_code3_extract ]]; then echo "PASS"; else echo "FAIL"; fi)"
echo "Test 4 (missing transport config): $(if [[ "$result4" == "$result4_extract" && $exit_code4 -eq $exit_code4_extract ]]; then echo "PASS"; else echo "FAIL"; fi)"
echo "Test 5 (target readiness): $(if [[ "$result5" == "$result5_extract" && $exit_code5 -eq $exit_code5_extract ]]; then echo "PASS"; else echo "FAIL"; fi)"
echo "Test 6 (get target readiness): $(if [[ "$result6" == "$result6_extract" && $exit_code6 -eq $exit_code6_extract ]]; then echo "PASS"; else echo "FAIL"; fi)"