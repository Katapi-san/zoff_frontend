
import sys
import os
from sqlalchemy import text

# Add parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Tag, StaffTag

def apply_curated_tags():
    db = SessionLocal()
    
    # Define Target Tags with desired ID ranges
    # We will try to find loosely matching tags or create specific ones.
    
    # Categories:
    # 1: Tech (1-50)
    # 2: Prop (51-100)
    # 3: Scene (101-200)
    # 4: Hobby (201+)

    targets = {
        "ぐっち": {
            "tech": ["#認定眼鏡士", "#フィッティング"],      # Range 1-50
            "prop": ["#丸顔", "#イエベ秋"],                # Range 51-100
            "scene": ["#ビジネス", "#ドライブ", "#デート"], # Range 101-200
            "hobby": ["#ゲーム", "#アニメ", "#サウナ"]      # Range 201+
        },
        "とんとん": {
            "tech": ["#加工技術", "#視力測定"],            # Range 1-50
            "prop": ["#面長", "#ブルベ冬"],                # Range 51-100
            "scene": ["#推し活", "#ライブ", "#特別な日"],   # Range 101-200
            "hobby": ["#韓国ファッション", "#K-POP", "#美容"] # Range 201+
        }
    }

    try:
        # Helper to ensure tag exists in range
        def ensure_tag(name, min_id, max_id):
            # Check existing
            existing = db.query(Tag).filter(Tag.name == name).first()
            if existing:
                # If matches range, return.
                if min_id <= existing.id <= max_id:
                    return existing
                else:
                    print(f"Warning: Tag {name} exists at ID {existing.id}, outside target range {min_id}-{max_id}. Using it anyway (Frontend might categorize wrongly).")
                    return existing
            
            # Create new with specific ID if possible
            # Find a free ID in range
            # validation
            used_ids = {t[0] for t in db.query(Tag.id).filter(Tag.id >= min_id, Tag.id <= max_id).all()}
            free_id = -1
            for i in range(min_id, max_id + 1):
                if i not in used_ids:
                    free_id = i
                    break
            
            if free_id == -1:
                # Fallback: Just let auto increment handle it (likely > max existing)
                print(f"No free ID in range {min_id}-{max_id} for {name}. Creating standard.")
                new_tag = Tag(name=name, type="GENERAL")
                db.add(new_tag)
                db.commit()
                db.refresh(new_tag)
                return new_tag
            else:
                print(f"Creating Tag {name} at forced ID {free_id}")
                new_tag = Tag(id=free_id, name=name, type="GENERAL")
                db.add(new_tag)
                # Need to use SQL for inserting identity usually? SQLAlchemy might handle if ID passed.
                # But ID column is auto-increment.
                # let's try db.add. If it fails due to identity insert off, we might need adjustments.
                # for SQLite it is fine.
                db.commit()
                db.refresh(new_tag)
                return new_tag

        for name, tasks in targets.items():
            staff = db.query(Staff).filter(Staff.name == name).first()
            if not staff:
                print(f"Staff {name} not found!")
                continue

            print(f"Processing Tags for {staff.name}...")
            
            # Clear existing
            db.query(StaffTag).filter(StaffTag.staff_id == staff.id).delete()
            
            final_tags = []
            
            # Technical
            for t in tasks['tech']: final_tags.append(ensure_tag(t, 1, 50))
            # Proposal
            for t in tasks['prop']: final_tags.append(ensure_tag(t, 51, 100))
            # Scene
            for t in tasks['scene']: final_tags.append(ensure_tag(t, 101, 200))
            # Hobby
            for t in tasks['hobby']: final_tags.append(ensure_tag(t, 201, 999))
            
            for tag in final_tags:
                if tag:
                    st = StaffTag(staff_id=staff.id, tag_id=tag.id)
                    db.add(st)
            
            print(f"Assigned {len(final_tags)} tags to {staff.name}")
            db.commit()

        print("Curated tags applied.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    apply_curated_tags()
