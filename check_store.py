import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'

def check_store():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM stores WHERE name LIKE '%熊本%'")
    rows = cursor.fetchall()
    print("Stores found:", rows)
    conn.close()

if __name__ == "__main__":
    check_store()
