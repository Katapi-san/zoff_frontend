import sys
import os
import random
from sqlalchemy import text

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Tag, StaffTag

def assign_random_tags():
    db = SessionLocal()
    try:
        print("Fetching all staff and tags...")
        staff_list = db.query(Staff).all()
        all_tags = db.query(Tag).all()

        if not staff_list:
            print("No staff found.")
            return

        # Group tags by category based on ID ranges
        tech_tags = [t for t in all_tags if 1 <= t.id <= 50]
        proposal_tags = [t for t in all_tags if 51 <= t.id <= 100]
        scene_tags = [t for t in all_tags if 101 <= t.id <= 200]
        hobby_tags = [t for t in all_tags if t.id >= 201]

        # Verify we have enough tags
        if len(tech_tags) < 2 or len(proposal_tags) < 2 or len(scene_tags) < 2 or len(hobby_tags) < 2:
            print("Error: Not enough tags in one or more categories to assign 2 per category.")
            print(f"Tech: {len(tech_tags)}, Proposal: {len(proposal_tags)}, Scene: {len(scene_tags)}, Hobby: {len(hobby_tags)}")
            return

        print(f"Found {len(staff_list)} staff members.")
        print("Clearing existing staff tags...")
        db.query(StaffTag).delete()
        db.commit()

        print("Assigning 2 random tags from each of the 4 categories to every staff member...")
        
        staff_tag_objects = []
        for staff in staff_list:
            # Select 2 random tags from each category
            selected_tags = []
            selected_tags.extend(random.sample(tech_tags, 2))
            selected_tags.extend(random.sample(proposal_tags, 2))
            selected_tags.extend(random.sample(scene_tags, 2))
            selected_tags.extend(random.sample(hobby_tags, 2))

            for tag in selected_tags:
                staff_tag_objects.append(StaffTag(staff_id=staff.id, tag_id=tag.id))
        
        # Bulk save for performance
        db.bulk_save_objects(staff_tag_objects)
        db.commit()
        
        print(f"Successfully assigned {len(staff_tag_objects)} tags to {len(staff_list)} staff members.")

    except Exception as e:
        print(f"Error assigning tags: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    assign_random_tags()
