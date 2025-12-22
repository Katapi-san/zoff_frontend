import sqlite3
import os
import requests

DB_PATH = 'backend/zoff_scope_v3.db'
PUBLIC_DIR = 'apps/customer/public'

IMAGES = {
    "イト": "https://static.staff-start.com/img/staff/icon/388/e6d77103ecbcfb21954ef429600e36cc-124970/9d17ba3bd63f3d71315c7e6f5a6be151_s.jpg",
    "uka": "https://static.staff-start.com/img/staff/icon/388/907435acd392a9dccecd313bddb18561-128772/6d8b4dfc8614057702f32be81c8a800e_s.jpg",
    "片田翔悟": "https://static.staff-start.com/img/staff/icon/388/5f984c99f3833955d8ea0b846fe92a3e-124960/59f031216d24c0da45f5a01f198176d1_s.jpg",
    "こーき": "https://static.staff-start.com/img/staff/icon/388/14748aab923ce759b7b800cb1196dc3b-128790/0b73cb1dea3ee748dc797f55311632ac_s.jpg",
    "kitsune": "https://static.staff-start.com/img/staff/icon/388/dcb920588ce6c1faf1368164eee84766-128776/0bec07e6cc110023b7d209e91c0ad7d9_s.jpg"
}

def doit():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Update Images
    for name, url in IMAGES.items():
        cursor.execute("SELECT image_url FROM staff WHERE name LIKE ?", (name,))
        row = cursor.fetchone()
        if not row:
            print(f"Staff {name} not found in DB")
            continue
        
        db_path = row[0]
        if not db_path:
            print(f"Skipping {name}, no image path")
            continue
            
        rel = db_path.lstrip('/')
        local = os.path.join(PUBLIC_DIR, rel.replace('/', os.sep))
        
        print(f"Updating {name} -> {local}")
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(local), exist_ok=True)
                with open(local, 'wb') as f:
                    f.write(resp.content)
                print("  Saved.")
            else:
                print(f"  Failed: {resp.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

    # 2. Update kitsune Store
    print("Updating kitsune store...")
    target_store = "ルミネ有楽町店"
    cursor.execute("SELECT id, name FROM stores WHERE name LIKE ?", ('%' + target_store + '%',))
    row = cursor.fetchone()
    if row:
        store_id = row[0]
        print(f"Found existing store: {row[1]} ({store_id})")
    else:
        print(f"Creating store {target_store}...")
        cursor.execute("INSERT INTO stores (name, prefecture, city, address) VALUES (?, '', '', '')", (target_store,))
        store_id = cursor.lastrowid
    
    cursor.execute("UPDATE staff SET store_id = ? WHERE name LIKE 'kitsune'", (store_id,))
    if cursor.rowcount > 0:
        print("Updated kitsune store_id.")
    else:
        print("kitsune not found for DB update.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    doit()
