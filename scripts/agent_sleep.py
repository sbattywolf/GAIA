#!/usr/bin/env python3
import argparse
import time
import signal
import sys

running = True

def handle(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handle)
signal.signal(signal.SIGTERM, handle)

def main():
    p = argparse.ArgumentParser(description='Persistent agent sleep helper')
    p.add_argument('--name', default='agent')
    p.add_argument('--interval', type=int, default=30, help='Heartbeat interval seconds')
    args = p.parse_args()

    print(f"agent_sleep: starting {args.name}", flush=True)
    try:
        while running:
            print(f"agent_sleep: heartbeat {args.name}", flush=True)
            time.sleep(args.interval)
    except Exception as e:
        print(f"agent_sleep: exception {e}", file=sys.stderr, flush=True)
    print(f"agent_sleep: exiting {args.name}", flush=True)

if __name__ == '__main__':
    main()
