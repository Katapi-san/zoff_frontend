import sqlite3
import os
import requests
import sys

# Configuration
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

LOCAL_DB_PATH = 'backend/zoff_scope_v3_auto_merge.db'

def auto_merge_stores():
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
        # 1. Identify Duplicates
        cursor.execute("SELECT id, name FROM stores")
        stores = cursor.fetchall()
        
        def normalize(name):
            # Normalization logic
            return name.replace("Zoff ", "").replace("Marche ", "").replace("　", " ").strip()

        name_map = {}
        for sid, name in stores:
            norm_name = normalize(name)
            if norm_name not in name_map:
                name_map[norm_name] = []
            
            # Fetch staff count to decide winner
            cursor.execute("SELECT count(*) FROM staff WHERE store_id = ?", (sid,))
            count = cursor.fetchone()[0]
            
            name_map[norm_name].append({
                'id': sid, 
                'original_name': name,
                'staff_count': count
            })

        print("\n--- Starting Auto Merge ---")
        merge_operations = []

        for norm_name, items in name_map.items():
            if len(items) > 1:
                # Decide Winner
                # Priority: 
                # 1. Max Staff Count
                # 2. If staff count equal (e.g. both 0), keep the one with smaller ID (arbitrary stability) 
                #    OR larger ID? Let's check user intent. User said "unify to ID with staff".
                #    If both 0, it doesn't matter much, but let's keep smaller ID usually as "original".
                
                # Sort by staff count (descending), then ID (ascending)
                sorted_items = sorted(items, key=lambda x: (-x['staff_count'], x['id']))
                
                winner = sorted_items[0]
                losers = sorted_items[1:]
                
                print(f"\nProcessing Group: '{norm_name}'")
                print(f"  Winner: ID {winner['id']} ({winner['original_name']}) - Staff: {winner['staff_count']}")
                
                for loser in losers:
                    print(f"  Loser:  ID {loser['id']} ({loser['original_name']}) - Staff: {loser['staff_count']}")
                    merge_operations.append((loser['id'], winner['id']))

        if not merge_operations:
            print("\nNo duplicates to merge.")
            return

        print(f"\nExecuting {len(merge_operations)} merges...")
        
        success_count = 0
        for old_id, new_id in merge_operations:
            try:
                # Move staff (if any exist in loser, though logic usually picks empty ones as losers)
                cursor.execute("UPDATE staff SET store_id = ? WHERE store_id = ?", (new_id, old_id))
                moved = cursor.rowcount
                
                # Delete loser store
                cursor.execute("DELETE FROM stores WHERE id = ?", (old_id,))
                
                print(f"  Merged {old_id} -> {new_id} (Moved {moved} staff)")
                success_count += 1
            except Exception as e:
                print(f"  Error merging {old_id} -> {new_id}: {e}")

        conn.commit()
        print(f"\nSuccessfully processed {success_count} merges.")

    except Exception as e:
        print(f"Error during DB operation: {e}")
        conn.close()
        return

    conn.close()
    
    # Upload
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
    auto_merge_stores()
