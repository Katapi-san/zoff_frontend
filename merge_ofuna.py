import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'
TARGET_NAME = '大船ルミネウイング店' 

def merge_ofuna():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get stores with exact name
    cursor.execute("SELECT id, name, address FROM stores WHERE name = ?", (TARGET_NAME,))
    stores = cursor.fetchall()
    
    print(f"Found {len(stores)} stores with exact name '{TARGET_NAME}':")
    for s in stores:
        print(s)
        
    if len(stores) < 2:
        print("Less than 2 stores, nothing to merge.")
        # Check if there are similar names?
        cursor.execute("SELECT id, name FROM stores WHERE name LIKE '%大船%' AND name != ?", (TARGET_NAME,))
        others = cursor.fetchall()
        print(f"Other 'Ofuna' stores: {others}")
    else:
        # Sort by ID. Keep first.
        stores.sort(key=lambda x: x[0])
        keep_id = stores[0][0]
        delete_ids = [s[0] for s in stores[1:]]
        
        print(f"Keeping Store {keep_id}. Deleting {delete_ids}.")
        
        # Move Staff
        placeholders = ','.join('?' for _ in delete_ids)
        cursor.execute(f"UPDATE staff SET store_id = ? WHERE store_id IN ({placeholders})", (keep_id, *delete_ids))
        print(f"Moved {cursor.rowcount} staff.")
        
        # Delete Stores
        cursor.execute(f"DELETE FROM stores WHERE id IN ({placeholders})", delete_ids)
        print(f"Deleted {cursor.rowcount} stores.")

    # Check tsunakan
    cursor.execute("SELECT name, store_id FROM staff WHERE name LIKE '%つなかん%'")
    print("Tsunakan status:", cursor.fetchall())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    merge_ofuna()
