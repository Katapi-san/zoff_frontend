import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'
TARGET_STORE_ID = 347
STORES_TO_MERGE = [561, 569]

def merge_stores():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verify Target Store Exists
        cursor.execute("SELECT id, name FROM stores WHERE id = ?", (TARGET_STORE_ID,))
        target_store = cursor.fetchone()
        if not target_store:
            print(f"Target Store ID {TARGET_STORE_ID} not found. Aborting.")
            return
        print(f"Target Store: {target_store[1]} (ID: {target_store[0]})")

        for old_id in STORES_TO_MERGE:
            # Check if old store exists
            cursor.execute("SELECT id, name FROM stores WHERE id = ?", (old_id,))
            old_store = cursor.fetchone()
            
            if not old_store:
                print(f"Store ID {old_id} not found. Skipping.")
                continue

            print(f"Processing Store: {old_store[1]} (ID: {old_store[0]})")

            # Move Staff
            cursor.execute("UPDATE staff SET store_id = ? WHERE store_id = ?", (TARGET_STORE_ID, old_id))
            print(f"  Moved {cursor.rowcount} staff members to Store ID {TARGET_STORE_ID}.")

            # Delete Old Store
            cursor.execute("DELETE FROM stores WHERE id = ?", (old_id,))
            print(f"  Deleted Store ID {old_id}.")

        conn.commit()
        print("Merge completed successfully.")

    except Exception as e:
        print(f"Error during merge: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    merge_stores()
