import requests
import sqlite3
import os
import time

MERCHANT_ID = "2aab9b0c4ba0e94ad2f011fa10327b76"
API_URL = "https://api.staff-start.com/v1/staff/list/"
DB_PATH = 'backend/zoff_scope_v3.db'
IMAGE_DIR = "apps/customer/public/images/staff/"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all DB staff for cache
cursor.execute("SELECT id, name, store_id, introduction, image_url FROM staff")
db_staff = {row[1]: {'id': row[0], 'store_id': row[2], 'intro': row[3], 'img': row[4]} for row in cursor.fetchall()}

# Get all stores for cache
cursor.execute("SELECT id, name FROM stores")
db_stores = {row[1]: row[0] for row in cursor.fetchall()}

def get_or_create_store(store_name):
    if not store_name: return None
    if store_name in db_stores:
        return db_stores[store_name]
    
    for db_name, sid in db_stores.items():
        if store_name in db_name: 
             return sid
             
    print(f"Creating new store: {store_name}")
    try:
        cursor.execute("INSERT INTO stores (name, prefecture, city, address) VALUES (?, '', '', '')", (store_name,))
        new_id = cursor.lastrowid
        db_stores[store_name] = new_id
        return new_id
    except:
        return None

updated_staff_count = 0
downloaded_images = 0

for page in range(1, 6):
    params = {"merchant_id": MERCHANT_ID, "offset": (page-1)*30, "count": 30}
    try:
        print(f"Fetching API page {page}...")
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("result", []) # API structure v1 is list in 'result'?
        # Wait, previous script used data.get("item", []).
        # Let's check response structure in previous file... it used data.get("item", [])
        # Staff Start V1 usually "result" or "item".
        if "item" in data:
            items = data["item"]
        elif "result" in data:
            items = data["result"]
            
        if not items: 
            print("No items.")
            break
        
        for item in items:
            name = item.get("name")
            shop_name = item.get("shop_name", "")
            comment = item.get("profile", "")
            # Image URL logic
            image_url_l = item.get("resized_image_url_l")
            image_url_m = item.get("resized_image_url_m")
            image_url_s = item.get("resized_image_url_s")
            target_image_url = image_url_l or image_url_m or image_url_s
            
            if not name: continue
            
            if name in db_staff:
                curr = db_staff[name]
                changes = []
                
                # Check Store
                new_store_id = get_or_create_store(shop_name)
                if new_store_id and new_store_id != curr['store_id']:
                    changes.append(f"Store: {curr['store_id']} -> {new_store_id} ({shop_name})")
                    cursor.execute("UPDATE staff SET store_id = ? WHERE id = ?", (new_store_id, curr['id']))
                
                # Check Comment
                db_comment = (curr['intro'] or "").replace('\r\n', '\n').strip()
                api_comment = (comment or "").replace('\r\n', '\n').strip()
                # Only update if API has content and differs significantly (length check?)
                if api_comment and db_comment != api_comment:
                     changes.append("Comment updated")
                     cursor.execute("UPDATE staff SET introduction = ? WHERE id = ?", (api_comment, curr['id']))
                
                # Check Image
                db_img_path = curr['img']
                needs_download = False
                local_path = None
                
                if db_img_path:
                    local_fname = db_img_path.split('/')[-1]
                    local_path = os.path.join(IMAGE_DIR, local_fname)
                    if not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
                        needs_download = True
                else:
                    # DB has no image path. assigning one.
                    import hashlib
                    ext = ".jpg"
                    if target_image_url and ".png" in target_image_url: ext = ".png"
                    # Safe filename hash
                    safe_name = hashlib.md5(name.encode('utf-8')).hexdigest() + ext
                    db_img_path = f"/images/staff/{safe_name}"
                    local_path = os.path.join(IMAGE_DIR, safe_name)
                    needs_download = True
                    changes.append(f"Image Path set to {db_img_path}")
                    cursor.execute("UPDATE staff SET image_url = ? WHERE id = ?", (db_img_path, curr['id']))

                if needs_download and target_image_url:
                    print(f"Downloading image for {name} from {target_image_url}...")
                    try:
                        img_resp = requests.get(target_image_url, timeout=10)
                        if img_resp.status_code == 200:
                            with open(local_path, 'wb') as f:
                                f.write(img_resp.content)
                            downloaded_images += 1
                        else:
                            print(f"Failed DL {target_image_url}: {img_resp.status_code}")
                    except Exception as e:
                        print(f"DL Error: {e}")

                if changes:
                    print(f"Updated {name}: {', '.join(changes)}")
                    updated_staff_count += 1
            
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error page {page}: {e}")

conn.commit()
conn.close()
print(f"Sync complete. Updated {updated_staff_count} staff. Downloaded {downloaded_images} images.")
