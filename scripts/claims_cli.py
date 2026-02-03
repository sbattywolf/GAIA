import argparse
from scripts import claims


def main():
    p = argparse.ArgumentParser(description='Claims CLI')
    sub = p.add_subparsers(dest='cmd')

    claim_p = sub.add_parser('claim')
    claim_p.add_argument('--story', required=True)
    claim_p.add_argument('--todolist', required=True)
    claim_p.add_argument('--owner', required=True)
    claim_p.add_argument('--agent-id', required=True)
    claim_p.add_argument('--fingerprint', required=True)
    claim_p.add_argument('--ttl', type=int, default=300)

    rel = sub.add_parser('release')
    rel.add_argument('--story', required=True)
    rel.add_argument('--todolist', required=True)
    rel.add_argument('--agent-id')
    rel.add_argument('--fingerprint')

    ins = sub.add_parser('inspect')
    ins.add_argument('--story', required=True)
    ins.add_argument('--todolist', required=True)

    args = p.parse_args()
    if args.cmd == 'claim':
        ok, res = claims.claim(args.story, args.todolist, args.owner, args.agent_id, args.fingerprint, ttl_seconds=args.ttl)
        print({'ok': ok, 'result': res})
    elif args.cmd == 'release':
        ok, res = claims.release(args.story, args.todolist, agent_id=args.agent_id, fingerprint=args.fingerprint)
        print({'ok': ok, 'result': res})
    elif args.cmd == 'inspect':
        info = claims.inspect_claim(args.story, args.todolist)
        print({'claim': info})
    else:
        p.print_help()

if __name__ == '__main__':
    main()
