import csv
import requests
import os
import time
import re

CSV_PATH = "zoff_staff_v5_enriched.csv"
IMAGE_DIR = "apps/customer/public/images/staff/"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

print(f"Reading {CSV_PATH}...")
rows = []
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

count_processed = 0
count_success = 0
count_failed = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Regex to find og:image or similar
og_image_pattern = re.compile(r'<meta property="og:image" content="([^"]+)"')
# Fallback: specific class or id? Let's rely on og:image first as it's standard.

for row in rows:
    filename = row.get('Image_Filename', '').strip()
    source_url = row.get('Source_URL', '').strip()
    
    if not filename: continue
    
    save_path = os.path.join(IMAGE_DIR, filename)
    
    # Check if exists
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1000: # Check > 1KB
        continue
    
    if not source_url:
        # print(f"No source URL for {filename}")
        continue

    print(f"[{count_processed+1}/{len(rows)}] missing {filename}. Fetching from {source_url}...")
    
    try:
        # 1. Fetch Page
        page_resp = requests.get(source_url, headers=headers, timeout=15)
        if page_resp.status_code != 200:
            print(f"  -> Page Fetch Failed: {page_resp.status_code}")
            count_failed += 1
            continue
            
        # 2. Extract Image URL
        match = og_image_pattern.search(page_resp.text)
        img_url = ""
        if match:
            img_url = match.group(1)
        else:
            # Try finding main image by common patterns if og:image fails
            # Maybe <img src="..." class="coordinate_image"> ?
            # Not easy to guess. Let's hope og:image works.
            print(f"  -> No og:image found.")
            # Simple fallback: find largest jpg? No.
            count_failed += 1
            continue

        # 3. Download Image
        # print(f"  -> Found Image: {img_url}")
        img_resp = requests.get(img_url, headers=headers, timeout=15)
        if img_resp.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(img_resp.content)
            print(f"  -> Saved.")
            count_success += 1
        else:
            print(f"  -> Image Download Failed: {img_resp.status_code}")
            count_failed += 1
            
        time.sleep(1.0) # Be nice to server

    except Exception as e:
        print(f"  -> Error: {e}")
        count_failed += 1
        
    count_processed += 1

print(f"Done. Success: {count_success}, Failed: {count_failed}")
