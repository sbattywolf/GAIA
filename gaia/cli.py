import argparse
import sys
from . import agent_manager, installer, resource_monitor


def main(argv=None):
    argv = argv or sys.argv[1:]
    p = argparse.ArgumentParser(prog='gaia', description='GAIA developer tooling')
    sub = p.add_subparsers(dest='cmd')

    p_install = sub.add_parser('install', help='Run environment installer (dry-run or apply)')
    p_install.add_argument('--apply', action='store_true')
    p_install.add_argument('--venv', default='.venv')
    p_install.add_argument('--requirements', default='requirements.txt')
    p_install.add_argument('--allow-system', action='store_true')

    p_agents = sub.add_parser('agents', help='Agent operations')
    p_agents.add_argument('action', choices=['list', 'start', 'stop', 'status', 'probe'], help='Action')
    p_agents.add_argument('--agent-id')

    p_monitor = sub.add_parser('monitor', help='Monitor helpers')
    p_monitor.add_argument('action', choices=['status', 'stream'], nargs='?', default='status')

    p_play = sub.add_parser('playbook', help='Playbook utilities')
    p_play.add_argument('action', choices=['list', 'run'], nargs='?', default='list')

    p_report = sub.add_parser('report', help='Reporting utilities')
    p_report.add_argument('--export', choices=['json', 'csv'], default='json')

    p_rm = sub.add_parser('resource', help='Resource monitor')
    p_rm.add_argument('action', choices=['status', 'watch'], nargs='?', default='status')

    p_run = sub.add_parser('run', help='Orchestrate dry-run -> apply with approval checkpoints')
    p_run.add_argument('--auto-approve', action='store_true', help='Proceed to apply without waiting for manual approval')
    p_run.add_argument('--venv', default='.venv')
    p_run.add_argument('--requirements', default='requirements.txt')
    p_run.add_argument('--allow-system', action='store_true')

    args = p.parse_args(argv)

    if args.cmd == 'install':
        return installer.run_apply(apply=args.apply, venv_path=args.venv, requirements=args.requirements, allow_system=args.allow_system)
    if args.cmd == 'agents':
        return agent_manager.handle(args.action, agent_id=args.agent_id)
    if args.cmd == 'monitor':
        return agent_manager.monitor_action(args.action)
    if args.cmd == 'resource':
        return resource_monitor.handle(args.action)
    if args.cmd == 'run':
        from . import orchestrator
        return orchestrator.run_sequence(venv_path=args.venv, requirements=args.requirements, allow_system=args.allow_system, auto_approve=args.auto_approve)
    print('No command specified; use --help')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
