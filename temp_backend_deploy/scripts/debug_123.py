
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models.store import Staff, Store

def check_123_and_gucci():
    db = SessionLocal()
    try:
        print("--- Checking 'ぐっち' ---")
        gucci = db.query(Staff).filter(Staff.name == "ぐっち").all()
        if not gucci:
            print("Gucci not found by exact name match.")
            # Try like
            gucci_fuzzy = db.query(Staff).filter(Staff.name.like("%ぐっち%")).all()
            print(f"Fuzzy match count: {len(gucci_fuzzy)}")
            for g in gucci_fuzzy:
                print(f"Found: {g.name} (ID: {g.id}), Store ID: {g.store_id}")
        else:
            for g in gucci:
                print(f"Found: {g.name} (ID: {g.id}), Store ID: {g.store_id}")
                
        print("\n--- Checking Store 123 Staff ---")
        store = db.query(Store).filter(Store.id == 123).first()
        if store:
            print(f"Store 123: {store.name}")
            staffs = db.query(Staff).filter(Staff.store_id == 123).all()
            print(f"Staff count in 123: {len(staffs)}")
            for s in staffs:
                print(f"- {s.name} (ID: {s.id})")
        else:
            print("Store 123 not found in DB.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_123_and_gucci()
