#!/usr/bin/env python3
"""Quick test script for dashboard server."""

import time
import subprocess
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

print("🚀 Starting GAIA Dashboard Server...")
proc = subprocess.Popen(
    ['python3', 'scripts/dashboard_server.py', '--port', '8095'],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(3)

# Test the APIs
try:
    print("\n📊 Testing API endpoints...")
    
    # Test stats
    response = requests.get('http://127.0.0.1:8095/api/stats')
    stats = response.json()
    print(f"✓ Stats API: {stats['total_tasks']} tasks, {stats['completed_tasks']} completed")
    
    # Test tasks
    response = requests.get('http://127.0.0.1:8095/api/tasks')
    tasks = response.json()
    print(f"✓ Tasks API: {len(tasks)} tasks loaded")
    
    # Test agents
    response = requests.get('http://127.0.0.1:8095/api/agents')
    agents = response.json()
    print(f"✓ Agents API: {len(agents)} agents configured")
    
    print(f"\n✅ All APIs working!")
    print(f"📈 Access dashboard at: http://127.0.0.1:8095/dashboard")
    print(f"\n⏸️  Server running... (PID: {proc.pid})")
    print("   Press CTRL+C to stop")
    
    # Keep running
    proc.wait()
    
except KeyboardInterrupt:
    print("\n\n🛑 Stopping server...")
    proc.terminate()
    proc.wait()
    print("✓ Server stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
    proc.terminate()
    proc.wait()
