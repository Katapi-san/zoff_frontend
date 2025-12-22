import requests
import json

URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/command"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"

headers = {"Content-Type": "application/json"}
# Command to delete all files in wwwroot.
command = {
    "command": "rm -rf /home/site/wwwroot/*",
    "dir": "/home/site/wwwroot"
}

print("Cleaning wwwroot (rm -rf /home/site/wwwroot/*)...")
try:
    response = requests.post(URL, data=json.dumps(command), headers=headers, auth=(USER, PASS), timeout=60)
    print(f"Status: {response.status_code}")
    print("Response snippet:", response.text[:200])
except Exception as e:
    print(f"Error cleaning wwwroot: {e}")
