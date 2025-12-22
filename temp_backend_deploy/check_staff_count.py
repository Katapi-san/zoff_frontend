
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.store import Staff

def count_staff():
    db = SessionLocal()
    count = db.query(Staff).count()
    print(f"Total Staff: {count}")
    
    # Check for Yuha
    yuha = db.query(Staff).filter(Staff.name == "ユーハ").first()
    if yuha:
        print(f"Found ユーハ at {yuha.store_id}")
    else:
        print("ユーハ not found")
    
    db.close()

if __name__ == "__main__":
    count_staff()
