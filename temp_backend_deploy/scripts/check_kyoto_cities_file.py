import requests
import json
import os

try:
    response = requests.get("http://localhost:8000/stores?prefecture=京都府")
    response.raise_for_status()
    stores = response.json()
    
    output_path = os.path.join(os.path.dirname(__file__), "kyoto_cities_check.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Found {len(stores)} stores in Kyoto.\n")
        for store in stores:
            f.write(f"Name: {store['name']}, City: '{store['city']}'\n")
    
    print(f"Wrote output to {output_path}")

except Exception as e:
    print(f"Error: {e}")
