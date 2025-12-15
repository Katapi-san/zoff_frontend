
import sys
import os
import csv

# Add parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Tag, StaffTag

def fix_tags():
    db = SessionLocal()
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zoff_staff_v5_enriched.csv")
        
        # 1. Load Gucci from CSV
        gucci_tags = []
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == 'ぐっち':
                    print("Found 'ぐっち' in CSV.")
                    # Extract logic same as import script
                    if row.get('Face_Type'): gucci_tags.append(row['Face_Type'])
                    if row.get('Personal_Color'): gucci_tags.append(row['Personal_Color'])
                    if row.get('Eye_Position'): gucci_tags.append(row['Eye_Position'])
                    if row.get('Hair_Style'): gucci_tags.append(row['Hair_Style'])
                    
                    for col in ['Tags', 'Tags-skill', 'Tags-Hobby']:
                        if row.get(col):
                            v = row[col].replace('、', ',').replace(' ', ',')
                            gucci_tags.extend(v.split(','))
                    break
        
        # Clean tags
        gucci_tags = [t.strip() for t in gucci_tags if t.strip()]
        gucci_tags = ['#' + t if not t.startswith('#') else t for t in gucci_tags]
        gucci_tags = list(set(gucci_tags))
        print(f"Gucci Tags from CSV: {gucci_tags}")

        # 2. Define standard tags for Tonton (Mock)
        tonton_tags = [
            "#面長", 
            "#ブルベ夏", 
            "#寄り目", 
            "#ロング", 
            "#認定眼鏡士", 
            "#カフェ巡り",
            "#トレンド",
            "#Zoff SMART"
        ]
        print(f"Tonton Tags (Mock): {tonton_tags}")

        # 3. Update DB
        all_tags_db = {t.name: t for t in db.query(Tag).all()}

        def update_staff_tags(staff_name, new_tags_list):
            staff_list = db.query(Staff).filter(Staff.name == staff_name).all()
            if not staff_list:
                print(f"{staff_name} not found in DB.")
                return

            for staff in staff_list:
                print(f"Updating tags for {staff.name} (ID: {staff.id})...")
                # Clear existing
                db.query(StaffTag).filter(StaffTag.staff_id == staff.id).delete()
                
                # Add new
                for tag_name in new_tags_list:
                    tag = all_tags_db.get(tag_name)
                    if not tag:
                        # Create if missing? Better to use existing, but let's see.
                        # Assuming these standard tags exist. If not, we skip or create.
                        # Detailed tags might allow creation.
                        print(f"  Creating new tag: {tag_name}")
                        tag = Tag(name=tag_name, type="GENERAL") # Default type
                        db.add(tag)
                        db.commit()
                        db.refresh(tag)
                        all_tags_db[tag_name] = tag
                    
                    st = StaffTag(staff_id=staff.id, tag_id=tag.id)
                    db.add(st)
                db.commit()

        if gucci_tags:
            update_staff_tags("ぐっち", gucci_tags)
        else:
            print("Gucci not found in CSV? Skipping update based on CSV.")

        update_staff_tags("とんとん", tonton_tags)
        
        print("Tag update completed.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_tags()
