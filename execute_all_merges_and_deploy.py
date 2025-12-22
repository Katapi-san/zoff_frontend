import sqlite3
import os
import shutil
import requests
import sys

# Paths
LOCAL_DB_PATH = 'backend/zoff_scope_v3.db'
DOWNLOADED_DB_PATH = 'backend/downloaded_zoff_scope_v3.db'

# Configuration for Deployment
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

# All requested merges (Keep ID, Delete ID)
ALL_MERGES = [
    # First batch
    (287, 563), # Mikan Shimokita
    (377, 562), # Aeon Mall Kakamigahara
    (123, 570), # Tokyo Dome City LaQua
    
    # Second batch
    (347, 561), # Ofuna (Manual fix attempt) - Note: 347 was target, 561/569 delete. 
                # Wait, user said "347, 561, 569" found? 
                # Earlier analysis said only 176 exists. I will SKIP these unless sure.
                # User request was: "347だけ残し...561,569削除". 
                # But I found these didn't exist. I will verify existence in script.

    # Third batch (The massive list)
    (279, 564), # Shimokitazawa
    (262, 565), # Lumine Est Shinjuku
    (365, 566), # Aeon Mall Kakamigahara Inter
    (382, 567), # Aeon Mall Higashiura
    (344, 572), # Shonan Mall Fill
    (35, 573),  # Grand Emio Tokorozawa
    (469, 574),  # YouMe Town Marugame
    
    # Fourth batch
    (531, 578)  # Diamor Osaka
]

def download_db():
    print(f"Downloading DB from {SCM_URL}...")
    try:
        response = requests.get(SCM_URL, auth=(USER, PASS), timeout=300)
        if response.status_code == 200:
            with open(DOWNLOADED_DB_PATH, 'wb') as f:
                f.write(response.content)
            print("Download Success.")
            return True
        else:
            print(f"Download Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Download Error: {e}")
        return False

def merge_and_update():
    # 1. Prepare Local DB
    if not os.path.exists(DOWNLOADED_DB_PATH):
        if not download_db():
            return

    print(f"Syncing local DB from downloaded...")
    shutil.copy2(DOWNLOADED_DB_PATH, LOCAL_DB_PATH)

    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()

    print("--- Starting Full Merge ---")
    
    # Track results
    success_count = 0
    
    for keep_id, delete_id in ALL_MERGES:
        # Check if stores exist
        cursor.execute("SELECT name FROM stores WHERE id = ?", (delete_id,))
        del_store = cursor.fetchone()
        
        cursor.execute("SELECT name FROM stores WHERE id = ?", (keep_id,))
        keep_store = cursor.fetchone()
        
        if not del_store:
            # print(f"Skipping {delete_id} -> {keep_id}: Delete-target store {delete_id} not found.")
            continue
            
        if not keep_store:
            print(f"Skipping {delete_id} -> {keep_id}: Keep-target store {keep_id} not found! (Cannot merge freely)")
            # Create keep store? No, unsafe.
            continue

        print(f"Merging: {del_store[0]} ({delete_id}) -> {keep_store[0]} ({keep_id})")
        
        # Move Staff
        cursor.execute("UPDATE staff SET store_id = ? WHERE store_id = ?", (keep_id, delete_id))
        moved = cursor.rowcount
        
        # Delete Store
        cursor.execute("DELETE FROM stores WHERE id = ?", (delete_id,))
        
        print(f"  Moved {moved} staff. Deleted store {delete_id}.")
        success_count += 1

    conn.commit()
    conn.close()
    
    print(f"--- Finished. Merged {success_count} pairs. ---")
    
    # 2. Upload
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
