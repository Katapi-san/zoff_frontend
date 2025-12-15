import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Store, Staff

def fix_data():
    db = SessionLocal()
    try:
        # --- Task 1: Merge Store 294 into 123 ---
        target_store_id = 123
        source_store_id = 294
        
        target_store = db.query(Store).filter(Store.id == target_store_id).first()
        source_store = db.query(Store).filter(Store.id == source_store_id).first()
        
        if not target_store:
            print(f"Target Store {target_store_id} not found!")
            return
            
        print(f"Target Store: {target_store.name} (ID: {target_store.id})")
        
        # Move specific staff 'ぐっち' and 'とんとん' to 123 (Ensure they are in 123)
        for name in ["ぐっち", "とんとん"]:
            staff_list = db.query(Staff).filter(Staff.name == name).all()
            for s in staff_list:
                print(f"Moving {s.name} (Current Store: {s.store_id}) to Store {target_store_id}")
                s.store_id = target_store_id
        
        # Move ALL staff from 294 to 123
        staff_in_source = db.query(Staff).filter(Staff.store_id == source_store_id).all()
        for s in staff_in_source:
            print(f"Moving {s.name} from Store {source_store_id} to Store {target_store_id}")
            s.store_id = target_store_id
            
        # Delete Store 294
        if source_store:
            print(f"Deleting Store {source_store.name} (ID: {source_store.id})")
            db.delete(source_store)
        else:
            print(f"Source Store {source_store_id} already deleted or not found.")

        # --- Task 2: Move 'つなかん' to 'Zoff 大船ルミネウイング店' ---
        staff_name_Task2 = "つなかん"
        target_store_name_Task2 = "大船ルミネウイング"

        # Find the store
        # Try finding exact or partial
        store_ofuna = db.query(Store).filter(Store.name.like(f"%{target_store_name_Task2}%")).first()
        
        if store_ofuna:
            print(f"Found Target Store for Task 2: {store_ofuna.name} (ID: {store_ofuna.id})")
            
            staff_tsuna = db.query(Staff).filter(Staff.name == staff_name_Task2).all()
            if not staff_tsuna:
                print(f"Staff {staff_name_Task2} not found!")
            else:
                for s in staff_tsuna:
                    print(f"Moving {s.name} (Current Store: {s.store_id}) to {store_ofuna.name} (ID: {store_ofuna.id})")
                    s.store_id = store_ofuna.id
        else:
            print(f"Store matching '{target_store_name_Task2}' not found!")

        db.commit()
        print("Data fix completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_data()
