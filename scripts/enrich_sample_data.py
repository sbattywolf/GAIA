#!/usr/bin/env python3
"""Sample data enrichment script for GAIA dashboard demonstration.

This script enriches existing tasks with sprint, milestone, and deadline data
to better showcase the enhanced dashboard views (Kanban, Roadmap, Calendar).

Usage:
    python scripts/enrich_sample_data.py
    python scripts/enrich_sample_data.py --preview  # Preview without writing
"""

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_FILE = ROOT / 'doc' / 'todo-archive.ndjson'


def load_tasks():
    """Load tasks from NDJSON file."""
    if not TASKS_FILE.exists():
        print(f"❌ Tasks file not found: {TASKS_FILE}")
        return []
    
    tasks = []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    tasks.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"⚠️  Skipping malformed line: {e}")
    
    return tasks


def save_tasks(tasks):
    """Save tasks back to NDJSON file."""
    backup = TASKS_FILE.with_suffix('.ndjson.backup')
    
    # Create backup
    if TASKS_FILE.exists():
        TASKS_FILE.rename(backup)
        print(f"✓ Created backup: {backup}")
    
    # Write enriched tasks
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        for task in tasks:
            f.write(json.dumps(task, ensure_ascii=False) + '\n')
    
    print(f"✓ Wrote {len(tasks)} enriched tasks to {TASKS_FILE}")


def enrich_tasks(tasks, dry_run=False):
    """Enrich tasks with sprint, milestone, and deadline data."""
    
    # Sprint names
    sprints = [
        'Sprint 1 - Foundation',
        'Sprint 2 - Core Features',
        'Sprint 3 - Integration',
        'Sprint 4 - Polish',
        'Backlog'
    ]
    
    # Milestone options
    milestones = [
        'Q1 2026 - MVP',
        'Q2 2026 - Beta',
        'Q3 2026 - Release',
        'Q4 2026 - Scaling'
    ]
    
    base_date = datetime.now()
    enriched_count = 0
    
    for i, task in enumerate(tasks):
        # Assign sprint (prioritize based on status)
        if 'sprint' not in task:
            if task.get('status') == 'completed':
                task['sprint'] = sprints[0]  # Completed tasks in Sprint 1
            elif task.get('status') == 'in-progress':
                task['sprint'] = sprints[1]  # In-progress in Sprint 2
            else:
                # Distribute pending across sprints based on priority
                if task.get('priority') == 'critical':
                    task['sprint'] = sprints[1]
                elif task.get('priority') == 'high':
                    task['sprint'] = random.choice(sprints[1:3])
                else:
                    task['sprint'] = random.choice(sprints[2:])
            enriched_count += 1
        
        # Assign milestone if high priority or has sprint
        if 'milestone' not in task and task.get('priority') in ['critical', 'high']:
            if task.get('sprint') == sprints[0]:
                task['milestone'] = milestones[0]
            elif task.get('sprint') in [sprints[1], sprints[2]]:
                task['milestone'] = milestones[1]
            else:
                task['milestone'] = milestones[2]
            enriched_count += 1
        
        # Assign deadline (spread over next 60 days)
        if 'deadline' not in task and 'target_date' not in task:
            # Critical and in-progress get near-term deadlines
            if task.get('priority') == 'critical':
                days_offset = random.randint(3, 14)
            elif task.get('status') == 'in-progress':
                days_offset = random.randint(7, 21)
            else:
                days_offset = random.randint(14, 60)
            
            deadline = base_date + timedelta(days=days_offset)
            task['deadline'] = deadline.strftime('%Y-%m-%dT%H:%M:%SZ')
            enriched_count += 1
        
        # Add progress field if missing
        if 'progress' not in task:
            if task.get('status') == 'completed':
                task['progress'] = 100
            elif task.get('status') == 'in-progress':
                task['progress'] = random.randint(25, 75)
            else:
                task['progress'] = 0
    
    print(f"\n📊 Enrichment Summary:")
    print(f"   Total tasks processed: {len(tasks)}")
    print(f"   Fields added/updated: {enriched_count}")
    
    # Distribution summary
    sprint_dist = {}
    for task in tasks:
        sprint = task.get('sprint', 'Unknown')
        sprint_dist[sprint] = sprint_dist.get(sprint, 0) + 1
    
    print(f"\n📋 Sprint Distribution:")
    for sprint, count in sorted(sprint_dist.items()):
        print(f"   {sprint}: {count} tasks")
    
    # Deadline summary
    with_deadline = len([t for t in tasks if 'deadline' in t or 'target_date' in t])
    print(f"\n📅 Deadlines:")
    print(f"   Tasks with deadlines: {with_deadline}/{len(tasks)}")
    
    if dry_run:
        print(f"\n⚠️  DRY RUN MODE - No changes written to file")
        print(f"   Run without --preview to save changes")
    
    return tasks


def show_sample_task(tasks):
    """Show a sample enriched task."""
    if not tasks:
        return
    
    # Find a task with good data
    sample = None
    for task in tasks:
        if 'sprint' in task and 'deadline' in task:
            sample = task
            break
    
    if not sample:
        sample = tasks[0]
    
    print(f"\n📄 Sample Enriched Task:")
    print(json.dumps(sample, indent=2, ensure_ascii=False))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Enrich GAIA task data with sprint, milestone, and deadline information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview enrichment without saving
  python scripts/enrich_sample_data.py --preview

  # Enrich and save
  python scripts/enrich_sample_data.py

  # Show sample task
  python scripts/enrich_sample_data.py --sample

Note: A backup is automatically created before modifying the file.
        """
    )
    
    parser.add_argument('--preview', '--dry-run', action='store_true',
                        help='Preview changes without writing to file')
    parser.add_argument('--sample', action='store_true',
                        help='Show sample enriched task and exit')
    
    args = parser.parse_args()
    
    print("🚀 GAIA Task Data Enrichment")
    print("=" * 60)
    
    # Load tasks
    print(f"📂 Loading tasks from: {TASKS_FILE}")
    tasks = load_tasks()
    
    if not tasks:
        print("❌ No tasks found. Nothing to enrich.")
        return 1
    
    print(f"✓ Loaded {len(tasks)} tasks")
    
    # Enrich tasks
    enriched_tasks = enrich_tasks(tasks, dry_run=args.preview or args.sample)
    
    # Show sample if requested
    if args.sample:
        show_sample_task(enriched_tasks)
        return 0
    
    # Save unless preview mode
    if not args.preview:
        save_tasks(enriched_tasks)
        print(f"\n✅ Task enrichment complete!")
        print(f"   View in enhanced dashboard: http://127.0.0.1:9080/enhanced")
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
