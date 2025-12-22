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
        response = requests.post(URL_CMD, headers=HEADERS, auth=AUTH, data=json.dumps(payload), timeout=30)
        return response.json()
    except Exception as e:
        return {"Output": f"Error: {e}", "ExitCode": -1}

print("--- 1. Listing files in wwwroot ---")
res = run_command("ls -Fa", "/home/site/wwwroot")
print(res.get("Output"))

print("\n--- 2. Attempting Python-based cleanup (via Kudu python) ---")
# KuduにはPythonがインストールされているため、変なファイル名でもPythonなら削除できる可能性がある
python_cleanup_code = """
import os
import shutil

root_dir = '/home/site/wwwroot'
print(f'Cleaning {root_dir}...')
for item in os.listdir(root_dir):
    item_path = os.path.join(root_dir, item)
    try:
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
            print(f'Deleted file: {item}')
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f'Deleted dir: {item}')
    except Exception as e:
        print(f'Failed to delete {item}: {e}')
"""

# Pythonコードをワンライナーに変換して実行
one_liner = python_cleanup_code.replace('\n', '; ')
cleanup_cmd = f"python -c \"{one_liner}\""
res = run_command(cleanup_cmd)
print("Cleanup Output:")
print(res.get("Output"))

print("\n--- 3. Listing files after cleanup ---")
res = run_command("ls -Fa", "/home/site/wwwroot")
print(res.get("Output"))
