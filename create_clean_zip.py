import zipfile
import os

SOURCE_DIR = "temp_frontend_sync"
ZIP_FILE = "frontend_deploy_clean.zip"

print(f"Zipping {SOURCE_DIR} to {ZIP_FILE}...")

try:
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(SOURCE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                # Create relative path
                arcname = os.path.relpath(file_path, SOURCE_DIR)
                # Force forward slashes ONLY
                arcname = arcname.replace(os.path.sep, '/')
                z.write(file_path, arcname)
    print("Zip created successfully.")
except Exception as e:
    print(f"Failed to create zip: {e}")
