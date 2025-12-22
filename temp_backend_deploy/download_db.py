import requests
import os
import sys

# Configuration
SCM_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/zoff_scope_v3.db"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

DOWNLOAD_PATH = "downloaded_zoff_scope_v3.db"

print(f"Downloading DB from {SCM_URL}...")

try:
    response = requests.get(SCM_URL, auth=(USER, PASS), timeout=300)
    
    if response.status_code == 200:
        with open(DOWNLOAD_PATH, 'wb') as f:
            f.write(response.content)
        print(f"Download Success! Saved to {DOWNLOAD_PATH}")
    else:
        print(f"Download Failed. Status: {response.status_code}")
        print(response.text[:200])
        sys.exit(1)

except Exception as e:
    print(f"Error: {e}")
