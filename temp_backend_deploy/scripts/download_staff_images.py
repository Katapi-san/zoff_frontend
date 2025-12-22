import csv
import requests
import os
import time

CSV_PATH = "new_staff_data.csv"
IMAGE_DIR = "../../apps/customer/public/images/staff/"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Downloading images for {len(rows)} staff...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

for row in rows:
    url = row.get('Image_URL')
    filename = row.get('Image_Filename')
    
    if not url or not filename:
        print(f"Skipping {row.get('Name')}: Missing URL or Filename")
        continue
        
    save_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(save_path):
        print(f"Skipping {filename}: Already exists")
        continue

    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as img_file:
                img_file.write(response.content)
        else:
            print(f"Failed to download {url}: Status {response.status_code}")
        time.sleep(0.2)
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print("Download complete.")
