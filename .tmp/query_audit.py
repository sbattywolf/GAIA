import sqlite3, json, os
DB='gaia.db'
if not os.path.exists(DB):
    print('gaia.db not found')
    raise SystemExit(0)
con=sqlite3.connect(DB)
cur=con.cursor()
cur.execute('SELECT id,timestamp,actor,action,details FROM audit ORDER BY id DESC LIMIT 10')
rows=cur.fetchall()
for r in rows:
    print(json.dumps({'id':r[0],'timestamp':r[1],'actor':r[2],'action':r[3],'details':r[4]}))
con.close()
