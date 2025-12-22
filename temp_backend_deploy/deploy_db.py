import requests
import os
import sys

# Configuration
# Backend SCM URL
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
# Assumption: Password is same, Username follows convention
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

LOCAL_DB_PATH = "zoff_scope_v3.db"

print(f"Checking access to {SCM_URL}...")

try:
    # Just check if we can reach it (Head request or similar)
    # VFS api returns file content on GET. GET might be large.
    # We can use requests.head but Kudu might not support it well for VFS?
    # Let's try to list the dir instead to verify auth.
    DIR_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/"
    response = requests.get(DIR_URL, auth=(USER, PASS), timeout=30)
    
    if response.status_code == 200:
        print("Auth Success! Directory listing retrieved.")
        # print("Files:", [f['name'] for f in response.json()][:5])
    else:
        print(f"Auth Failed or Dir not found. Status: {response.status_code}")
        print(response.text[:200])
        sys.exit(1)

    # Proceed to Upload
    print(f"Uploading {LOCAL_DB_PATH}...")
    if not os.path.exists(LOCAL_DB_PATH):
        print("Local DB not found!")
        sys.exit(1)
        
    with open(LOCAL_DB_PATH, 'rb') as f:
        # PUT to upload/replace
        headers = {"If-Match": "*"} # Force overwrite
        resp = requests.put(SCM_URL, data=f, auth=(USER, PASS), headers=headers, timeout=300)
    
    if resp.status_code in [200, 201, 204]:
        print("Upload Success!")
    else:
        print(f"Upload Failed. Status: {resp.status_code}")
        print(resp.text)
        
except Exception as e:
    print(f"Error: {e}")
