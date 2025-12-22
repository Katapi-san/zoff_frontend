import requests
import time

URL = "https://zoff-scope-backend.azurewebsites.net/health"

def test_live():
    print(f"Hitting {URL}...")
    try:
        resp = requests.get(URL, timeout=10)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_live()
