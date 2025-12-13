import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Store

def check_stores():
    db = SessionLocal()
    store_names = ["ミカン下北店", "イオンモール橿原店", "渋谷マークシティ店"]
    for name in store_names:
        store = db.query(Store).filter(Store.name.like(f"%{name}%")).first()
        if store:
            print(f"Found: {name} -> ID: {store.id}, Name: {store.name}")
        else:
            print(f"Not Found: {name}")
    db.close()

if __name__ == "__main__":
    check_stores()
