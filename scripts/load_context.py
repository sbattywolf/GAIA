#!/usr/bin/env python3
"""
GAIA Context Loader

Loads project context, backlog items, and prepares proposals for GitHub Copilot.
This script helps AI agents and developers quickly understand the current state
of the project and what needs to be done.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def print_header(title: str, char: str = "="):
    """Print a formatted header."""
    print(f"\n{char * 70}")
    print(f"  {title}")
    print(f"{char * 70}\n")


def load_session_state() -> Dict[str, Any]:
    """Load current session state from .copilot/session_state.json."""
    state_file = Path('.copilot/session_state.json')
    
    if not state_file.exists():
        return {
            "status": "NEW_SESSION",
            "message": "No previous session state found"
        }
    
    try:
        with open(state_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to load session state: {e}"
        }


def load_backlog_items() -> List[Dict[str, Any]]:
    """Load backlog items from various sources."""
    items = []
    
    # Check for backlog directories
    backlog_dirs = ['backlogs', 'tasks', 'issues', 'sprints']
    
    for dir_name in backlog_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            continue
        
        # Look for JSON and markdown files
        for file_path in dir_path.glob('**/*'):
            if file_path.suffix in ['.json', '.md']:
                try:
                    item = {
                        'source': str(file_path),
                        'type': file_path.suffix[1:],
                        'name': file_path.stem,
                    }
                    
                    if file_path.suffix == '.json':
                        with open(file_path, 'r') as f:
                            item['content'] = json.load(f)
                    else:
                        with open(file_path, 'r') as f:
                            content = f.read()
                            item['content'] = content[:500]  # First 500 chars
                            item['full_path'] = str(file_path)
                    
                    items.append(item)
                except Exception as e:
                    print(f"Warning: Could not load {file_path}: {e}")
    
    return items


def load_recent_events(max_events: int = 20) -> List[Dict[str, Any]]:
    """Load recent events from events.ndjson."""
    events_file = Path('events.ndjson')
    
    if not events_file.exists():
        return []
    
    events = []
    try:
        with open(events_file, 'r') as f:
            lines = f.readlines()
            # Get last N lines
            for line in lines[-max_events:]:
                if line.strip():
                    events.append(json.loads(line))
    except Exception as e:
        print(f"Warning: Could not load events: {e}")
    
    return events


def analyze_project_structure() -> Dict[str, Any]:
    """Analyze the project structure and key files."""
    structure = {
        'agents': [],
        'scripts': [],
        'docs': [],
        'config_files': [],
    }
    
    # Count agents
    agents_dir = Path('agents')
    if agents_dir.exists():
        structure['agents'] = [
            f.name for f in agents_dir.glob('*.py')
            if f.name != '__init__.py'
        ]
    
    # Count scripts
    scripts_dir = Path('scripts')
    if scripts_dir.exists():
        structure['scripts'] = [
            f.name for f in scripts_dir.glob('*.py')
            if f.name != '__init__.py'
        ][:10]  # Limit to first 10
    
    # Count docs
    doc_dir = Path('doc')
    if doc_dir.exists():
        structure['docs'] = [
            str(f.relative_to(doc_dir))
            for f in doc_dir.glob('**/*.md')
        ][:15]  # Limit to first 15
    
    # Check for key config files
    config_files = [
        'requirements.txt',
        'requirements-dev.txt',
        '.env.example',
        'pytest.ini',
        'orchestrator.py',
        'PLAN.md',
        'TODO.md',
    ]
    
    structure['config_files'] = [
        f for f in config_files
        if Path(f).exists()
    ]
    
    return structure


def generate_context_summary() -> str:
    """Generate a comprehensive context summary."""
    summary = []
    
    summary.append("# GAIA Project Context Summary")
    summary.append(f"Generated: {datetime.now().astimezone().isoformat()}")
    summary.append("")
    
    # Session state
    print_header("Loading Session State")
    state = load_session_state()
    summary.append("## Current Session State")
    summary.append(f"- Status: {state.get('status', 'UNKNOWN')}")
    summary.append(f"- Current Task: {state.get('current_task_id', 'None')}")
    summary.append(f"- Last Sync: {state.get('last_sync', 'Never')}")
    
    if 'steps_completed' in state:
        summary.append(f"- Completed Steps: {len(state['steps_completed'])}")
    
    if 'next_immediate_step' in state:
        summary.append(f"- Next Step: {state['next_immediate_step']}")
    
    summary.append("")
    print(json.dumps(state, indent=2))
    
    # Project structure
    print_header("Analyzing Project Structure")
    structure = analyze_project_structure()
    summary.append("## Project Structure")
    summary.append(f"- Agents: {len(structure['agents'])} files")
    summary.append(f"- Scripts: {len(structure['scripts'])}+ files")
    summary.append(f"- Documentation: {len(structure['docs'])}+ files")
    summary.append("")
    
    if structure['agents']:
        summary.append("### Available Agents")
        for agent in structure['agents'][:5]:
            summary.append(f"  - {agent}")
        if len(structure['agents']) > 5:
            summary.append(f"  - ... and {len(structure['agents']) - 5} more")
        summary.append("")
    
    print(f"Found {len(structure['agents'])} agents, {len(structure['scripts'])} scripts")
    
    # Backlog items
    print_header("Loading Backlog Items")
    backlog = load_backlog_items()
    summary.append("## Backlog Overview")
    summary.append(f"- Total Items: {len(backlog)}")
    summary.append("")
    
    if backlog:
        summary.append("### Recent Backlog Items")
        for item in backlog[:5]:
            summary.append(f"  - [{item['type'].upper()}] {item['name']}")
            summary.append(f"    Source: {item['source']}")
        summary.append("")
    
    print(f"Found {len(backlog)} backlog items")
    
    # Recent events
    print_header("Loading Recent Events")
    events = load_recent_events()
    summary.append("## Recent Activity")
    summary.append(f"- Recent Events: {len(events)}")
    summary.append("")
    
    if events:
        summary.append("### Last 5 Events")
        for event in events[-5:]:
            event_type = event.get('type', 'unknown')
            timestamp = event.get('timestamp', 'unknown')
            source = event.get('source', 'unknown')
            summary.append(f"  - [{event_type}] from {source} at {timestamp}")
        summary.append("")
    
    print(f"Found {len(events)} recent events")
    
    # Key files to review
    summary.append("## Key Files to Review")
    key_files = [
        ('README.md', 'Main project documentation'),
        ('PLAN.md', 'Current implementation plan'),
        ('TODO.md', 'Todo list and pending items'),
        ('.github/copilot-instructions.md', 'Copilot/agent instructions'),
        ('orchestrator.py', 'Main orchestrator service'),
    ]
    
    for file_path, description in key_files:
        if Path(file_path).exists():
            summary.append(f"- `{file_path}`: {description}")
    
    summary.append("")
    
    # Recommendations
    summary.append("## Quick Start Recommendations")
    summary.append("")
    summary.append("1. **Review current session state** in `.copilot/session_state.json`")
    summary.append("2. **Check the plan** in `PLAN.md` for approved work")
    summary.append("3. **Read agent instructions** in `.github/copilot-instructions.md`")
    summary.append("4. **Explore backlog items** in `backlogs/`, `tasks/`, `issues/`")
    summary.append("5. **Tail events** with `Get-Content events.ndjson -Wait -Tail 10`")
    summary.append("")
    
    return "\n".join(summary)


def save_context_file(content: str) -> str:
    """Save context summary to a file."""
    output_dir = Path('.tmp')
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'context_summary_{timestamp}.md'
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    return str(output_file)


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("  GAIA Context Loader")
    print("  Loading project context for development...")
    print("=" * 70 + "\n")
    
    # Change to repo root
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    
    # Generate context
    context = generate_context_summary()
    
    # Save to file
    output_file = save_context_file(context)
    
    # Print summary
    print_header("Context Summary")
    print(context)
    
    print_header("Output Saved")
    print(f"Context summary saved to: {output_file}")
    print("\nYou can now:")
    print("  1. Review the summary above")
    print("  2. Open the saved file for detailed context")
    print("  3. Start working on backlog items")
    print("  4. Ask GitHub Copilot for help with specific tasks")
    print()


if __name__ == '__main__':
    main()
