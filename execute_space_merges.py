import sqlite3
import os
import shutil
import requests
import sys
from generated_merges import GENERATED_MERGES

# Paths
LOCAL_DB_PATH = 'backend/zoff_scope_v3.db'
DOWNLOADED_DB_PATH = 'backend/downloaded_zoff_scope_v3.db'

# Configuration for Deployment
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

# Add Manual Fixes
MANUAL_MERGES = [
    (491, 581), # サクラマチ クマモト店 <-  サクラマチクマモト店
    (433, 626)  # ららぽーと甲子園店 <-  Zoff ららぽーと甲子園店
]

ALL_MERGES = GENERATED_MERGES + MANUAL_MERGES

def merge_and_update():
    # Sync DB first (already downloaded in previous steps, but good to ensure latest)
    if os.path.exists(DOWNLOADED_DB_PATH):
         print(f"Syncing local DB from downloaded...")
         shutil.copy2(DOWNLOADED_DB_PATH, LOCAL_DB_PATH)
    else:
        print("Downloaded DB not found! Aborting.")
        return

    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()

    print(f"--- Starting Space Merges (Total: {len(ALL_MERGES)}) ---")
    
    success_count = 0
    
    for keep_id, delete_id in ALL_MERGES:
        try:
            # Check existence
            cursor.execute("SELECT name FROM stores WHERE id = ?", (delete_id,))
            del_res = cursor.fetchone()
            if not del_res:
                print(f"Skipping {delete_id}: Not found.")
                continue
            
            cursor.execute("SELECT name FROM stores WHERE id = ?", (keep_id,))
            keep_res = cursor.fetchone()
            if not keep_res:
                print(f"Skipping {keep_id}: Keep target not found.")
                continue

            print(f"Merging: '{del_res[0]}' ({delete_id}) -> '{keep_res[0]}' ({keep_id})")
            
            # Move Staff
            cursor.execute("UPDATE staff SET store_id = ? WHERE store_id = ?", (keep_id, delete_id))
            moved = cursor.rowcount
            
            # Delete Store
            cursor.execute("DELETE FROM stores WHERE id = ?", (delete_id,))
            
            print(f"  Moved {moved} staff. Deleted store {delete_id}.")
            success_count += 1
            
        except Exception as e:
            print(f"Error processing {delete_id}->{keep_id}: {e}")

    conn.commit()
    conn.close()
    
    print(f"--- Finished. Merged {success_count} pairs. ---")
    
    # Upload
    print(f"Uploading modified DB to Azure...")
    with open(LOCAL_DB_PATH, 'rb') as f:
        headers = {"If-Match": "*"}
        resp = requests.put(SCM_URL, data=f, auth=(USER, PASS), headers=headers, timeout=300)
        
    if resp.status_code in [200, 201, 204]:
        print("Upload Success!")
    else:
        print(f"Upload Failed: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    merge_and_update()
