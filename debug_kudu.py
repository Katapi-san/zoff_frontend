import requests

URL_BASE = "https://zoff-scope-frontend.scm.azurewebsites.net/api"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"

print("Checking Auth with GET /deployments...")
try:
    response = requests.get(f"{URL_BASE}/deployments", auth=(USER, PASS), timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response snippet: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
