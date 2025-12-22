import os
import shutil

TARGET_DIR = "apps/customer/public/images/staff"

print(f"Normalizing filenames in {TARGET_DIR} (force lowercase)...")

if not os.path.exists(TARGET_DIR):
    print(f"Directory {TARGET_DIR} not found!")
    exit(1)

count = 0
for filename in os.listdir(TARGET_DIR):
    # Skip directories
    old_path = os.path.join(TARGET_DIR, filename)
    if not os.path.isfile(old_path):
        continue

    new_filename = filename.lower()
    
    if new_filename != filename:
        temp_path = os.path.join(TARGET_DIR, f"{filename}.tmp")
        new_path = os.path.join(TARGET_DIR, new_filename)
        
        try:
            # Rename to temp
            os.rename(old_path, temp_path)
            # Rename temp to new
            os.rename(temp_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
            count += 1
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

print(f"Renamed {count} files to lowercase.")
