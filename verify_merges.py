import sqlite3
import os

DB_PATH = 'backend/downloaded_zoff_scope_v3.db'

def check_status():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    checks = [
        (564, 279, "Shimokitazawa"),
        (565, 262, "Lumine Est Shinjuku"),
        (566, 365, "Aeon Mall Kakamigahara"),
        (567, 382, "Aeon Mall Higashiura"),
        (572, 344, "Shonan Mall Fill"),
        (573, 35,  "Grand Emio Tokorozawa"),
        (574, 469, "YouMe Town Marugame"),
        (578, 531, "Diamor Osaka")
    ]

    print(f"Checking DB integrity...")
    failure = False
    for del_id, keep_id, label in checks:
        cursor.execute("SELECT id FROM stores WHERE id = ?", (del_id,))
        res_del = cursor.fetchone()
        
        cursor.execute("SELECT id FROM stores WHERE id = ?", (keep_id,))
        res_keep = cursor.fetchone()

        if res_del:
            print(f"[FAIL] {label}: Old ID {del_id} STILL EXISTS.")
            failure = True
        else:
            # print(f"[PASS] {label}: Old ID {del_id} gone.")
            pass

        if not res_keep:
            print(f"[FAIL] {label}: New ID {keep_id} MISSING.")
            failure = True
    
    conn.close()
    if not failure:
        print("ALL MERGES VERIFIED SUCCESSFULLY.")
    else:
        print("SOME MERGES FAILED.")

if __name__ == "__main__":
    check_status()
