import csv
import os
import shutil
import uuid

CSV_PATH = "zoff_staff_v5_enriched.csv" # Root relative? No, script run in backend/scripts, so ../../zoff_staff_v5_enriched.csv
# Wait, let's allow finding it.
# Assuming running in backend/scripts
CSV_PATH = "../../zoff_staff_v5_enriched.csv"
IMAGE_DIR = "../../apps/customer/public/images/staff/"

temp_rows = []
used_filenames = set()

print("Sanitizing filenames...")

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for i, row in enumerate(reader):
        original_filename = row.get('Image_Filename', '').strip()
        if not original_filename:
            temp_rows.append(row)
            continue
            
        old_path = os.path.join(IMAGE_DIR, original_filename)
        
        # Determine new filename (ASCII safe)
        # Preserve extension
        _, ext = os.path.splitext(original_filename)
        if not ext: ext = ".jpg"
        
        # New name: staff_{i+1}.jpg
        new_filename = f"staff_{i+1:03d}{ext}"
        new_path = os.path.join(IMAGE_DIR, new_filename)
        
        # Rename if exists
        if os.path.exists(old_path):
            try:
                # Check collision (though unlikely with unique index)
                # Rename
                # Handle case where file might already be renamed (if run multiple times)
                # But we rename to new pattern.
                if old_path != new_path:
                    shutil.move(old_path, new_path)
                    print(f"Renamed: {original_filename} -> {new_filename}")
            except Exception as e:
                print(f"Error renaming {original_filename}: {e}")
        elif os.path.exists(new_path):
             # Already renamed presumably
             pass
        else:
             print(f"Warning: File not found {original_filename}")

        # Update CSV row
        row['Image_Filename'] = new_filename
        temp_rows.append(row)

# Write back CSV
with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(temp_rows)

print("CSV updated and files renamed.")
