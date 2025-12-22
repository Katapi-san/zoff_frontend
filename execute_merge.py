import sqlite3
import os
import shutil

# We will apply changes to the local main DB file, then deploy it.
DB_PATH = 'backend/zoff_scope_v3.db'
DOWNLOADED_DB_PATH = 'backend/downloaded_zoff_scope_v3.db'

def merge_stores():
    # Ensure we work on the latest data by copying downloaded db to local db path
    # NOTE: This overwrites local DB with the one downloaded from Azure to ensure sync
    if os.path.exists(DOWNLOADED_DB_PATH):
        print(f"Syncing local DB with downloaded DB...")
        shutil.copy2(DOWNLOADED_DB_PATH, DB_PATH)
    else:
        print("Downloaded DB not found. Using local DB existing file.")
    
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # defined as (keep_id, delete_id)
    merges = [
        (531, 578)  # Diamor Osaka
    ]

    try:
        for keep_id, delete_id in merges:
            print(f"Processing Merge: Keep {keep_id} <- Delete {delete_id}")
            
            # 1. Update Staff
            cursor.execute("UPDATE staff SET store_id = ? WHERE store_id = ?", (keep_id, delete_id))
            moved_count = cursor.rowcount
            print(f"  Moved {moved_count} staff members.")

            # 2. Delete Store
            cursor.execute("DELETE FROM stores WHERE id = ?", (delete_id,))
            deleted_count = cursor.rowcount
            if deleted_count > 0:
                print(f"  Deleted store ID {delete_id}.")
            else:
                print(f"  Store ID {delete_id} not found or already deleted.")

        conn.commit()
        print("Merge operation completed successfully.")

    except Exception as e:
        print(f"Error merging stores: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    merge_stores()
