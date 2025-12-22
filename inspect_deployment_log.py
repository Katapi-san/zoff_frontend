import requests
import json

URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/deployments"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"

try:
    response = requests.get(URL, auth=(USER, PASS), timeout=30)
    deployments = response.json()
    
    if deployments:
        latest = deployments[0]
        deploy_id = latest['id']
        print(f"Latest Deployment ID: {deploy_id}, Status: {latest['status']}")
        
        # Get log for this deployment
        log_url = f"{URL}/{deploy_id}/log"
        log_response = requests.get(log_url, auth=(USER, PASS), timeout=30)
        logs = log_response.json()
        
        print("Deployment Logs:")
        for entry in logs:
            print(f" - {entry.get('message')} (Details: {entry.get('details_url')})")
            if entry.get('details_url'):
                 # Fetch details if it's a failure
                 details_response = requests.get(entry.get('details_url'), auth=(USER, PASS), timeout=30)
                 print(details_response.text[:1000]) # Print first 1000 chars of details

    else:
        print("No deployments found.")

except Exception as e:
    print(f"Error: {e}")
