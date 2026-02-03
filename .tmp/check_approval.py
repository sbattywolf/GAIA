import os, json
ROOT = os.getcwd()
appr = os.path.join(ROOT, '.tmp', 'approval.json')
print('approval.json ->', appr)
if os.path.exists(appr):
    print('--- approval.json ---')
    with open(appr, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print('no approval.json')

print('\n--- recent events matching approval ---')
evf = os.path.join(ROOT, 'events.ndjson')
if os.path.exists(evf):
    found = False
    with open(evf, 'r', encoding='utf-8', errors='ignore') as f:
        for line in list(f)[-300:]:
            if 'approval' in line:
                print(line.strip())
                found = True
    if not found:
        print('no approval events in last 300 lines')
else:
    print('events.ndjson not found')

print('\n--- traces table (last 50) filtered for approval (direct sqlite query) ---')
try:
    import sqlite3
    dbp = os.path.join(ROOT, 'gaia.db')
    if os.path.exists(dbp):
        conn = sqlite3.connect(dbp)
        cur = conn.cursor()
        cur.execute("SELECT id,timestamp,action,agent_id,status,details FROM traces ORDER BY id DESC LIMIT 200")
        rows = cur.fetchall()
        conn.close()
        hits = [dict(id=r[0], timestamp=r[1], action=r[2], agent_id=r[3], status=r[4], details=r[5]) for r in rows if r[2] and 'approval' in (r[2] or '')]
        if not hits:
            print('no approval traces')
        else:
            print(json.dumps(hits, indent=2))
    else:
        print('gaia.db not found at', dbp)
except Exception as e:
    print('failed direct sqlite query:', e)
