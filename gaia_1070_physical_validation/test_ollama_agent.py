#!/usr/bin/env python3
"""
Simple test script to verify Ollama integration works properly.
This demonstrates that agents can use Ollama models.
"""

import requests
import json

def test_ollama_connection():
    """Test connection to Ollama API"""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            print("✓ Successfully connected to Ollama API")
            models = response.json()['models']
            print(f"Available models: {len(models)}")
            for model in models[:3]:  # Show first 3 models
                print(f"  - {model['name']}")
            return True
        else:
            print(f"✗ Failed to connect to Ollama API: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to Ollama API: {e}")
        return False

def test_ollama_generation():
    """Test generating text with Ollama"""
    try:
        payload = {
            "model": "qwen2.5-coder:7b",
            "prompt": "Hello, can you tell me about your capabilities?",
            "stream": False
        }
        
        response = requests.post('http://localhost:11434/api/generate', 
                              json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Successfully generated text with Ollama")
            print(f"Response: {result['response'][:100]}...")
            return True
        else:
            print(f"✗ Failed to generate text with Ollama: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error generating text with Ollama: {e}")
        return False

def main():
    print("Testing Ollama Integration")
    print("=" * 30)
    
    success = True
    success &= test_ollama_connection()
    success &= test_ollama_generation()
    
    print("\n" + "=" * 30)
    if success:
        print("✓ All tests passed - Ollama is working correctly!")
        print("This demonstrates that agents can use Ollama models.")
    else:
        print("✗ Some tests failed")
        
    return success

if __name__ == "__main__":
    main()