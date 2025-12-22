import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'
TARGET_STAFF = 'つなかん'
TARGET_STORE = '大船ルミネウィング店'

def update_tsunakan():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Find Store
    # Try searching with wildcard
    search_term = '%' + TARGET_STORE.replace('店', '') + '%'
    cursor.execute("SELECT id, name FROM stores WHERE name LIKE ?", (search_term,))
    row = cursor.fetchone()
    
    if row:
        store_id = row[0]
        print(f"Found existing store: {row[1]} (ID: {store_id})")
    else:
        print(f"Store '{TARGET_STORE}' not found. Creating...")
        cursor.execute("INSERT INTO stores (name, prefecture, city, address) VALUES (?, '', '', '')", (TARGET_STORE,))
        store_id = cursor.lastrowid
        print(f"Created store ID: {store_id}")

    # Find Staff
    cursor.execute("SELECT id FROM staff WHERE name LIKE ?", (TARGET_STAFF,))
    staff_row = cursor.fetchone()
    if not staff_row:
        print(f"Staff '{TARGET_STAFF}' not found.")
        conn.close()
        return

    # Update
    cursor.execute("UPDATE staff SET store_id = ? WHERE name LIKE ?", (store_id, TARGET_STAFF))
    print(f"Updated {TARGET_STAFF}'s store to ID {store_id}.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_tsunakan()
