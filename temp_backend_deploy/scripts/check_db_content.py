import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Store, Staff

def check_content():
    db = SessionLocal()
    store_count = db.query(Store).count()
    staff_count = db.query(Staff).count()
    print(f"Stores: {store_count}")
    print(f"Staff: {staff_count}")
    
    if staff_count > 0:
        staff = db.query(Staff).first()
        print(f"Sample Staff: {staff.name}, Store ID: {staff.store_id}")
        
    db.close()

if __name__ == "__main__":
    check_content()
