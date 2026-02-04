#!/usr/bin/env python3
"""Minimal online agent runner for GAIA.

Supports a small set of commands: dry_run, send_telegram, create_issue.
Respects PROTOTYPE_USE_LOCAL_EVENTS and ALLOW_COMMAND_EXECUTION environment flags.
Appends events to `events.ndjson` and writes a short audit row to `gaia.db`.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from typing import Any, Dict

import requests


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def append_event(event: Dict[str, Any]) -> None:
    path = os.path.join(os.getcwd(), "events.ndjson")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def write_audit(trace_id: str, action: str, payload: Dict[str, Any]) -> None:
    db = os.path.join(os.getcwd(), "gaia.db")
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, trace_id TEXT, action TEXT, payload TEXT, ts TEXT)"
        )
        cur.execute(
            "INSERT INTO audit (trace_id, action, payload, ts) VALUES (?, ?, ?, ?)",
            (trace_id, action, json.dumps(payload), now_iso()),
        )
        conn.commit()
    finally:
        try:
            conn.close()
        except Exception:
            pass


def send_telegram(text: str, bot_token: str, chat_id: str) -> Dict[str, Any]:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    resp = requests.post(url, json={"chat_id": chat_id, "text": text})
    resp.raise_for_status()
    return resp.json()


def create_issue(repo: str, title: str, body: str, token: str) -> Dict[str, Any]:
    api = f"https://api.github.com/repos/{repo}/issues"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    resp = requests.post(api, json={"title": title, "body": body}, headers=headers)
    resp.raise_for_status()
    return resp.json()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--command", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--body", default="")
    p.add_argument("--branch", default="")
    args = p.parse_args(argv)

    prototype = os.environ.get("PROTOTYPE_USE_LOCAL_EVENTS", "1") in ("1", "true", "True")
    allow_exec = os.environ.get("ALLOW_COMMAND_EXECUTION", "0") in ("1", "true", "True")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    gh_token = os.environ.get("GITHUB_TOKEN")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    trace_id = f"trace-{int(time.time())}"

    event = {
        "id": trace_id,
        "type": "command",
        "action": args.command,
        "source": "online-agent",
        "actor": "agent:online",
        "payload": {"title": args.title, "body": args.body, "branch": args.branch},
        "timestamp": now_iso(),
        "trace_id": trace_id,
    }

    append_event({**event, "note": "received"})
    write_audit(trace_id, "received_command", event)

    if args.command == "dry_run":
        print("Dry run: appended event and recorded audit.")
        return 0

    if prototype and not allow_exec:
        print("Prototype mode active and ALLOW_COMMAND_EXECUTION not enabled; not executing.")
        append_event({**event, "note": "prototype_skipped"})
        write_audit(trace_id, "skipped_prototype", {})
        return 0

    try:
        if args.command == "send_telegram":
            if not bot_token or not chat_id:
                raise SystemExit("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
            res = send_telegram(args.body or args.title, bot_token, chat_id)
            append_event({**event, "note": "telegram_sent", "result": res})
            write_audit(trace_id, "telegram_sent", res)
            print("Telegram sent.")
            return 0

        if args.command == "create_issue":
            if not repo or not gh_token:
                raise SystemExit("GITHUB_REPOSITORY or GITHUB_TOKEN not set")
            res = create_issue(repo, args.title or "(no title)", args.body or "", gh_token)
            append_event({**event, "note": "issue_created", "result": res})
            write_audit(trace_id, "issue_created", {"issue_url": res.get("html_url")})
            print("Issue created:", res.get("html_url"))
            return 0

        print("Unknown command:", args.command)
        return 2

    except Exception as e:
        append_event({**event, "note": "error", "error": str(e)})
        write_audit(trace_id, "error", {"error": str(e)})
        print("Error:", e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
