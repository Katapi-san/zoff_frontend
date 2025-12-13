import requests
import sys

def test_api():
    try:
        response = requests.get("http://localhost:8001/stores")
        if response.status_code == 200:
            stores = response.json()
            print(f"Success! Found {len(stores)} stores.")
            if stores:
                print("Sample store:", stores[0])
                print(f"Name: {stores[0].get('name')}")
                print(f"Hours: {stores[0].get('opening_hours')}")
                print(f"Phone: {stores[0].get('phone_number')}")
        else:
            print(f"Failed. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
