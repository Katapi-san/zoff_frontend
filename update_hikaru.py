import sqlite3
import os
import requests

DB_PATH = 'backend/zoff_scope_v3.db'
PUBLIC_DIR = 'apps/customer/public'

IMAGES = {
    "ひー": "https://static.staff-start.com/img/staff/icon/388/6072be6234defc5778c04d7379646cd4-124924/3942e835ba40cd03b29db31739f4146c_s.jpg",
    "hikaru": "https://static.staff-start.com/img/staff/icon/388/6bc03f27031c8cf1138a797178d771ba-124942/4d072f3983caf993a07d97d94ac82de5_s.jpg"
}

def doit():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Update Images
    for name, url in IMAGES.items():
        # Case insensitive match
        cursor.execute("SELECT image_url FROM staff WHERE name LIKE ?", (name,))
        row = cursor.fetchone()
        if not row:
            print(f"User {name} not found in DB")
            continue
        
        db_path_str = row[0]
        if not db_path_str:
            print(f"Skipping {name}, no image path")
            continue
            
        rel = db_path_str.lstrip('/')
        local = os.path.join(PUBLIC_DIR, rel.replace('/', os.sep))
        
        print(f"Updating image for {name} -> {local}")
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

    # 2. Update hikaru data
    print("Updating hikaru data...")
    # Find/Create Store
    store_name = "サクラマチクマモト店"
    cursor.execute("SELECT id FROM stores WHERE name = ?", (store_name,))
    row = cursor.fetchone()
    if row:
        store_id = row[0]
    else:
        print(f"Creating store {store_name}...")
        cursor.execute("INSERT INTO stores (name, prefecture, city, address) VALUES (?, '', '', '')", (store_name,))
        store_id = cursor.lastrowid
        
    comment = "サクラマチクマモト店に勤務しております。皆様のメガネ選びに貢献できれば嬉しいです☺️"
    cursor.execute("UPDATE staff SET store_id = ?, introduction = ? WHERE name LIKE 'hikaru'", (store_id, comment))
    
    if cursor.rowcount > 0:
        print(f"Updated {cursor.rowcount} row(s) for hikaru.")
    else:
        print("Failed to update hikaru (name not found?)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    doit()
