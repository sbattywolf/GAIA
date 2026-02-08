#!/usr/bin/env python3
"""Launch GAIA Enhanced Dashboard with automatic browser opening.

This script starts the GAIA dashboard server on an available port and
automatically opens the enhanced dashboard in your default browser.

Usage:
    python scripts/launch_enhanced_dashboard.py
    python scripts/launch_enhanced_dashboard.py --port 8080
    python scripts/launch_enhanced_dashboard.py --no-browser
"""

import argparse
import os
import sys
import time
import webbrowser
from pathlib import Path
import socket
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def find_available_port(start_port=9080, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Launch GAIA Enhanced Dashboard with automatic browser opening',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch on default port (9080)
  python scripts/launch_enhanced_dashboard.py

  # Launch on specific port
  python scripts/launch_enhanced_dashboard.py --port 8080

  # Launch without opening browser
  python scripts/launch_enhanced_dashboard.py --no-browser

Features:
  • Automatically finds available port
  • Opens enhanced dashboard in default browser
  • Shows both standard and enhanced URLs
        """
    )
    
    parser.add_argument('--port', type=int, default=9080,
                        help='Preferred port (default: 9080)')
    parser.add_argument('--host', default='127.0.0.1',
                        help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open browser automatically')
    parser.add_argument('--standard', action='store_true',
                        help='Open standard dashboard instead of enhanced')
    
    args = parser.parse_args()
    
    print("🚀 GAIA Enhanced Dashboard Launcher")
    print("=" * 60)
    
    # Find available port
    port = find_available_port(args.port)
    if port is None:
        print(f"❌ Could not find available port starting from {args.port}")
        return 1
    
    if port != args.port:
        print(f"ℹ️  Port {args.port} in use, using {port} instead")
    
    # Build URLs
    base_url = f"http://{args.host}:{port}"
    enhanced_url = f"{base_url}/enhanced"
    standard_url = f"{base_url}/dashboard"
    dashboard_url = enhanced_url if not args.standard else standard_url
    
    print(f"\n📍 Server starting on {base_url}")
    print(f"   Standard Dashboard: {standard_url}")
    print(f"   Enhanced Dashboard: {enhanced_url}")
    print(f"   API Endpoints: {base_url}/api/")
    
    # Start server in subprocess
    server_script = ROOT / 'scripts' / 'dashboard_server.py'
    
    if not server_script.exists():
        print(f"❌ Server script not found: {server_script}")
        return 1
    
    print(f"\n🔧 Starting server...")
    
    try:
        # Start server
        cmd = [sys.executable, str(server_script), '--host', args.host, '--port', str(port)]
        proc = subprocess.Popen(cmd, cwd=ROOT)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(2)
        
        # Check if server is running
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((args.host, port))
            sock.close()
            
            if result != 0:
                print("⚠️  Server may not have started properly")
        except Exception as e:
            print(f"⚠️  Could not verify server: {e}")
        
        # Open browser
        if not args.no_browser:
            print(f"\n🌐 Opening {dashboard_url} in browser...")
            try:
                webbrowser.open(dashboard_url)
                print("✅ Browser opened successfully")
            except Exception as e:
                print(f"⚠️  Could not open browser: {e}")
                print(f"   Please open manually: {dashboard_url}")
        else:
            print(f"\n📋 Dashboard ready at: {dashboard_url}")
        
        print(f"\n✨ Dashboard is running!")
        print(f"   Press CTRL+C to stop the server")
        
        # Wait for server process
        proc.wait()
        
    except KeyboardInterrupt:
        print("\n\n✓ Shutting down server...")
        proc.terminate()
        proc.wait()
        print("✓ Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
