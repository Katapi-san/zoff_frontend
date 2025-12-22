import requests
import json
import time

MERCHANT_ID = "2aab9b0c4ba0e94ad2f011fa10327b76"
API_URL = "https://api.staff-start.com/v1/staff/list/"

all_staff = []

for page in range(1, 6):
    offset = (page - 1) * 30
    params = {
        "merchant_id": MERCHANT_ID,
        "offset": offset,
        "count": 30 
    }
    
    print(f"Fetching page {page} (offset {offset})...")
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("item", [])
        if not items:
            print("No more items found.")
            break
            
        print(f"Found {len(items)} items.")
        all_staff.extend(items)
        
        time.sleep(1) # Be polite
        
    except Exception as e:
        print(f"Error fetching page {page}: {e}")

print(f"Total staff collected: {len(all_staff)}")

with open("zoff_staff_api_dump.json", "w", encoding="utf-8") as f:
    json.dump(all_staff, f, ensure_ascii=False, indent=2)

print("Saved to zoff_staff_api_dump.json")
