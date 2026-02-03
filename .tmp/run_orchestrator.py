import os
import sys
ROOT = os.getcwd()
# ensure local repo root is on sys.path so `import gaia` works
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from gaia import orchestrator

def main():
    print('Starting orchestrator run_sequence (auto_approve=False)')
    rc = orchestrator.run_sequence(auto_approve=False)
    print('orchestrator exit code:', rc)
    return rc

if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
