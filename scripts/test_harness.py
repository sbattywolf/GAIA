"""Local test harness to run secret-based unhappy scenarios and assert expected outputs.

Usage:
  python scripts/test_harness.py --scenario invalid_token

This script is local-only and safe to run. It will load `.tmp/test_secrets/invalid_tokens.env.template`
or `.tmp/test_secrets/invalid_tokens.env` and set env vars accordingly, then attempt to call
`scripts/approval_listener.py` methods in a simulated fashion to assert that failure events are recorded.
"""
import os
import argparse
import time
from importlib import import_module


def load_test_env(path):
    if not os.path.exists(path):
        print('test env not found', path)
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '=' not in line: continue
            k, v = line.split('=', 1)
            os.environ[k.strip()] = v.strip()
    return os.environ


def scenario_invalid_token():
    print('Running invalid_token scenario')
    # load invalid token env
    load_test_env('.tmp/test_secrets/invalid_tokens.env')
    # attempt to call a small helper that uses telegram_client.send_message and should fail
    try:
        tc = import_module('scripts.telegram_client')
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat = os.environ.get('CHAT_ID') or os.environ.get('TELEGRAM_NOTIFY_CHAT')
        print('sending test message (expected to fail)')
        # record audit row count before
        import sqlite3
        before_cnt = 0
        try:
            conn = sqlite3.connect('gaia.db')
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM command_audit')
            before_cnt = cur.fetchone()[0]
            conn.close()
        except Exception:
            before_cnt = None

        failed = False
        exc_message = ''
        try:
            r = tc.send_message(token, chat, 'test invalid token (expected)')
            print('send_message returned:', r)
            failed = False
        except Exception as e:
            exc_message = str(e)
            print('send_message failed as expected:', exc_message)
            failed = True

        # allow some time for events to be written
        time.sleep(0.8)

        # inspect events.ndjson for failure entries
        evt_found = False
        evt_lines = []
        if os.path.exists('events.ndjson'):
            with open('events.ndjson', 'r', encoding='utf-8') as f:
                evt_lines = f.read().splitlines()
            for l in evt_lines[-50:]:
                low = l.lower()
                if 'telegram' in low and ('fail' in low or 'error' in low or 'not found' in low or 'invalid-token-example' in low):
                    evt_found = True
                    break

        # also consider exception message as evidence of failure
        exc_indicates_failure = False
        if exc_message:
            lowe = exc_message.lower()
            if 'not found' in lowe or '404' in lowe or 'invalid' in lowe:
                exc_indicates_failure = True

        # check audit table unchanged (no new executed/approved rows caused by send failure)
        after_cnt = None
        try:
            conn = sqlite3.connect('gaia.db')
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM command_audit')
            after_cnt = cur.fetchone()[0]
            conn.close()
        except Exception:
            after_cnt = None

        print('assertions: send_failed=', failed, 'event_found=', evt_found, 'audit_before=', before_cnt, 'audit_after=', after_cnt)
        # assert conditions: require send failure and either an event or exception message indicating failure
        if not failed:
            raise SystemExit('Expected send_message to fail but it succeeded')
        if not (evt_found or exc_indicates_failure):
            raise SystemExit('Expected telegram failure event or exception indicating failure, but neither found')
        if before_cnt is not None and after_cnt is not None and after_cnt != before_cnt:
            raise SystemExit('Unexpected change in command_audit rows during failure scenario')
        print('invalid_token scenario: OK')
    except Exception as e:
        print('harness error', e)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--scenario', default='invalid_token')
    args = p.parse_args()
    if args.scenario == 'invalid_token':
        scenario_invalid_token()
    else:
        print('unknown scenario')


if __name__ == '__main__':
    main()
