import requests
import time
import sys

URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/deployments/latest?deployer=Push-Deployer&time=2025-12-15_12-24-19Z"
# Actually I need to capture the exact URL from previous output or just poll /api/deployments/latest?
# The output snippet above truncated the URL.
# But usually GET /api/deployments/latest returns the status.

USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"
BASE_URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/deployments"

print("Polling deployment status...")
for i in range(20):
    try:
        response = requests.get(f"{BASE_URL}", auth=(USER, PASS), timeout=30)
        data = response.json()
        if data:
            latest = data[0] # List is ordered by time desc
            print(f"Latest ID: {latest.get('id')} Status: {latest.get('status')} Message: {latest.get('message')}")
            
            if latest.get('status') == 4: # Success
                print("Deployment Success!")
                break
            elif latest.get('status') == 3: # Failed
                print("Deployment Failed!")
                break
            else:
                print(f"Current Status: {latest.get('status')} (Building...)")
        else:
            print("No deployments found?")
    except Exception as e:
        print(f"Error polling: {e}")
    
    time.sleep(10)
