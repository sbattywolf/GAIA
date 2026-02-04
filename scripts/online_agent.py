#!/usr/bin/env python3
"""Minimal online agent runner for GAIA.

Supports a small set of commands: dry_run, send_telegram, create_issue.
Respects PROTOTYPE_USE_LOCAL_EVENTS and ALLOW_COMMAND_EXECUTION environment flags.
Appends events to `events.ndjson` and writes a short audit row to `gaia.db`.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sqlite3
import sys
import time
from typing import Any, Dict, Optional

import requests

# Structured logger
logger = logging.getLogger("online_agent")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


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
        # Ensure compatibility with existing DBs: if the existing `audit` table lacks expected
        # columns, fall back to an alternate table `audit_v2` so we don't fail writes.
        cur.execute("PRAGMA table_info(audit)")
        cols = [r[1] for r in cur.fetchall()]
        if "trace_id" in cols and "payload" in cols:
            cur.execute(
                "INSERT INTO audit (trace_id, action, payload, ts) VALUES (?, ?, ?, ?)",
                (trace_id, action, json.dumps(payload), now_iso()),
            )
        else:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS audit_v2 (id INTEGER PRIMARY KEY, trace_id TEXT, action TEXT, payload TEXT, ts TEXT)"
            )
            cur.execute(
                "INSERT INTO audit_v2 (trace_id, action, payload, ts) VALUES (?, ?, ?, ?)",
                (trace_id, action, json.dumps(payload), now_iso()),
            )
        conn.commit()
    finally:
        try:
            conn.close()
        except Exception:
            pass


def request_with_retry(
    method: str,
    url: str,
    json_payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    max_retries: Optional[int] = None,
) -> Dict[str, Any]:
    # Allow configuration from environment for CI or runtime tuning
    if max_retries is None:
        try:
            max_retries = int(os.environ.get("ONLINE_AGENT_MAX_RETRIES", "3"))
        except Exception:
            max_retries = 3

    base_delay = 1
    try:
        base_delay = float(os.environ.get("ONLINE_AGENT_RETRY_BASE_DELAY", "1"))
    except Exception:
        base_delay = 1

    delay = base_delay
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(json.dumps({"event": "request_attempt", "method": method, "url": url, "attempt": attempt}))
            if method.lower() == "post":
                resp = requests.post(url, json=json_payload, headers=headers, timeout=15)
            else:
                resp = requests.get(url, params=json_payload, headers=headers, timeout=15)
            resp.raise_for_status()
            try:
                return resp.json()
            except ValueError:
                return {"status_code": resp.status_code, "text": resp.text}
        except Exception as e:
            last_err = e
            logger.warning(json.dumps({"event": "request_error", "attempt": attempt, "error": str(e)}))
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
    # Final failure: raise last error for caller to handle
    raise last_err


def send_telegram(text: str, bot_token: str, chat_id: str) -> Dict[str, Any]:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    return request_with_retry("post", url, json_payload={"chat_id": chat_id, "text": text})


def create_issue(repo: str, title: str, body: str, token: str) -> Dict[str, Any]:
    api = f"https://api.github.com/repos/{repo}/issues"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    return request_with_retry("post", api, json_payload={"title": title, "body": body}, headers=headers)


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
