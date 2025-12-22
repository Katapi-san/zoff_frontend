import requests
import os
import time

ZIP_FILE = "frontend_deploy_clean.zip"
URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/zipdeploy"
USER = "$zoff-scope-frontend"
PASS = "2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9"

import zipfile

if not os.path.exists(ZIP_FILE):
    print(f"Error: {ZIP_FILE} not found.")
    exit(1)

# Inspect Zip
try:
    with zipfile.ZipFile(ZIP_FILE, 'r') as z:
        print("Zip content preview:")
        for name in z.namelist()[:5]:
            print(f" - {name}")
        if "package.json" not in z.namelist() and "./package.json" not in z.namelist():
            print("WARNING: package.json not found in root of zip!")
except Exception as e:
    print(f"Error reading zip: {e}")
    exit(1)

file_size = os.path.getsize(ZIP_FILE)
print(f"Uploading {ZIP_FILE} ({file_size} bytes) to {URL}...")

try:
    with open(ZIP_FILE, 'rb') as f:
        # Stream upload with explicit content type
        headers = {'Content-Type': 'application/zip'}
        # Append isAsync=true
        upload_url = f"{URL}?isAsync=true"
        print(f"Posting to {upload_url}...")
        
        response = requests.post(
            upload_url, 
            data=f, 
            auth=(USER, PASS),
            headers=headers,
            timeout=1200
        )
    
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
    
    if response.status_code in [200, 201, 202]:
        print("DEPLOYMENT INITIATED (Async)")
        if response.status_code == 202:
            print("Server accepted the request for processing.")
            # Poll for status? URL is in Location header usually.
            if 'Location' in response.headers:
                print(f"Status URL: {response.headers['Location']}")
    else:
        print("DEPLOYMENT FAILED")
        exit(1)

except Exception as e:
    print(f"Exception during deployment: {e}")
    exit(1)
