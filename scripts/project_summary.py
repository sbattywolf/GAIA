#!/usr/bin/env python3
"""
CLI tool to generate project summary and statistics.
Provides a quick command-line view of project status.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = ROOT / 'doc'


def load_ndjson(filepath: Path) -> List[Dict]:
    """Load NDJSON file."""
    if not filepath.exists():
        return []
    
    tasks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    tasks.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return tasks


def load_json(filepath: Path) -> List[Dict]:
    """Load JSON file."""
    if not filepath.exists():
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def print_header(text: str, char='='):
    """Print a formatted header."""
    print()
    print(char * 60)
    print(f"  {text}")
    print(char * 60)


def print_stat(label: str, value, color=''):
    """Print a statistic line."""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    c = colors.get(color, '')
    reset = colors['reset'] if c else ''
    print(f"  {label:.<40} {c}{value}{reset}")


def generate_summary():
    """Generate and display project summary."""
    
    # Load data
    tasks = load_ndjson(DOC_ROOT / 'todo-archive.ndjson')
    agents = load_json(ROOT / 'agents.json')
    
    # Calculate statistics
    total = len(tasks)
    completed = len([t for t in tasks if t.get('status') == 'completed'])
    pending = len([t for t in tasks if t.get('status') == 'pending'])
    in_progress = len([t for t in tasks if t.get('status') == 'in-progress'])
    
    critical = len([t for t in tasks if t.get('priority') == 'critical'])
    high = len([t for t in tasks if t.get('priority') == 'high'])
    medium = len([t for t in tasks if t.get('priority') == 'medium'])
    low = len([t for t in tasks if t.get('priority') == 'low'])
    
    total_hours = sum(t.get('est_hours', 0) for t in tasks)
    completed_hours = sum(t.get('est_hours', 0) for t in tasks if t.get('status') == 'completed')
    
    completion_pct = (completed / total * 100) if total > 0 else 0
    
    # Display summary
    print_header("🚀 GAIA PROJECT SUMMARY", '=')
    print(f"\n  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_header("📊 Task Overview")
    print_stat("Total Tasks", total, 'blue')
    print_stat("Completed", f"{completed} ({completion_pct:.1f}%)", 'green')
    print_stat("In Progress", in_progress, 'yellow')
    print_stat("Pending", pending, 'yellow')
    print()
    
    print_header("⚡ Priority Breakdown")
    print_stat("Critical", critical, 'red' if critical > 0 else '')
    print_stat("High", high, 'yellow' if high > 0 else '')
    print_stat("Medium", medium)
    print_stat("Low", low)
    print()
    
    print_header("⏱️  Time Tracking")
    print_stat("Estimated Hours (Total)", f"{total_hours:.1f}h", 'blue')
    print_stat("Completed Hours", f"{completed_hours:.1f}h", 'green')
    print_stat("Remaining Hours", f"{total_hours - completed_hours:.1f}h", 'yellow')
    hours_pct = (completed_hours / total_hours * 100) if total_hours > 0 else 0
    print_stat("Progress (by hours)", f"{hours_pct:.1f}%")
    print()
    
    print_header("🤖 Agents")
    print_stat("Configured Agents", len(agents), 'blue')
    for agent in agents[:5]:  # Show first 5
        name = agent.get('name', agent.get('id', 'Unknown'))
        print(f"    • {name}")
    if len(agents) > 5:
        print(f"    ... and {len(agents) - 5} more")
    print()
    
    # Recent tasks
    print_header("📝 Recent Tasks")
    sorted_tasks = sorted(tasks, 
                         key=lambda t: t.get('added_at', t.get('last_updated', '')), 
                         reverse=True)
    for task in sorted_tasks[:5]:
        status = task.get('status', 'unknown')
        priority = task.get('priority', 'medium')
        status_icon = '✓' if status == 'completed' else '⧗' if status == 'in-progress' else '○'
        priority_icon = '🔴' if priority == 'critical' else '🟡' if priority == 'high' else '🟢'
        
        print(f"  {status_icon} {priority_icon} {task.get('id', 'N/A'):6s} | {task.get('title', 'No title')[:40]}")
    print()
    
    # Progress bar
    print_header("📈 Overall Progress")
    bar_width = 50
    filled = int(bar_width * completion_pct / 100)
    bar = '█' * filled + '░' * (bar_width - filled)
    print(f"  [{bar}] {completion_pct:.1f}%")
    print()
    
    print("=" * 60)
    print()


def main():
    """Main entry point."""
    try:
        generate_summary()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
