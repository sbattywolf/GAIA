#!/usr/bin/env python3
"""Enhanced monitor server with dashboard views for GAIA project."""

from __future__ import annotations
import os
import json
import argparse
import subprocess
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = ROOT / 'scripts'
DOC_ROOT = ROOT / 'doc'
TMP = ROOT / '.tmp'


def load_json_file(filepath: Path, default=None):
    """Safely load a JSON file."""
    if default is None:
        default = []
    try:
        if not filepath.exists():
            return default
        return json.loads(filepath.read_text(encoding='utf-8'))
    except Exception:
        return default


def load_ndjson_file(filepath: Path):
    """Load NDJSON file and return list of objects."""
    try:
        if not filepath.exists():
            return []
        content = filepath.read_text(encoding='utf-8')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        results = []
        for line in lines:
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip malformed lines
                continue
        return results
    except Exception:
        return []


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for GAIA project dashboard."""

    def _set_json_headers(self, code=200):
        """Set JSON response headers."""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _set_html_headers(self, code=200):
        """Set HTML response headers."""
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Admin-Token')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        path = self.path.split('?')[0]  # Remove query params

        # Dashboard home
        if path == '/' or path == '/dashboard':
            return self._serve_dashboard()

        # Enhanced dashboard
        if path == '/enhanced' or path == '/dashboard/enhanced':
            return self._serve_enhanced_dashboard()

        # API: Tasks data
        if path == '/api/tasks':
            return self._serve_tasks()

        # API: Agents data
        if path == '/api/agents':
            return self._serve_agents()

        # API: Project stats
        if path == '/api/stats':
            return self._serve_stats()

        # API: Pending commands
        if path == '/api/pending':
            return self._serve_pending()

        # API: Roadmap data
        if path == '/api/roadmap':
            return self._serve_roadmap()

        # API: Sprint data
        if path == '/api/sprints':
            return self._serve_sprints()

        # Serve static files from doc/ (for NDJSON access)
        if path.startswith('/doc/'):
            return self._serve_file(DOC_ROOT / path[5:])

        # Serve static files
        if path.startswith('/scripts/') or path.endswith(('.html', '.js', '.css')):
            filepath = ROOT / path.lstrip('/')
            return self._serve_file(filepath)

        # 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')

    def do_POST(self):
        """Handle POST requests."""
        path = self.path.split('?')[0]

        # API: Trigger archive refresh
        if path == '/api/refresh':
            return self._trigger_refresh()

        # 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')

    def _serve_dashboard(self):
        """Serve the main dashboard HTML."""
        dashboard_path = STATIC_ROOT / 'project_dashboard.html'
        if dashboard_path.exists():
            try:
                content = dashboard_path.read_text(encoding='utf-8')
                self._set_html_headers(200)
                self.wfile.write(content.encode('utf-8'))
                return
            except Exception as e:
                print(f"Error serving dashboard: {e}")
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Dashboard not found')

    def _serve_enhanced_dashboard(self):
        """Serve the enhanced dashboard HTML."""
        dashboard_path = STATIC_ROOT / 'project_dashboard_enhanced.html'
        if dashboard_path.exists():
            try:
                content = dashboard_path.read_text(encoding='utf-8')
                self._set_html_headers(200)
                self.wfile.write(content.encode('utf-8'))
                return
            except Exception as e:
                print(f"Error serving enhanced dashboard: {e}")
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Enhanced dashboard not found')

    def _serve_tasks(self):
        """Serve tasks data from todo-archive.ndjson."""
        tasks = load_ndjson_file(DOC_ROOT / 'todo-archive.ndjson')
        self._set_json_headers(200)
        self.wfile.write(json.dumps(tasks, default=str).encode('utf-8'))

    def _serve_agents(self):
        """Serve agents configuration."""
        agents = load_json_file(ROOT / 'agents.json', [])
        self._set_json_headers(200)
        self.wfile.write(json.dumps(agents, default=str).encode('utf-8'))

    def _serve_stats(self):
        """Calculate and serve project statistics."""
        tasks = load_ndjson_file(DOC_ROOT / 'todo-archive.ndjson')
        agents = load_json_file(ROOT / 'agents.json', [])
        
        stats = {
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if t.get('status') == 'completed']),
            'pending_tasks': len([t for t in tasks if t.get('status') == 'pending']),
            'inprogress_tasks': len([t for t in tasks if t.get('status') == 'in-progress']),
            'critical_tasks': len([t for t in tasks if t.get('priority') == 'critical']),
            'high_priority_tasks': len([t for t in tasks if t.get('priority') == 'high']),
            'total_agents': len(agents),
            'total_est_hours': sum(t.get('est_hours', 0) for t in tasks),
            'completed_hours': sum(t.get('est_hours', 0) for t in tasks if t.get('status') == 'completed'),
        }
        
        self._set_json_headers(200)
        self.wfile.write(json.dumps(stats, default=str).encode('utf-8'))

    def _serve_pending(self):
        """Serve pending commands."""
        pending = load_json_file(TMP / 'pending_commands.json', [])
        self._set_json_headers(200)
        self.wfile.write(json.dumps({'pending': pending}, default=str).encode('utf-8'))

    def _trigger_refresh(self):
        """Trigger update_todo_archive.py script."""
        try:
            # Path to the update script
            script_path = ROOT / 'scripts' / 'update_todo_archive.py'
            
            if not script_path.exists():
                self._set_json_headers(404)
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'update_todo_archive.py not found'
                }).encode('utf-8'))
                return
            
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path), '--verbose'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(ROOT)
            )
            
            if result.returncode == 0:
                # Success
                self._set_json_headers(200)
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': 'Archive updated successfully',
                    'output': result.stdout,
                    'stats': self._extract_stats(result.stdout)
                }).encode('utf-8'))
            else:
                # Error
                self._set_json_headers(500)
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'Script execution failed',
                    'output': result.stdout,
                    'stderr': result.stderr
                }).encode('utf-8'))
                
        except subprocess.TimeoutExpired:
            self._set_json_headers(500)
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'Script execution timed out (30s)'
            }).encode('utf-8'))
        except Exception as e:
            self._set_json_headers(500)
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8'))

    def _extract_stats(self, output: str) -> dict:
        """Extract statistics from script output."""
        stats = {}
        for line in output.split('\n'):
            if 'Sprint items:' in line:
                stats['sprint_items'] = int(line.split(':')[1].strip())
            elif 'Backlog items:' in line:
                stats['backlog_items'] = int(line.split(':')[1].strip())
            elif 'Total entries:' in line:
                stats['total_entries'] = int(line.split(':')[1].strip())
        return stats

    def _serve_roadmap(self):
        """Serve roadmap data grouped by sprints/milestones."""
        tasks = load_ndjson_file(DOC_ROOT / 'todo-archive.ndjson')
        
        # Group tasks by sprint/milestone
        roadmap = {}
        for task in tasks:
            sprint = task.get('sprint') or task.get('milestone') or 'Backlog'
            if sprint not in roadmap:
                roadmap[sprint] = []
            roadmap[sprint].append(task)
        
        self._set_json_headers(200)
        self.wfile.write(json.dumps(roadmap, default=str).encode('utf-8'))

    def _serve_sprints(self):
        """Serve sprint data."""
        tasks = load_ndjson_file(DOC_ROOT / 'todo-archive.ndjson')
        
        # Extract unique sprints
        sprints = set()
        for task in tasks:
            sprint = task.get('sprint') or task.get('milestone')
            if sprint:
                sprints.add(sprint)
        
        sprint_data = []
        for sprint in sorted(sprints):
            sprint_tasks = [t for t in tasks if (t.get('sprint') or t.get('milestone')) == sprint]
            sprint_data.append({
                'name': sprint,
                'total_tasks': len(sprint_tasks),
                'completed': len([t for t in sprint_tasks if t.get('status') == 'completed']),
                'in_progress': len([t for t in sprint_tasks if t.get('status') == 'in-progress']),
                'pending': len([t for t in sprint_tasks if t.get('status') == 'pending']),
            })
        
        self._set_json_headers(200)
        self.wfile.write(json.dumps(sprint_data, default=str).encode('utf-8'))

    def _serve_file(self, filepath: Path):
        """Serve a static file."""
        if not filepath.exists() or not filepath.is_file():
            self.send_response(404)
            self.end_headers()
            return

        try:
            # Determine content type
            content_type = 'application/octet-stream'
            suffix = filepath.suffix.lower()
            content_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.json': 'application/json',
                '.ndjson': 'application/x-ndjson',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
            }
            content_type = content_types.get(suffix, content_type)

            # Read and serve file
            content = filepath.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"Error serving file {filepath}: {e}")
            self.send_response(500)
            self.end_headers()


def serve(host: str = '127.0.0.1', port: int = 9080):
    """Start the dashboard server."""
    addr = (host, port)
    httpd = HTTPServer(addr, DashboardHandler)
    print(f'🚀 GAIA Project Dashboard serving on http://{host}:{port}')
    print(f'   Standard Dashboard: http://{host}:{port}/dashboard')
    print(f'   Enhanced Dashboard: http://{host}:{port}/enhanced')
    print(f'   API Endpoints: http://{host}:{port}/api/')
    print(f'   Press CTRL+C to stop')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Server stopped')
    finally:
        httpd.server_close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='GAIA Project Dashboard Server')
    parser.add_argument('--host', default=os.environ.get('GAIA_DASHBOARD_HOST', '127.0.0.1'),
                        help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=int(os.environ.get('GAIA_DASHBOARD_PORT', '9080')),
                        help='Port to bind to (default: 9080 - less common to avoid conflicts)')
    args = parser.parse_args()
    
    serve(args.host, args.port)


if __name__ == '__main__':
    main()
