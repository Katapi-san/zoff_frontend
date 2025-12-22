import requests
import json

URL_CMD = "https://zoff-scope-frontend.scm.azurewebsites.net/api/command"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"
AUTH = (USER, PASS)
HEADERS = {"Content-Type": "application/json"}

# Python code to be executed on the server
REMOTE_PYTHON_SCRIPT = """
import os
import shutil
import stat

ROOT = '/home/site/wwwroot'

def on_rm_error(func, path, exc_info):
    # Try to make writable and delete again
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
        print(f"Force deleted: {path}")
    except Exception as e:
        print(f"Failed to force delete {path}: {e}")

print(f"Traversal deletion of {ROOT}...")

for root, dirs, files in os.walk(ROOT, topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        try:
            os.remove(file_path)
            # print(f"Deleted file: {name}") 
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")
            on_rm_error(os.remove, file_path, None)

    for name in dirs:
        dir_path = os.path.join(root, name)
        try:
            os.rmdir(dir_path)
            # print(f"Deleted dir: {name}")
        except Exception as e:
            print(f"Error removing dir {dir_path}: {e}")
            on_rm_error(os.rmdir, dir_path, None)

# Finally check if ROOT is empty
print("Remaining items in wwwroot:")
try:
    print(os.listdir(ROOT))
except Exception as e:
    print(e)
"""

# Helper to escape quotes for the command line
# We will use "python -c 'CODE'" style.
# Need to be careful with newlines. I'll join with newlines escaped or use ;
# Actually best is to write the file to /tmp/nuke.py then run it.

def run_command(cmd, dir_path="/home/site/wwwroot"):
    payload = {"command": cmd, "dir": dir_path}
    try:
        return requests.post(URL_CMD, headers=HEADERS, auth=AUTH, data=json.dumps(payload), timeout=60).json()
    except Exception as e:
        return {"Output": f"Error: {e}"}

print("1. Uploading cleanup script to /tmp/nuke.py")
# We can't easily upload via API without zip. 
# So we will use echo to write the file.
# Note: simple echo might fail with complex chars. 
# Let's try to base64 decode on server? Or just use a very simple python one-liner to write the file.

# Simplify script for one-liner compatibility (semicolons, no comments)
script_oneliner = (
    "import os, shutil, stat; "
    "ROOT='/home/site/wwwroot'; "
    "print(f'Cleaning {ROOT}'); "
    "def handle_err(func, path, exc): "
    "  try: os.chmod(path, stat.S_IWRITE); func(path); print(f'Force del: {path}'); "
    "  except Exception as e: print(f'Fail: {path} {e}'); "
    "for root, dirs, files in os.walk(ROOT, topdown=False): "
    "  for f in files: "
    "    p=os.path.join(root,f); "
    "    try: os.remove(p); "
    "    except: handle_err(os.remove, p, None); "
    "  for d in dirs: "
    "    p=os.path.join(root,d); "
    "    try: os.rmdir(p); "
    "    except: handle_err(os.rmdir, p, None); "
    "print('Done. Remaining:'); "
    "try: print(os.listdir(ROOT)); "
    "except: pass"
)

# Escape double quotes for shell
cmd = f"python3 -c \"{script_oneliner}\""
print("Executing python cleanup...")
res = run_command(cmd)
print(res.get("Output"))
print(res.get("Error"))
