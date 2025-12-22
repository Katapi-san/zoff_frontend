import requests
import json

DIR_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/vfs/site/wwwroot/"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

response = requests.get(DIR_URL, auth=(USER, PASS))
if response.status_code == 200:
    files = response.json()
    for f in files:
        print(f"{f['name']} : {f['size']}")
else:
    print(response.status_code)
