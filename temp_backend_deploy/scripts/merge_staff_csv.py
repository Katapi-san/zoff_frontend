import csv
import os
import shutil

EXISTING_CSV_PATH = "../../zoff_staff_v5_enriched.csv"
NEW_DATA_CSV_PATH = "new_staff_data.csv"
BACKUP_CSV_PATH = "../../zoff_staff_v5_enriched.csv.bak"

# 1. Backup existing CSV
if os.path.exists(EXISTING_CSV_PATH):
    shutil.copy2(EXISTING_CSV_PATH, BACKUP_CSV_PATH)
    print(f"Backed up existing CSV to {BACKUP_CSV_PATH}")

# 2. Read Existing Data
existing_data = []
existing_keys = set()

fieldnames = ['Name', 'Shop', 'Face_Type', 'Personal_Color', 'Eye_Position', 'Hair_Style', 'Tags', 'Comment', 'Image_Filename', 'Source_URL']

if os.path.exists(EXISTING_CSV_PATH):
    with open(EXISTING_CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize keys
            clean_row = {k: row.get(k, '') for k in fieldnames}
            existing_data.append(clean_row)
            key = f"{clean_row['Name'].strip()}_{clean_row['Shop'].strip()}"
            existing_keys.add(key)

print(f"Loaded {len(existing_data)} existing records.")

# 3. Read New Data and Append if unique
new_count = 0
updated_count = 0

with open(NEW_DATA_CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Name', '').strip()
        shop = row.get('Shop', '').strip()
        key = f"{name}_{shop}"
        
        # Prepare row matching fieldnames
        clean_row = {k: row.get(k, '') for k in fieldnames}
        
        if key in existing_keys:
            # Optional: Update existing record?
            # For now, let's assume we skip if exact match, or maybe update if new data is 'better'?
            # The scraping script was fetching fresh data. Let's update if we found it again?
            # Actually, let's just append new ones. Logic in import_full_staff_v7 handles dates if present, 
            # but our scraper didn't scrape dates into comments like the previous data seemed to have.
            # We will just skip duplicates to be safe, or we might end up with duplicates in the CSV which the import script handles.
            # The import script aggregates by name, but takes the "latest" based on date in comment.
            # If we don't have a date, it might not overwrite correctly if we just append.
            # However, `import_full_staff_v7` uses `staff_data` dict keyed by Name. 
            # If Name matches, it updates IF the new row has a later date.
            # Our new data has NO date in comment.
            # So `import_full_staff_v7` might strip it or ignore it if we are not careful.
            
            # Let's just Add them to the list. If deduplication is needed, the unique key should prevent adding to `existing_data` list if we check `existing_keys`.
            # But wait, `existing_keys` check above was `continue` if found.
            # So we are skipping duplicates.
            pass
        else:
            existing_data.append(clean_row)
            existing_keys.add(key)
            new_count += 1

print(f"Added {new_count} new records.")

# 4. Write Merged CSV
with open(EXISTING_CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerows(existing_data)

print(f"Saved merged data to {EXISTING_CSV_PATH}")
