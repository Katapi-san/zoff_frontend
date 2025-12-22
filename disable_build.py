import requests
import json

URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/settings"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"

headers = {"Content-Type": "application/json"}
data = {"SCM_DO_BUILD_DURING_DEPLOYMENT": "false"}

print("Setting SCM_DO_BUILD_DURING_DEPLOYMENT=false...")
response = requests.post(URL, data=json.dumps(data), headers=headers, auth=(USER, PASS))

print(f"Status: {response.status_code}")
print(response.text)
