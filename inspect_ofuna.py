import sqlite3
DB_PATH = 'backend/zoff_scope_v3.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT id, name, address FROM stores WHERE name LIKE '%大船%'")
for row in cursor.fetchall():
    print(row)
conn.close()
