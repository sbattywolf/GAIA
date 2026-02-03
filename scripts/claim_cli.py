#!/usr/bin/env python3
"""Small CLI wrapper for claim operations (inspect, claim, release, refresh).

Usage examples:
  python scripts/claim_cli.py inspect my_story default
  python scripts/claim_cli.py claim my_story default owner agent-id fp-123
  python scripts/claim_cli.py release my_story default --agent agent-id
  python scripts/claim_cli.py refresh my_story default --agent agent-id
"""
import argparse
import json
import sys

from scripts import claims


def eprint(*a, **k):
    print(*a, file=sys.stderr, **k)


def cmd_inspect(args):
    res = claims.inspect_claim(args.story, args.todolist)
    print(json.dumps(res, indent=2, default=str))
    return 0


def cmd_claim(args):
    ok, payload = claims.claim(
        args.story, args.todolist, args.owner, args.agent, args.fingerprint, ttl_seconds=args.ttl
    )
    print(json.dumps({"ok": ok, "result": payload}, indent=2, default=str))
    return 0 if ok else 1


def cmd_release(args):
    ok, payload = claims.release(args.story, args.todolist, agent_id=args.agent, fingerprint=args.fingerprint)
    print(json.dumps({"ok": ok, "result": payload}, indent=2, default=str))
    return 0 if ok else 1


def cmd_refresh(args):
    ok, payload = claims.refresh(args.story, args.todolist, agent_id=args.agent, fingerprint=args.fingerprint, ttl_seconds=args.ttl)
    print(json.dumps({"ok": ok, "result": payload}, indent=2, default=str))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="claim_cli")
    sp = p.add_subparsers(dest="cmd")

    p_ins = sp.add_parser("inspect")
    p_ins.add_argument("story")
    p_ins.add_argument("todolist")
    p_ins.set_defaults(func=cmd_inspect)

    p_claim = sp.add_parser("claim")
    p_claim.add_argument("story")
    p_claim.add_argument("todolist")
    p_claim.add_argument("owner")
    p_claim.add_argument("agent")
    p_claim.add_argument("fingerprint")
    p_claim.add_argument("--ttl", type=int, default=300)
    p_claim.set_defaults(func=cmd_claim)

    p_rel = sp.add_parser("release")
    p_rel.add_argument("story")
    p_rel.add_argument("todolist")
    p_rel.add_argument("--agent", dest="agent", default=None)
    p_rel.add_argument("--fingerprint", dest="fingerprint", default=None)
    p_rel.set_defaults(func=cmd_release)

    p_ref = sp.add_parser("refresh")
    p_ref.add_argument("story")
    p_ref.add_argument("todolist")
    p_ref.add_argument("--agent", dest="agent", default=None)
    p_ref.add_argument("--fingerprint", dest="fingerprint", default=None)
    p_ref.add_argument("--ttl", type=int, default=None)
    p_ref.set_defaults(func=cmd_refresh)

    args = p.parse_args(argv)
    if not hasattr(args, "func"):
        p.print_help()
        return 2
    try:
        return args.func(args)
    except Exception as e:
        eprint("error:", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
