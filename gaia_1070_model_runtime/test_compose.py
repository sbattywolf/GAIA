#!/usr/bin/env python3
"""
Test script to validate Docker Compose configuration syntax
"""

import yaml
import sys
import os

def test_compose_syntax():
    """Test that the compose file has valid YAML syntax"""
    try:
        with open('docker-compose.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Check that we have a version and services
        if not config.get('version'):
            print("FAIL: Missing version in compose file")
            return False
            
        if not config.get('services'):
            print("FAIL: Missing services in compose file")
            return False
            
        # Check for required service
        if 'gaia-ollama' not in config['services']:
            print("FAIL: Missing gaia-ollama service")
            return False
            
        service = config['services']['gaia-ollama']
        
        # Check required elements
        required_elements = ['image', 'container_name', 'ports', 'volumes']
        for element in required_elements:
            if element not in service:
                print(f"FAIL: Missing {element} in gaia-ollama service")
                return False
                
        print("PASS: Docker Compose configuration syntax is valid")
        return True
        
    except yaml.YAMLError as e:
        print(f"FAIL: YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"FAIL: Error reading compose file: {e}")
        return False

if __name__ == "__main__":
    success = test_compose_syntax()
    sys.exit(0 if success else 1)