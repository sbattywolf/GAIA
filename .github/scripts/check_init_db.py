import orchestrator, sqlite3
orchestrator.init_db()
print('init_db completed, DB path:', orchestrator.DB_PATH)
conn = sqlite3.connect(orchestrator.DB_PATH)
cur = conn.cursor()
cur.execute('PRAGMA table_info(audit)')
cols = [r[1] for r in cur.fetchall()]
print('audit columns:', cols)
conn.close()
