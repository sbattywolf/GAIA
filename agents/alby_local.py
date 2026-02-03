import argparse
import os
from agents.agent_utils import build_event, append_event_atomic, is_dry_run

EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', 'events.ndjson')


def cmd_create_story(args):
    payload = {'title': args.title, 'description': args.description}
    event = build_event('alby.story.created', 'alby.local', payload)
    if args.dry_run or is_dry_run():
        print('[dry-run] would emit event:', event)
    else:
        append_event_atomic(EVENTS_PATH, event)
        print('Emitted event to', EVENTS_PATH)


def cmd_plan_sprint(args):
    payload = {'sprint_name': args.name, 'weeks': args.weeks}
    event = build_event('alby.sprint.planned', 'alby.local', payload)
    if args.dry_run or is_dry_run():
        print('[dry-run] would emit event:', event)
    else:
        append_event_atomic(EVENTS_PATH, event)
        print('Emitted event to', EVENTS_PATH)


def main():
    p = argparse.ArgumentParser(prog='alby-local', description='Alby local agent CLI (GAIA)')
    p.add_argument('--dry-run', action='store_true', help='Do not write events, only print')
    sub = p.add_subparsers(dest='cmd')

    c1 = sub.add_parser('create-story', help='Create a backlog story')
    c1.add_argument('--title', required=True)
    c1.add_argument('--description', default='')
    c1.set_defaults(func=cmd_create_story)

    c2 = sub.add_parser('plan-sprint', help='Plan a sprint')
    c2.add_argument('--name', required=True)
    c2.add_argument('--weeks', type=int, default=2)
    c2.set_defaults(func=cmd_plan_sprint)

    args = p.parse_args()
    if not hasattr(args, 'func'):
        p.print_help()
        return
    args.func(args)


if __name__ == '__main__':
    main()
