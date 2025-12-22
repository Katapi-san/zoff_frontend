import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'
TARGET_STORE_NAME = '大船ルミネウィング店' # Note: Check variations like 'Zoff 大船...' or '大船ルミネウイング' (small 'i' vs big 'I')

def fix_duplicate_stores():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Inspect variations of Ofuna stores
    # Use wildcard to catch variations
    cursor.execute("SELECT id, name, address FROM stores WHERE name LIKE '%大船%'")
    stores = cursor.fetchall()
    
    print(f"Found {len(stores)} stores matching '大船':")
    valid_store_id = None
    invalid_store_ids = []

    for s in stores:
        sid, name, address = s
        print(f" - ID: {sid}, Name: {name}, Address: {address}")
        # Logic: Valid if address is not empty/null
        if address and str(address).strip():
            if valid_store_id is None:
                valid_store_id = sid
            else:
                print("WARNING: Multiple valid stores with address? Using first one.")
        else:
            invalid_store_ids.append(sid)

    if not valid_store_id:
        print("Error: No valid store with address found! Cannot proceed safely.")
        return

    print(f"Valid Store ID: {valid_store_id}")
    print(f"Invalid Stores to delete: {invalid_store_ids}")

    if not invalid_store_ids:
        print("No invalid stores to process.")
        return

    # 2. Migrate Staff
    # Check staff in invalid stores
    placeholders = ','.join('?' for _ in invalid_store_ids)
    cursor.execute(f"SELECT id, name, store_id FROM staff WHERE store_id IN ({placeholders})", invalid_store_ids)
    staff_to_move = cursor.fetchall()
    
    print(f"Found {len(staff_to_move)} staff to move:")
    for st in staff_to_move:
        print(f" - {st[1]} (from Store {st[2]})")

    if staff_to_move:
        cursor.execute(f"UPDATE staff SET store_id = ? WHERE store_id IN ({placeholders})", (valid_store_id, *invalid_store_ids))
        print(f"Moved {cursor.rowcount} staff to Store {valid_store_id}.")
    
    # 3. Delete Invalid Stores
    cursor.execute(f"DELETE FROM stores WHERE id IN ({placeholders})", invalid_store_ids)
    print(f"Deleted {cursor.rowcount} invalid stores.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_duplicate_stores()
