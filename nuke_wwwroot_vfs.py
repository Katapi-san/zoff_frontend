import requests
import json
import os

URL_VFS = "https://zoff-scope-frontend.scm.azurewebsites.net/api/vfs/tmp/clean.py"
URL_CMD = "https://zoff-scope-frontend.scm.azurewebsites.net/api/command"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"
AUTH = (USER, PASS)

# Python script content
SCRIPT_CONTENT = """
import os
import shutil
import stat
import sys

ROOT = '/home/site/wwwroot'

def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
        print(f"Force deleted: {path}")
    except Exception as e:
        print(f"Failed to force delete {path}: {e}")

print(f"Start cleaning {ROOT}...")

if not os.path.exists(ROOT):
    print(f"{ROOT} does not exist.")
    sys.exit0

for root, dirs, files in os.walk(ROOT, topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        try:
            os.remove(file_path)
        except Exception as e:
            # print(f"Error removing file {file_path}: {e}")
            on_rm_error(os.remove, file_path, None)

    for name in dirs:
        dir_path = os.path.join(root, name)
        try:
            os.rmdir(dir_path)
        except Exception as e:
            # print(f"Error removing dir {dir_path}: {e}")
            on_rm_error(os.rmdir, dir_path, None)

print("Finished cleaning.")
try:
    print("Remaining items:", os.listdir(ROOT))
except Exception as e:
    print(e)
"""

print("1. Uploading script via VFS...")
headers = {"If-Match": "*"} # Overwrite
try:
    response = requests.put(URL_VFS, data=SCRIPT_CONTENT, auth=AUTH, headers=headers, timeout=60)
    print(f"Upload Status: {response.status_code}")
except Exception as e:
    print(f"Upload Failed: {e}")
    exit(1)

print("2. Executing script...")
cmd_payload = {
    "command": "python3 /tmp/clean.py",
    "dir": "/tmp"
}
try:
    response = requests.post(URL_CMD, json=cmd_payload, auth=AUTH, timeout=120)
    print("Execution Output:")
    print(response.json().get('Output'))
    print("Execution Error:")
    print(response.json().get('Error'))
except Exception as e:
    print(f"Execution Failed: {e}")

