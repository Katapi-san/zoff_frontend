import requests
import json

try:
    response = requests.get("http://localhost:8000/stores?prefecture=京都府")
    response.raise_for_status()
    stores = response.json()
    
    print(f"Found {len(stores)} stores in Kyoto.")
    for store in stores:
        print(f"Name: {store['name']}, City: '{store['city']}'")

except Exception as e:
    print(f"Error: {e}")
