#!/usr/bin/env python3
"""Lightweight scheduler for repository tasks.

Usage:
  python scripts/ascheduler.py --config scripts/ascheduler_config.json
  python scripts/ascheduler.py --run-once telegram

The config file is JSON with an array of tasks. Each task:
  {
    "name": "telegram",
    "interval_minutes": 30,
    "command": ["python", "scripts/telegram_summary.py"],
    "env": { "PROTOTYPE_USE_LOCAL_EVENTS": "0" }
  }

This script launches a background thread per task that runs the command
on the configured interval. It's intentionally small and dependency-free.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import shlex
import subprocess
import threading
import time
from typing import Any, Dict


LOG = logging.getLogger("ascheduler")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")


def run_command(task: Dict[str, Any], once: bool = False) -> None:
    name = task.get("name", "unnamed")
    cmd = task.get("command")
    interval = int(task.get("interval_minutes", 0))
    env_overrides = task.get("env", {}) or {}

    if not cmd:
        LOG.error("Task %s has no command, skipping", name)
        return

    def _run_loop():
        while True:
            LOG.info("Running task %s: %s", name, cmd)
            try:
                env = os.environ.copy()
                env.update({k: str(v) for k, v in env_overrides.items()})
                # allow either list or string commands
                if isinstance(cmd, str):
                    proc = subprocess.run(shlex.split(cmd), env=env)
                else:
                    proc = subprocess.run([str(c) for c in cmd], env=env)
                LOG.info("Task %s exited with %s", name, proc.returncode)
            except Exception as e:
                LOG.exception("Task %s failed: %s", name, e)

            if once or interval <= 0:
                break

            time.sleep(interval * 60)

    t = threading.Thread(target=_run_loop, name=f"ascheduler-{name}")
    t.daemon = True
    t.start()


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="scripts/ascheduler_config.json")
    parser.add_argument("--run-once", help="Run a single task by name and exit")
    args = parser.parse_args()

    config = load_config(args.config)
    tasks = config.get("tasks", []) if isinstance(config, dict) else list(config)

    if args.run_once:
        task = next((t for t in tasks if t.get("name") == args.run_once), None)
        if not task:
            LOG.error("No task named %s found in %s", args.run_once, args.config)
            raise SystemExit(2)
        run_command(task, once=True)
        return

    # start all tasks
    for task in tasks:
        run_command(task)

    try:
        # keep main thread alive while background threads run
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        LOG.info("ascheduler: exiting on keyboard interrupt")


if __name__ == "__main__":
    main()
