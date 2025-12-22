import requests
import json
import time

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

print("Creating trash dir...")
run_command("mkdir -p /home/site/trash")

print("Moving contents to trash...")
# Try to move all visible files and dirs
run_command("mv /home/site/wwwroot/* /home/site/trash/")
run_command("mv /home/site/wwwroot/.* /home/site/trash/")

print("Checking wwwroot after move...")
res = run_command("ls -la /home/site/wwwroot")
print(res.get("Output"))

print("Deleting trash (async)...")
# We don't care if this finishes
run_command("rm -rf /home/site/trash &")
