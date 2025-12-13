import sys
import os

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Store

def list_stores():
    db = SessionLocal()
    stores = db.query(Store).all()
    print(f"Total stores: {len(stores)}")
    for store in stores:
        if "湘南" in store.name:
            print(f"Found: {store.id}: {store.name}")
    db.close()

if __name__ == "__main__":
    list_stores()
