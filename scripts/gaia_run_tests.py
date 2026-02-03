#!/usr/bin/env python3
"""Lightweight gaia test runner.
Runs quick smoke checks for the CLI and writes a small report.
"""
import subprocess
import json
import os
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPORT = os.path.join(ROOT, '.tmp', 'gaia_test_report.json')

os.makedirs(os.path.join(ROOT, '.tmp'), exist_ok=True)

results = {'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'steps': []}


def run(cmd):
    print('>', ' '.join(cmd))
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False, timeout=120)
        return (0, out.decode('utf-8', errors='ignore'))
    except subprocess.CalledProcessError as e:
        return (e.returncode, e.output.decode('utf-8', errors='ignore') if e.output else str(e))
    except Exception as e:
        return (255, str(e))

# 1. dry-run installer
rc, out = run([ 'python', '-m', 'gaia.cli', 'install' ])
results['steps'].append({'name':'install.dryrun','rc':rc,'out':out})

# 2. list agents
rc, out = run([ 'python', '-m', 'gaia.cli', 'agents', 'list' ])
results['steps'].append({'name':'agents.list','rc':rc,'out':out})

# 3. status
rc, out = run([ 'python', '-m', 'gaia.cli', 'agents', 'status' ])
results['steps'].append({'name':'agents.status','rc':rc,'out':out})

# write report
with open(REPORT, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\nTest report written to', REPORT)
