import sys
import os
import csv
import argparse

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Tag, StaffTag, Store

def import_staff_from_csv(csv_file_path):
    db = SessionLocal()
    
    # Cache existing tags to avoid repeated queries
    existing_tags = {tag.name: tag for tag in db.query(Tag).all()}
    
    def get_tag_if_exists(tag_name):
        return existing_tags.get(tag_name)



    def get_store_id(name_part):
        if not name_part:
            # Default to first store if no shop name provided
            return db.query(Store).first().id
            

        # Manual mappings for known CSV inconsistencies
        manual_map = {
            "サクラマチクマモト店": "サクラマチ クマモト店"
        }
        if name_part in manual_map:
            name_part = manual_map[name_part]
        elif "サクラマチ" in name_part:
            name_part = "サクラマチ クマモト店"

        # 1. Try exact match (approximate with like for safety)
        store = db.query(Store).filter(Store.name.like(f"%{name_part}%")).first()
        if store:
            return store.id

        # Special handling for "本社" (Headquarters)
        if name_part == "本社":
            # Check if exists
            hq = db.query(Store).filter(Store.name == "本社").first()
            if not hq:
                print("Creating '本社' store...")
                hq = Store(
                    name="本社", 
                    prefecture="東京都", 
                    city="港区", 
                    address="北青山3-6-1", # Dummy or real Zoff HQ address
                    opening_hours="9:30 - 18:30",
                    phone_number="",
                    remarks="Headquarters"
                )
                db.add(hq)
                db.commit()
                db.refresh(hq)
            return hq.id

        # 2. Try variations
        variations = [
            name_part.replace('ウィ', 'ウイ'),
            name_part.replace('ウイ', 'ウィ'),
            name_part.replace('ヴェ', 'ベ'),
            name_part.replace('ヴァ', 'バ'),
            # Handle generic "Zoff" prefix if it was in CSV but not in DB
            name_part.replace('Zoff ', ''), 
             # Handle "Marche " prefix if in DB but not CSV
             # But we are searching DB with LIKE, so "StoreName" matches "Marche StoreName".
             # The reverse: CSV has "Marche StoreName" and DB has "StoreName".
             name_part.replace('Marche ', ''),
             name_part.replace('Marché ', ''),
        ]
        
        for v in variations:
            if v == name_part: continue
            store = db.query(Store).filter(Store.name.like(f"%{v}%")).first()
            if store:
                print(f"  Matched '{name_part}' to '{store.name}' using variation '{v}'")
                return store.id

        print(f"ERROR: Store matching '{name_part}' not found. Using first available store.")
        return db.query(Store).first().id

    try:
        # Clear existing data
        print("Clearing existing staff data...")
        db.query(StaffTag).delete()
        db.query(Staff).delete()
        db.commit()
        print("Existing staff data cleared.")

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            print(f"CSV Headers: {reader.fieldnames}")
            
            for row in reader:
                # Debug print
                # print(f"Row keys: {row.keys()}")
                # Skip empty rows
                if not row.get('Name'):
                    continue

                print(f"Importing {row['Name']}...")
                
                # Aggregate Tags from various columns
                tags_list = []
                
                # Face Type
                if row.get('Face_Type'):
                    val = row['Face_Type'].strip()
                    if not val.startswith('#'): val = '#' + val
                    tags_list.append(val)
                
                # Personal Color
                if row.get('Personal_Color'):
                    val = row['Personal_Color'].strip()
                    if not val.startswith('#'): val = '#' + val
                    tags_list.append(val)
                
                # Eye Position
                if row.get('Eye_Position'):
                    val = row['Eye_Position'].strip()
                    # Simplify complex values if needed, or keep as is. Taking as is for now.
                    if not val.startswith('#'): val = '#' + val
                    tags_list.append(val)
                
                # Hair Style
                if row.get('Hair_Style'):
                    val = row['Hair_Style'].strip()
                    if not val.startswith('#'): val = '#' + val
                    tags_list.append(val)
                
                # General Tags column
                if row.get('Tags'):
                    raw_tags = row['Tags'].replace('、', ',').replace(' ', ',') 
                    for t in raw_tags.split(','):
                        t = t.strip()
                        if t:
                            if not t.startswith('#'): t = '#' + t
                            tags_list.append(t)

                # Tags-skill
                if row.get('Tags-skill'):
                    raw_tags = row['Tags-skill'].replace('、', ',').replace(' ', ',') 
                    for t in raw_tags.split(','):
                        t = t.strip()
                        if t:
                            if not t.startswith('#'): t = '#' + t
                            tags_list.append(t)

                # Tags-Hobby
                if row.get('Tags-Hobby'):
                    raw_tags = row['Tags-Hobby'].replace('、', ',').replace(' ', ',') 
                    for t in raw_tags.split(','):
                        t = t.strip()
                        if t:
                            if not t.startswith('#'): t = '#' + t
                            tags_list.append(t)
                
                # Remove duplicates
                tags_list = list(set(tags_list))


                # Get Store ID
                store_query = row.get('Shop', '').strip()
                store_id = get_store_id(store_query)
                
                # Image Path construction
                image_filename = row.get('Image_Filename', '')
                # Assuming images are stored in /images/staff/
                image_url = f"/images/staff/{image_filename}" if image_filename else ""

                # Create Staff object
                staff_data = {
                    "name": row['Name'],
                    "display_name": row['Name'], # Using Name as display name provided
                    "real_name": row['Name'],    # Using Name as real name provided
                    "role": "スタッフ",           # Default role
                    "image_url": image_url,
                    "scope_score": 80,           # Default score as it's not in CSV
                    "introduction": row.get('Comment', ''),
                    "store_id": store_id
                }
                
                staff = Staff(**staff_data)
                db.add(staff)
                db.commit()
                db.refresh(staff)
                
                # Link Tags
                for tag_name in tags_list:
                    tag = get_tag_if_exists(tag_name)
                    if tag:
                        staff_tag = StaffTag(staff_id=staff.id, tag_id=tag.id)
                        db.add(staff_tag)
                    else:
                        print(f"  Skipping unknown tag: {tag_name}")
                
                db.commit()
                
        print("Import completed successfully.")
        
    except Exception as e:
        print(f"Error importing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import staff data from CSV')
    parser.add_argument('file', help='Path to the CSV file')
    args = parser.parse_args()
    
    if os.path.exists(args.file):
        import_staff_from_csv(args.file)
    else:
        print(f"File not found: {args.file}")
