#!/usr/bin/env python3
"""Simple reclaimer CLI for orchestrator.

Runs `orchestrator.reclaim_stale_tasks(ttl_seconds)` once or in a loop.
Useful as a lightweight, future-upgradeable process (cron/worker).
"""
import argparse
import time
import orchestrator


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--ttl', type=int, default=300, help='TTL seconds for in-progress tasks')
    p.add_argument('--interval', type=int, default=0, help='If >0, run reclaim every N seconds (loop).')
    p.add_argument('--reclaim-max-attempts', type=int, default=3, help='Maximum reclaim attempts before marking failed')
    p.add_argument('--status-file', type=str, default=None, help='Path to write JSON status report')
    p.add_argument('--once', action='store_true', help='Run only once')
    args = p.parse_args(argv)

    if args.once or args.interval <= 0:
        report = orchestrator.reclaim_and_report(args.ttl, max_attempts=args.reclaim_max_attempts, status_path=args.status_file)
        print('reclaimed', report.get('reclaimed'))
        if args.status_file:
            print('status written to', args.status_file)
        return 0

    try:
        while True:
            report = orchestrator.reclaim_and_report(args.ttl, max_attempts=args.reclaim_max_attempts, status_path=args.status_file)
            print('reclaimed', report.get('reclaimed'))
            if args.status_file:
                print('status written to', args.status_file)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
