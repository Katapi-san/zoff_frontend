import sqlite3
import os
import requests
import sys

# Configuration
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

LOCAL_DB_PATH = 'backend/zoff_scope_v3_fixes.db'

# Merge targets: (source_id, target_id)
# Source will be deleted, staff moved to target.
MERGE_PAIRS = [
    (287, 116),
    (377, 206)
]

def fix_db():
    print(f"Downloading DB from Azure...")
    try:
        resp = requests.get(SCM_URL, auth=(USER, PASS), stream=True, timeout=60)
        if resp.status_code == 200:
            with open(LOCAL_DB_PATH, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download successful.")
        else:
            print(f"Download failed: {resp.status_code}")
            return
    except Exception as e:
        print(f"Download error: {e}")
        return

    print("Connecting to DB...")
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()

    try:
        for source_id, target_id in MERGE_PAIRS:
            print(f"\nProcessing Merge: {source_id} -> {target_id}")
            
            # Check staff
            cursor.execute("SELECT count(*) FROM staff WHERE store_id = ?", (source_id,))
            staff_count = cursor.fetchone()[0]
            print(f"  Staff count in source {source_id}: {staff_count}")

            if staff_count > 0:
                print(f"  Moving staff from {source_id} to {target_id}...")
                cursor.execute("UPDATE staff SET store_id = ? WHERE store_id = ?", (target_id, source_id))
                print(f"  Moved {cursor.rowcount} staff.")
            else:
                print(f"  No staff to move from {source_id}.")

            # Delete source store
            print(f"  Deleting store {source_id}...")
            cursor.execute("DELETE FROM stores WHERE id = ?", (source_id,))
            if cursor.rowcount > 0:
                print(f"  Store {source_id} deleted.")
            else:
                print(f"  Store {source_id} not found or already deleted.")
        
        conn.commit()
    
    except Exception as e:
        print(f"Error during DB operation: {e}")
        conn.close()
        return

    conn.close()
    print("\nDB operations completed.")

    print(f"Uploading updated DB to Azure...")
    try:
        with open(LOCAL_DB_PATH, 'rb') as f:
            headers = {"If-Match": "*"}
            resp = requests.put(SCM_URL, data=f, auth=(USER, PASS), headers=headers, timeout=300)
            
        if resp.status_code in [200, 201, 204]:
            print("Upload Success!")
        else:
            print(f"Upload Failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Upload error: {e}")

if __name__ == "__main__":
    fix_db()
