"""Simple sequence worker agent.

Claims `.tmp/active_task.json`, processes open todos for the sequence,
marks them done (simulation by default), appends progress and triggers
proposal merge when complete.

Usage:
    python agents/sequence_worker.py --once --simulate
    python agents/sequence_worker.py --poll 10
"""
from pathlib import Path
import time
import argparse
import json
from scripts import sequence_manager as sm


def process_active_once(simulate=True, delay=0.2):
    af = sm.ACTIVE_FILE
    if not af.exists():
        print('No active task.')
        return False
    try:
        active = json.loads(af.read_text(encoding='utf-8'))
        seq_id = active.get('active_sequence')
    except Exception as e:
        print('Failed reading active task:', e)
        return False

    todos = sm._load_todos()
    # collect open todos for seq in order
    open_todos = []
    for k, v in todos.items():
        if v.get('seq_id') == seq_id and v.get('status') != 'done':
            open_todos.append((k, v))
    if not open_todos:
        print('No open todos for', seq_id)
        sm._maybe_finish_sequence(seq_id)
        return True

    # sort by id (which encodes step/sub indexes)
    open_todos.sort()
    for tid, entry in open_todos:
        print('Processing', tid, entry.get('title'))
        # simulate some work
        time.sleep(delay)
        # parse tid to find indices
        parts = tid.split(':')
        if len(parts) == 3:
            _, si, sj = parts
            si = int(si); sj = int(sj)
            sm._mark_todo_done(seq_id, si, sj)
        elif len(parts) == 2:
            _, si = parts
            si = int(si)
            sm._mark_todo_done(seq_id, si, None)
        else:
            # unexpected
            sm._mark_todo_done(seq_id, entry.get('step_index'), entry.get('sub_index'))

    # after processing, attempt finish
    finished = sm._maybe_finish_sequence(seq_id)
    print('Finished:', finished)
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--once', action='store_true')
    p.add_argument('--poll', type=int, default=0, help='poll interval seconds')
    p.add_argument('--simulate', action='store_true', default=True)
    args = p.parse_args()

    if args.once or args.poll <= 0:
        process_active_once(simulate=args.simulate)
        return

    try:
        while True:
            process_active_once(simulate=args.simulate)
            time.sleep(args.poll)
    except KeyboardInterrupt:
        print('Interrupted')


if __name__ == '__main__':
    main()
