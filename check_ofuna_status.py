import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'

def check_status():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check for requested IDs
    target_ids = [347, 561, 569]
    placeholders = ','.join('?' for _ in target_ids)
    cursor.execute(f"SELECT id, name FROM stores WHERE id IN ({placeholders})", target_ids)
    found = cursor.fetchall()
    
    print(f"Checking for IDs {target_ids}...")
    if found:
        print(f"Found: {found}")
    else:
        print("None of the requested IDs were found.")

    # Check for any Ofuna store
    cursor.execute("SELECT id, name FROM stores WHERE name LIKE '%大船%'")
    ofuna = cursor.fetchall()
    print(f"Existing 'Ofuna' stores: {ofuna}")
    
    conn.close()

if __name__ == "__main__":
    check_status()
