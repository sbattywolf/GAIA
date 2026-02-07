import os, subprocess, sys
os.makedirs('.tmp/pytest', exist_ok=True)
cmd = [sys.executable, '-m', 'pytest', 'tests', '-q', '--basetemp', '.tmp/pytest', '--ignore=tests/test_secrets.py']
print('Running:', ' '.join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print('Return code:', res.returncode)
print(res.stdout)
print(res.stderr)
sys.exit(res.returncode)
