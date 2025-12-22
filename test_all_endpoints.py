import requests

endpoints = [
    "/health",
    "/staffs/?limit=3",
    "/stores/?limit=3",
    "/customers/?limit=3"
]

base_url = "https://zoff-scope-backend.azurewebsites.net"

for endpoint in endpoints:
    url = base_url + endpoint
    print(f"\nTesting: {endpoint}")
    try:
        resp = requests.get(url, timeout=10)
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                print(f"  Items: {len(data)}")
            else:
                print(f"  Response: {data}")
        else:
            print(f"  Error: {resp.text[:200]}")
    except Exception as e:
        print(f"  Failed: {e}")
