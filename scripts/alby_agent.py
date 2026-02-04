#!/usr/bin/env python3
"""Lightweight ALby-based local agent scaffold.

Functions:
- find_alby_docs(): scan repo for ALby 0.3 docs (README, CHANGELOG, docs).
- run_archive(): call scripts/version_docs.py --archive
- run_validate(): call scripts/validate_todolists.py
- run_tests(): run pytest for targeted tests
- main(): CLI with --dry-run to show actions

This scaffold is intentionally simple and safe. Expand heuristics as needed.
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
from pathlib import Path
import json
import shutil
from datetime import datetime

try:
    # local orchestrator helper for audit writes
    from orchestrator import write_audit
except Exception:
    write_audit = None

ROOT = Path(__file__).resolve().parent.parent


def find_alby_docs(root: Path = ROOT) -> list[Path]:
    matches: list[Path] = []
    patterns = ["ALby", "Alby", "alby", "ALby-0.3", "alby-0.3", "ALBY"]
    for p in root.rglob("*"):
        if p.is_file():
            name = p.name
            if any(x in name for x in patterns):
                matches.append(p)
            else:
                # quick content search for ALby 0.3 mention in small files
                try:
                    if p.stat().st_size < 200_000:
                        text = p.read_text(encoding='utf-8', errors='ignore')
                        if 'ALby 0.3' in text or 'ALby v0.3' in text or 'alby 0.3' in text:
                            matches.append(p)
                except Exception:
                    pass
    return matches


def run_cmd(cmd: list[str], dry_run: bool = False) -> int:
    print('CMD:', ' '.join(cmd))
    if dry_run:
        return 0
    try:
        r = subprocess.run(cmd, check=False)
        return r.returncode
    except FileNotFoundError:
        print('Command not found:', cmd[0])
        return 127


def run_archive(dry_run: bool = False) -> int:
    script = ROOT / 'scripts' / 'version_docs.py'
    if not script.exists():
        print('Archive script not found:', script)
        return 1
    return run_cmd([sys.executable, str(script), '--archive'], dry_run=dry_run)


def run_validate(dry_run: bool = False) -> int:
    script = ROOT / 'scripts' / 'validate_todolists.py'
    if not script.exists():
        print('Validator not found:', script)
        return 1
    return run_cmd([sys.executable, str(script)], dry_run=dry_run)


def find_todolists_for_story(story_key: str, root: Path = ROOT) -> list[Path]:
    base = root / '.tmp' / 'todolists'
    if not base.exists():
        return []
    matches: list[Path] = []
    for p in base.iterdir():
        if story_key in p.name:
            matches.append(p)
    return matches


def ensure_merged_dir(root: Path = ROOT) -> Path:
    d = root / '.tmp' / 'merged_candidates'
    d.mkdir(parents=True, exist_ok=True)
    return d


def make_merge_candidate(src: Path, dest_dir: Path, actor: str = 'Gise', dry_run: bool = False) -> Path | None:
    name = src.name
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    dest = dest_dir / f"{name}.candidate.{ts}.json"
    print('Prepare candidate:', dest)
    if dry_run:
        return dest
    try:
        # copy original file to candidate with metadata wrapper
        payload = {
            'source': str(src.relative_to(ROOT)),
            'created_at': ts,
            'actor': actor,
            'content': None,
        }
        try:
            payload['content'] = json.loads(src.read_text(encoding='utf-8'))
        except Exception:
            payload['content'] = src.read_text(encoding='utf-8', errors='ignore')
        dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        # write audit row if available
        if write_audit:
            try:
                write_audit(actor or 'Gise', 'merge_candidate_created', json.dumps({'file': str(src), 'candidate': str(dest)}))
            except Exception:
                print('audit write failed')
        return dest
    except Exception as e:
        print('failed to create candidate:', e)
        return None



def run_tests(dry_run: bool = False, targets: list[str] | None = None) -> int:
    cmd = [sys.executable, '-m', 'pytest']
    if targets:
        cmd.extend(targets)
    return run_cmd(cmd, dry_run=dry_run)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', help='Print actions without executing')
    p.add_argument('--run-archive', action='store_true', help='Run archive step')
    p.add_argument('--run-validate', action='store_true', help='Run validator')
    p.add_argument('--run-tests', action='store_true', help='Run pytest')
    p.add_argument('--scan-alby', action='store_true', help='Scan for ALby 0.3 docs')
    p.add_argument('--test-targets', nargs='*', help='pytest targets (optional)')
    p.add_argument('--story', help='Story key to process (e.g., STR_TestGise)')
    p.add_argument('--actor', help='Actor name for audit entries', default='Gise')
    args = p.parse_args()

    if args.scan_alby:
        found = find_alby_docs()
        if not found:
            print('No ALby 0.3 docs found in repo.')
        else:
            print('Found ALby-related files:')
            for f in found:
                print(' -', f.relative_to(ROOT))

    if args.run_archive:
        rc = run_archive(dry_run=args.dry_run)
        print('archive rc=', rc)

    if args.run_validate:
        rc = run_validate(dry_run=args.dry_run)
        print('validate rc=', rc)

    if args.run_tests:
        rc = run_tests(dry_run=args.dry_run, targets=args.test_targets)
        print('tests rc=', rc)

    # Gise-specific story processing
    if getattr(args, 'story', None):
        story = args.story
        actor = getattr(args, 'actor', 'Gise')
        todolists = find_todolists_for_story(story)
        if not todolists:
            print('No todolist files found for story', story)
        else:
            merged_dir = ensure_merged_dir()
            # run validator first (global)
            vrc = run_validate(dry_run=args.dry_run)
            print('global validate rc=', vrc)
            # archive snapshot
            arc_rc = run_archive(dry_run=args.dry_run)
            print('archive rc=', arc_rc)
            for t in todolists:
                cand = make_merge_candidate(t, merged_dir, actor=actor, dry_run=args.dry_run)
                if cand:
                    print('candidate ready:', cand)
                else:
                    print('candidate failed for', t)


if __name__ == '__main__':
    main()
