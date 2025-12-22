import requests
import json
import time
import random

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

trash_suffix = random.randint(1000, 9999)
trash_dir = f"/home/site/trash_{trash_suffix}"

print(f"Creating trash dir {trash_dir}...")
run_command(f"mkdir -p {trash_dir}")

print("Moving .next to trash...")
out = run_command(f"mv .next {trash_dir}/")
print(f"mv .next Output: {out.get('Output')}")
print(f"mv .next Error: {out.get('Error')}")

print("Moving public to trash...")
out = run_command(f"mv public {trash_dir}/")
print(f"mv public Output: {out.get('Output')}")
print(f"mv public Error: {out.get('Error')}")

print("Moving node_modules to trash...")
out = run_command(f"mv node_modules {trash_dir}/")
print(f"mv node_modules Output: {out.get('Output')}")
print(f"mv node_modules Error: {out.get('Error')}")

print("Listing wwwroot...")
run_command("ls -Fa /home/site/wwwroot")
