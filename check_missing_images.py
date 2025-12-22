import sqlite3
import os

db_path = 'backend/zoff_scope_v3.db'
if not os.path.exists(db_path):
    print("DB not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    names = ['akina', 'Ari', 'MD']
    placeholders = ','.join('?' for _ in names)
    cursor.execute(f"SELECT name, image_url FROM staff WHERE name IN ({placeholders})", names)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
