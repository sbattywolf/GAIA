"""Run a programmatic readiness test: enqueue, verify pending, approve via local CLI.
This is safe to run offline and does not require external Telegram.
"""
import sys, json
sys.path.insert(0, '.')
from importlib import import_module
m = import_module('scripts.tg_command_manager')

print('enqueue test command')
added = m.enqueue_command('local_test_chat', 'msg-run-test', 'run: echo readiness-auto-test', {'first_name':'AutoTester'})
print('added count', len(added))
print('pending file:', m.PENDING)
print(m.PENDING.read_text(encoding='utf-8'))

print('\nlist pending:')
items = m.list_pending()
for i,it in enumerate(items):
    print(i, it.get('id'), it.get('status'), (it.get('command') or '')[:80])

if items:
    cid = items[0]['id']
    print('\napprove via CLI function id=', cid)
    res = m.approve(cid)
    print('approved status=', res.get('status'))

# show events tail
from pathlib import Path
p = Path('events.ndjson')
if p.exists():
    lines = p.read_text(encoding='utf-8').splitlines()
    print('\nlast events:')
    for l in lines[-20:]:
        print(l)

# show recent audit rows
import sqlite3
conn = sqlite3.connect('gaia.db')
cur = conn.cursor()
try:
    cur.execute('SELECT command_id, action, ts FROM command_audit ORDER BY id DESC LIMIT 10')
    rows = cur.fetchall()
    print('\ncommand_audit rows:')
    for r in rows:
        print(r)
except Exception as e:
    print('db error', e)
conn.close()
