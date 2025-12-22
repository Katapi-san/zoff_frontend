import requests
import time

USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"
BASE_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/deployments"

def poll():
    auth = (USER, PASS)
    print("Polling Backend Deployment...")
    for i in range(10):
        try:
            r = requests.get(BASE_URL, auth=auth)
            data = r.json()
            if data:
                latest = data[0]
                print(f"ID: {latest['id']} Status: {latest['status']} (4=Success, 3=Fail)")
                if latest['status'] == 4:
                    print("Deployment Success")
                    return
                if latest['status'] == 3:
                     print("Deployment FAILED")
                     # Try to get log
                     log_url = f"{BASE_URL}/{latest['id']}/log"
                     lr = requests.get(log_url, auth=auth)
                     # Inspect detailed log
                     # Usually list of log entries
                     for entry in lr.json():
                         print(f"{entry['message']}")
                         if entry['details_url']:
                             # Fetch details if needed
                             pass
                     return
            else:
                print("No deployments.")
        except Exception as e:
            print(e)
        time.sleep(5)

if __name__ == "__main__":
    poll()
