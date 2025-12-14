
import sys
import os

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Store



def list_stores():
    db = SessionLocal()


    target_names = ["本社", "サクラマチ", "熊本", "クマモト"]
    
    with open("debug_stores_utf8.txt", "w", encoding="utf-8") as f:
        f.write("Checking specific stores:\n")
        for name in target_names:
            store = db.query(Store).filter(Store.name.like(f"%{name}%")).first()
            if store:
                f.write(f"Found '{name}': ID={store.id}, Name='{store.name}'\n")
            else:
                f.write(f"NOT FOUND: '{name}'\n")
                
        f.write("\n--- Listing first 20 stores ---\n")
        stores = db.query(Store).limit(20).all()
        for s in stores:
            f.write(f"{s.id}: [{s.name}]\n")

    db.close()

if __name__ == "__main__":
    list_stores()


