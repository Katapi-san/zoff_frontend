import sqlite3
import os

DB_PATH = 'backend/zoff_scope_v3.db'
TARGET_ID = 29
TARGET_NAME = 'とらいあんぐる'
NEW_IMAGE_URL = 'https://static.staff-start.com/img/staff/icon/388/229118b6b5ec48bd139405e378234df9-125041/aa636ff59983a48cb3c4ef3584dd29a9_m.jpg'

def update_image():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify staff
    cursor.execute("SELECT id, name, image_url FROM staff WHERE id = ?", (TARGET_ID,))
    row = cursor.fetchone()
    
    if not row:
        print(f"Staff with ID {TARGET_ID} not found.")
        # Try finding by name
        cursor.execute("SELECT id, name, image_url FROM staff WHERE name LIKE ?", (f"%{TARGET_NAME}%",))
        row = cursor.fetchone()
        if not row:
            print(f"Staff with name '{TARGET_NAME}' not found.")
            conn.close()
            return
    
    staff_id, staff_name, old_url = row
    print(f"Found Staff: {staff_name} (ID: {staff_id})")
    print(f"Current Image: {old_url}")

    # Update
    cursor.execute("UPDATE staff SET image_url = ? WHERE id = ?", (NEW_IMAGE_URL, staff_id))
    print(f"Updated image URL for ID {staff_id}.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_image()
