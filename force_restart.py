import requests
import time

SCM_URL_BASE = "https://zoff-scope-backend.scm.azurewebsites.net/api"
USER = "$zoff-scope-backend"
PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL"

def restart_site():
    print("Attempting to trigger restart via VFS touch...")
    
    # Touch a file to trigger restart (e.g. web.config or just updating main.py timestamp)
    # Actually, let's just upload a dummy file to wwwroot to see if it works, 
    # but to restart, usually modifying requirements.txt or main startup file works.
    
    # Let's try listing processes first?
    # ps_url = f"{SCM_URL_BASE}/processes"
    # r = requests.get(ps_url, auth=(USER, PASS))
    # print(r.text)
    
    # Simple strategy: Upload a small change to a non-critical file or just re-upload main.py
    # But we don't have main.py locally to upload easily without potentially breaking it if our local is stale.
    
    # Alternative: Use the 'deploy' endpoint to re-deploy the latest commit? No.
    
    # Let's try downloading main.py, appending a newline, and uploading it back.
    vfs_main = f"{SCM_URL_BASE}/vfs/site/wwwroot/main.py"
    
    try:
        r = requests.get(vfs_main, auth=(USER, PASS))
        if r.status_code == 200:
            content = r.text
            # toggle a comment at the end
            if "# RESTART_TRIGGER" in content:
                content = content.replace("# RESTART_TRIGGER", "")
            else:
                content += "\n# RESTART_TRIGGER"
            
            headers = {"If-Match": "*"}
            resp = requests.put(vfs_main, data=content.encode('utf-8'), headers=headers, auth=(USER, PASS))
            if resp.status_code < 300:
                print("Successfully updated main.py to trigger restart.")
            else:
                print(f"Failed to update main.py: {resp.status_code}")
        else:
            print("Could not get main.py")
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    restart_site()
