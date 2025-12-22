import sqlite3
import os
import requests
import shutil

DB_PATH = 'backend/zoff_scope_v3.db'
PUBLIC_DIR = 'apps/customer/public'

UPDATES = {
    "こま": "https://static.staff-start.com/img/staff/icon/388/2a511f83cf2dd20b017ae99136aa4729-124964/44413b7dceea00f4cfff3f883720d26d_m.jpg",
    "Ari": "https://static.staff-start.com/img/staff/icon/388/ff82e4a25d68f8ace3491726270abba2-124944/426246cb0e0ea8ab20aaa81b8b1c1d32_m.jpg",
    "MD": "https://static.staff-start.com/img/staff/icon/388/816f0ac187b26a3368862e48f965f0c8-124997/978c57d449bf4658b983a87fe956007f_s.jpg",
    "Sara": "https://static.staff-start.com/img/staff/icon/388/e19473609605730c4b284dd913e822f9-124928/0c35d007a61e8aee62cb112c3083c83f_s.jpg"
}

def update_images():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for name, url in UPDATES.items():
        # Match case insensitive for safety, though SQLite default LIKE is case-insensitive for ASCII
        cursor.execute("SELECT image_url FROM staff WHERE name LIKE ?", (name,))
        row = cursor.fetchone()
        
        if not row:
            print(f"Skipping {name}: Not found in DB")
            continue
            
        db_image_path = row[0]
        if not db_image_path:
            print(f"Skipping {name}: No image path in DB")
            continue
            
        rel_path = db_image_path.lstrip('/')
        local_path = os.path.join(PUBLIC_DIR, rel_path.replace('/', os.sep))
        
        print(f"Updating {name} -> {local_path} ...")
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(resp.content)
                print(f"  Success.")
            else:
                print(f"  Failed download: {resp.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

    conn.close()

if __name__ == "__main__":
    update_images()
