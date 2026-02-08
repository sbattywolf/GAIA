import json
import sys


def main():
    try:
        baseline = json.load(open('.secrets.baseline'))
    except Exception:
        baseline = {'results': {}}
    scan = json.load(open('scan.json'))
    base_files = set(baseline.get('results', {}).keys())
    scan_files = set(scan.get('results', {}).keys())
    new_files = sorted(list(scan_files - base_files))
    if new_files:
        print('New potential secrets found in files:')
        for f in new_files:
            print(' -', f)
        print('\nIf these are expected, update .secrets.baseline by running:\n  pip install detect-secrets\n  detect-secrets scan > .secrets.baseline\n')
        sys.exit(1)
    print('No new potential secrets found versus baseline.')


if __name__ == '__main__':
    main()
