import sqlite3
import os

DB_PATH = 'backend/downloaded_zoff_scope_v3.db'

def check_target_stores():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    targets = [
        (287, 563, "Mikan Shimokita"),
        (377, 562, "Aeon Mall Kisogawa"),
        (123, 570, "Tokyo Dome City LaQua")
    ]

    print("Checking store existence...")
    for keep_id, delete_id, label in targets:
        print(f"\n--- {label} ---")
        # Check Keep Store
        cursor.execute("SELECT id, name, address FROM stores WHERE id = ?", (keep_id,))
        keep = cursor.fetchone()
        if keep:
            print(f"  KEEP: ID {keep[0]}, Name: {keep[1]}, Addr: {keep[2]}")
        else:
            print(f"  KEEP: ID {keep_id} NOT FOUND")

        # Check Delete Store
        cursor.execute("SELECT id, name, address FROM stores WHERE id = ?", (delete_id,))
        delete = cursor.fetchone()
        if delete:
            print(f"  DEL : ID {delete[0]}, Name: {delete[1]}, Addr: {delete[2]}")
            
            # Check staff count in delete store
            cursor.execute("SELECT count(*) FROM staff WHERE store_id = ?", (delete_id,))
            staff_count = cursor.fetchone()[0]
            print(f"        Staff count to move: {staff_count}")
        else:
            print(f"  DEL : ID {delete_id} NOT FOUND")

    conn.close()

if __name__ == "__main__":
    check_target_stores()
