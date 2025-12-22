import os
import shutil
import re

TARGET_DIR = "apps/customer/public/images/staff"

def sanitize_filename(name):
    # Convert to lowercase
    new_name = name.lower()
    # Replace non-ascii characters (if any) - though we saw mostly ascii
    # Only allow a-z, 0-9, _, ., -
    # But wait, we want to keep it simple. Just lowercase for now to match API expectations?
    # We should also check what the API expects.
    # If the API has "Tsunakan.jpg" and we verify file is "tsunakan.jpg", that's fine?
    # No, API returned "tsunakan.jpg" (lowercase).
    # Local file might be "Tsunakan.jpg".
    return new_name

print(f"Normalizing filenames in {TARGET_DIR}...")

if not os.path.exists(TARGET_DIR):
    print(f"Directory {TARGET_DIR} not found!")
    exit(1)

count = 0
for filename in os.listdir(TARGET_DIR):
    old_path = os.path.join(TARGET_DIR, filename)
    if os.path.isfile(old_path):
        new_filename = sanitize_filename(filename)
        if new_filename != filename:
            new_path = os.path.join(TARGET_DIR, new_filename)
            # Handle potential collision
            if os.path.exists(new_path) and new_path != old_path:
                print(f"Skipping {filename} -> {new_filename} (Target exists)")
                continue
            
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
            count += 1

print(f"Renamed {count} files.")
