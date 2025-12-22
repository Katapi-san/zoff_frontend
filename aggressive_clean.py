import requests
import json

URL_CMD = "https://zoff-scope-frontend.scm.azurewebsites.net/api/command"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"
AUTH = (USER, PASS)
HEADERS = {"Content-Type": "application/json"}

def run_command(cmd, dir_path="/home/site/wwwroot"):
    payload = {
        "command": cmd,
        "dir": dir_path
    }
    try:
        response = requests.post(URL_CMD, headers=HEADERS, auth=AUTH, data=json.dumps(payload), timeout=60)
        print(f"CMD: {cmd}")
        print(f"Status: {response.status_code}")
        print(f"Output: {response.json().get('Output')}")
        print(f"Error: {response.json().get('Error')}")
        print("-" * 20)
    except Exception as e:
        print(f"Exec failed: {e}")

print("--- Starting Aggressive Cleanup ---")

# 1. Try simple rm -rf *
run_command("rm -rf *")

# 2. Try deleting hidden files like .next explicitly
run_command("rm -rf .next")
run_command("rm -rf .git")
run_command("rm -rf .env.production")

# 3. Check what remains
run_command("ls -la")

# 4. If python is available, try to print strict list
run_command("python3 -c \"import os; print(os.listdir('.'))\"")
