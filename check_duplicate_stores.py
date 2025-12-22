import sqlite3
import os
import requests
import sys

# Configuration
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

LOCAL_DB_PATH = 'backend/zoff_scope_v3_check_duplicates.db'

def check_duplicates():
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
        # Normalize names by removing 'Zoff ' prefix and full-width spaces for comparison?
        # For now, let's find EXACT duplicates and "Zoff " prefixed duplicates.
        
        cursor.execute("SELECT id, name FROM stores")
        stores = cursor.fetchall()
        
        # Dictionary to group IDs by name
        name_map = {}
        
        # Helper to normalize store name slightly for better matching
        def normalize(name):
            n = name.replace("Zoff ", "").replace("　", " ").strip()
            return n

        for sid, name in stores:
            norm_name = normalize(name)
            if norm_name not in name_map:
                name_map[norm_name] = []
            name_map[norm_name].append({'id': sid, 'original_name': name})
            
        print("\n--- Duplicate Store Check ---")
        found = False
        for norm_name, items in name_map.items():
            if len(items) > 1:
                found = True
                print(f"\nPotential Duplicates for '{norm_name}':")
                for item in items:
                    # Count staff for each
                    cursor.execute("SELECT count(*) FROM staff WHERE store_id = ?", (item['id'],))
                    count = cursor.fetchone()[0]
                    print(f"  - ID: {item['id']}, Name: '{item['original_name']}', Staff Count: {count}")

        if not found:
            print("No obvious duplicate store names found.")

    except Exception as e:
        print(f"Error during DB operation: {e}")
        conn.close()
        return

    conn.close()

if __name__ == "__main__":
    check_duplicates()
