import requests
import json

# Test store detail with staff
store_id = 256  # 適当な店舗ID
url = f"https://zoff-scope-backend.azurewebsites.net/stores/{store_id}/staff"

print(f"Testing: {url}")
try:
    resp = requests.get(url, timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Staff count: {len(data)}")
        if data:
            print(f"First staff: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
    else:
        print(f"Error: {resp.text[:300]}")
except Exception as e:
    print(f"Failed: {e}")

# Test store detail
print(f"\n\nTesting store detail:")
url2 = f"https://zoff-scope-backend.azurewebsites.net/stores/{store_id}"
try:
    resp = requests.get(url2, timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Store: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"Error: {resp.text[:300]}")
except Exception as e:
    print(f"Failed: {e}")
