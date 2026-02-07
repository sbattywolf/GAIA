#!/usr/bin/env python3
"""
GAIA Dashboard Launcher

Simple one-command launcher for the GAIA dashboard.
Automatically finds an available port and opens the browser.
Uses less common ports (9080-9099 range) to avoid conflicts.
"""

import sys
import socket
import webbrowser
import time
import subprocess
import random
from pathlib import Path

def find_available_port(start_port=None, max_attempts=20):
    """
    Find an available port starting from a random less-common port.
    
    Uses port range 9080-9099 by default to avoid common port conflicts.
    """
    if start_port is None:
        # Start from random port in less common range to avoid conflicts
        start_port = random.randint(9080, 9099)
    
    # Try ports in sequence from start_port
    for offset in range(max_attempts):
        port = start_port + offset
        # Keep in reasonable range
        if port > 65535:
            port = 9080 + (port - 65536) % 20
            
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result != 0:  # Port is available
                return port
        except:
            pass
    return None

def main():
    """Launch the dashboard."""
    print("🚀 GAIA Dashboard Launcher")
    print("=" * 50)
    
    # Find repository root
    try:
        root = Path(__file__).resolve().parents[1]
    except:
        root = Path.cwd()
    
    print(f"Repository: {root}")
    
    # Check if dashboard server exists
    server_script = root / 'scripts' / 'dashboard_server.py'
    if not server_script.exists():
        print(f"❌ Error: Dashboard server not found at {server_script}")
        print("   Make sure you're in the GAIA repository directory.")
        return 1
    
    # Find available port
    print("\n🔍 Finding available port...")
    port = find_available_port()
    if port is None:
        print("❌ Error: Could not find an available port.")
        print("   Try closing some applications and try again.")
        return 1
    
    print(f"✓ Using port {port}")
    
    # Start the server
    dashboard_url = f"http://127.0.0.1:{port}/dashboard"
    print(f"\n🌐 Starting dashboard server...")
    print(f"   URL: {dashboard_url}")
    print(f"\n⏸️  Server is running. Press Ctrl+C to stop.\n")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)  # Give server time to start
        try:
            print(f"🌍 Opening browser...")
            webbrowser.open(dashboard_url)
        except:
            print(f"   Could not auto-open browser.")
            print(f"   Please open manually: {dashboard_url}")
    
    # Start browser opening in background
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start the server (this blocks)
    try:
        subprocess.run([
            sys.executable,
            str(server_script),
            '--port', str(port)
        ])
    except KeyboardInterrupt:
        print("\n\n✓ Dashboard stopped.")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
