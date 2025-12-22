import requests
import json
import sys

USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"
BASE_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/LogFiles/"

def get_logs():
    auth = (USER, PASS)
    try:
        resp = requests.get(BASE_URL, auth=auth)
        files = resp.json()
        
        docker_logs = [f for f in files if 'docker' in f['name'].lower()]
        docker_logs.sort(key=lambda x: x['mtime'], reverse=True)
        
        if not docker_logs:
            with open("backend_log_dump.txt", "w") as f:
                f.write("No docker logs found.")
            return

        latest_log = docker_logs[0]
        log_url = latest_log['href']
        
        log_resp = requests.get(log_url, auth=auth)
        content = log_resp.text
        
        with open("backend_log_dump.txt", "w", encoding='utf-8') as f:
            f.write(f"--- Log: {latest_log['name']} ---\n")
            f.write(content)

    except Exception as e:
        with open("backend_log_dump.txt", "w") as f:
            f.write(f"Exception: {e}")

if __name__ == "__main__":
    get_logs()
