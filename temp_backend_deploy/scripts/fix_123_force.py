
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models.store import Staff, Store
from sqlalchemy import text

def fix_data_force():
    db = SessionLocal()
    try:
        # Force Store 123
        target_store_id = 123
        
        # Check target store
        s123 = db.query(Store).filter(Store.id == target_store_id).first()
        if not s123:
            print("Creating Store 123 (LaQua)...")
            s123 = Store(id=target_store_id, name="Zoff 東京ドームシティ・ラクーア店", prefecture="東京都", city="文京区")
            db.add(s123)
            db.commit()
            db.refresh(s123)
        else:
            print(f"Store 123 exists: {s123.name}")

        # Fix Gucci
        gucci_list = db.query(Staff).filter(Staff.name == "ぐっち").all()
        if not gucci_list:
            print("Gucci not found! Creating...")
            gucci = Staff(name="ぐっち", display_name="ぐっち", store_id=target_store_id, role="スタッフ")
            db.add(gucci)
        else:
            for g in gucci_list:
                print(f"Updating Gucci (ID: {g.id}) to Store 123")
                g.store_id = target_store_id
        
        # Fix Tonton
        tonton_list = db.query(Staff).filter(Staff.name == "とんとん").all()
        if not tonton_list:
            print("Tonton not found! Creating...")
            # Using data from user request (implied context)
            tonton = Staff(
                name="とんとん", 
                display_name="とんとん", 
                store_id=target_store_id, 
                role="スタッフ"
            )
            # URL text implies Tonton has some content, but for now just create/link
            db.add(tonton)
        else:
            for t in tonton_list:
                print(f"Updating Tonton (ID: {t.id}) to Store 123")
                t.store_id = target_store_id
        
        # Explicitly update using textual SQL to bypass any ORM weirdness if type mismatch exists
        db.commit()
        
        # Verify 
        check = db.query(Staff).filter(Staff.store_id == target_store_id).count()
        print(f"Verified Staff Count in 123: {check}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_data_force()
