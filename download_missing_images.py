import csv
import requests
import os
import time

CSV_PATH = "zoff_staff_v5_enriched.csv"
IMAGE_DIR = "apps/customer/public/images/staff/"

# Ensure dir exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

print(f"Reading {CSV_PATH}...")
rows = []
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Found {len(rows)} staff records.")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

count_downloaded = 0
count_failed = 0
count_missing_url = 0

for row in rows:
    filename = row.get('Image_Filename', '').strip()
    # Try different possible column names for Image URL
    url = row.get('Image_URL', '').strip()
    # if not url, maybe it's implicitly derived? 
    # But usually scrapper saves it. Let's check headers later if this fails.
    
    if not filename: 
        continue

    save_path = os.path.join(IMAGE_DIR, filename)
    
    # Check if exists (case insensitive check for Windows, but we want exact mostly)
    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        continue
    
    # Try to find case-insensitive match
    # dir_files = os.listdir(IMAGE_DIR)
    # lower_map = {f.lower(): f for f in dir_files}
    # if filename.lower() in lower_map:
    #    continue
    
    print(f"Missing image: {filename}. URL: {url}")
    
    if not url:
        count_missing_url += 1
        continue
        
    try:
        print(f"Downloading {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f"  -> Saved to {save_path}")
            count_downloaded += 1
        else:
            print(f"  -> Failed: Status {response.status_code}")
            count_failed += 1
        time.sleep(0.5)
    except Exception as e:
        print(f"  -> Error: {e}")
        count_failed += 1

print("------------------------------------------------")
print(f"Download complete. Downloaded: {count_downloaded}, Failed: {count_failed}, No URL: {count_missing_url}")
