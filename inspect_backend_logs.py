import requests
import re

USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"
BASE_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/LogFiles/"

import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_logs():
    auth = (USER, PASS)
    try:
        print(f"DEBUG: Listing {BASE_URL}...")
        resp = requests.get(BASE_URL, auth=auth)
        print(f"DEBUG: Status Code: {resp.status_code}")
        files = resp.json()
        print(f"DEBUG: Found {len(files)} files.")
        
        print(f"File list:")
        for f in files:
            print(f" - {f['name']} ({f['mtime']})")

        # Prioritize python_app.log
        python_logs = [f for f in files if 'python_app.log' in f['name']]
        log_files = python_logs if python_logs else [f for f in files if f['name'].endswith('.log') or f['name'].endswith('.txt')]
        
        log_files.sort(key=lambda x: x['mtime'], reverse=True)
        
        if log_files:
            target = log_files[0]
            print(f"Reading most recent log: {target['name']}...")
            r = requests.get(target['href'], auth=auth)
            # Handle encoding issues manually if needed, but requests.text usually guesses well
            content = r.text
            
            print(f"--- Last 100 lines of {target['name']} ---")
            lines = content.splitlines()
            for line in lines[-100:]:
                print(line)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    get_logs()
