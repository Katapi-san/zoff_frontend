
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models.store import Staff

def update_tonton_image():
    db = SessionLocal()
    try:
        tonton = db.query(Staff).filter(Staff.name == "とんとん").first()
        if tonton:
            print("Updating Tonton image URL...")
            # Guessing standard Zoff ID based image path from the provided ID 125009
            tonton.image_url = "https://www.zoff.co.jp/client_info/ZOFF/view/user/systemimages/staff/125009_1.jpg"
            # Optional: Add some standard tags if missing, but let's leave tags blank for now
            db.commit()
            print("Done")
        else:
            print("Tonton not found")
    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    update_tonton_image()
