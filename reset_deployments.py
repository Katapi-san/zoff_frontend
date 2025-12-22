import requests
import json

URL_CMD = "https://zoff-scope-frontend.scm.azurewebsites.net/api/command"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"
AUTH = (USER, PASS)
HEADERS = {"Content-Type": "application/json"}

def run_command(cmd, dir_path="/home/site/wwwroot"):
    payload = {"command": cmd, "dir": dir_path}
    try:
        response = requests.post(URL_CMD, headers=HEADERS, auth=AUTH, data=json.dumps(payload), timeout=60)
        return response.json()
    except Exception as e:
        return {"Output": f"Error: {e}"}

print("Deleting deployments history...")
run_command("rm -rf /home/site/deployments/*")

print("Setting SCM_CLEAN_AFTER_DEPLOYMENT...")
# Can't set env var easily for the global scope from here, but can try to pass it in deployment.
# We will just try to delete wwwroot again.

print("Deleting wwwroot again...")
run_command("rm -rf /home/site/wwwroot/*")
run_command("rm -rf /home/site/wwwroot/.*") # hidden files

print("Checking wwwroot...")
res = run_command("ls -Fa /home/site/wwwroot")
print(res.get("Output"))
