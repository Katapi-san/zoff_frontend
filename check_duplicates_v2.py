import sqlite3
import os
import requests
import sys

# Configuration
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

LOCAL_DB_PATH = 'backend/zoff_scope_v3_space_check.db'

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
        cursor.execute("SELECT id, name FROM stores")
        stores = cursor.fetchall()
        
        # Helper to normalize store name slightly for better matching
        def normalize(name):
            # Remove "Zoff " and "Marche " prefixes
            n = name.replace("Zoff ", "").replace("Marche ", "").replace("　", " ").strip()
            return n

        name_map = {}
        for sid, name in stores:
            norm_name = normalize(name)
            if norm_name not in name_map:
                name_map[norm_name] = []
            name_map[norm_name].append({'id': sid, 'original_name': name})
            
        print("\n--- Duplicate Store Check ---")
        
        found = False
        sorted_names = sorted(name_map.keys())

        # Write to file to avoid encoding issues on stdout
        with open('duplicates_report_utf8.txt', 'w', encoding='utf-8') as f:
            for norm_name in sorted_names:
                items = name_map[norm_name]
                if len(items) > 1:
                    found = True
                    msg = f"\nPotential Duplicates for '{norm_name}':\n"
                    print(msg.strip())
                    f.write(msg)
                    
                    for item in items:
                        # Count staff for each
                        cursor.execute("SELECT count(*) FROM staff WHERE store_id = ?", (item['id'],))
                        count = cursor.fetchone()[0]
                        line = f"  - ID: {item['id']}, Name: '{item['original_name']}', Staff Count: {count}\n"
                        print(line.strip())
                        f.write(line)

        if not found:
            print("No obvious duplicate store names found.")

    except Exception as e:
        print(f"Error during DB operation: {e}")
        conn.close()
        return

    conn.close()

if __name__ == "__main__":
    check_duplicates()
