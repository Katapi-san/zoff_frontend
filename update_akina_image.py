import sqlite3
import os
import requests
import shutil

DB_PATH = 'backend/zoff_scope_v3.db'
TARGET_NAME = 'akina'
NEW_IMAGE_URL = 'https://static.staff-start.com/img/staff/icon/388/ce8e1c9691c1de7f36f3653e927621a5-125061/693bc29baf055386eb2a22c4341130a1_m.jpg'
PUBLIC_DIR = 'apps/customer/public'

def update_akina_image():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT image_url FROM staff WHERE name = ?", (TARGET_NAME,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"Staff {TARGET_NAME} not found in DB")
        return

    db_image_path = row[0] # e.g. /images/staff/staff_012.jpeg
    print(f"Current image path in DB: {db_image_path}")

    if not db_image_path:
        print("No image path set for this staff.")
        return

    # Convert to local file path
    # db_image_path starts with /, remove it
    rel_path = db_image_path.lstrip('/')
    local_path = os.path.join(PUBLIC_DIR, rel_path.replace('/', os.sep))
    
    print(f"Target local file: {local_path}")
    
    # Download
    print(f"Downloading new image from {NEW_IMAGE_URL}...")
    try:
        resp = requests.get(NEW_IMAGE_URL, timeout=30)
        if resp.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(resp.content)
            print("Download success. File overwritten.")
        else:
            print(f"Download failed: {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_akina_image()
