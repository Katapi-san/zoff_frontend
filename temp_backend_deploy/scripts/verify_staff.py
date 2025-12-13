import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff

def verify():
    db = SessionLocal()
    staffs = db.query(Staff).all()
    print(f"Total Staff Count: {len(staffs)}")
    for s in staffs:
        print(f"ID: {s.id}, Name: {s.name}, StoreID: {s.store_id}")
    db.close()

if __name__ == "__main__":
    verify()
