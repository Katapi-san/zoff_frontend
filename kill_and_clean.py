import requests
import json
import time

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
        err = response.json().get('Error')
        if err: print(f"Error: {err}")
        print("-" * 20)
    except Exception as e:
        print(f"Exec failed: {e}")

print("--- KILLING NODE ---")
run_command("killall node")
run_command("pkill node")

time.sleep(5)

print("--- NUKING WWWROOT ---")
# Try python script via VFS again, assuming I uploaded it in previous step
run_command("python3 /tmp/clean.py")

print("--- CHECKING STATUS ---")
run_command("ls -Fa /home/site/wwwroot")
run_command("python3 -c \"import os; print(os.listdir('/home/site/wwwroot'))\"")
