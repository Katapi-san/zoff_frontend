
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models.store import Staff

def update_tonton_data():
    db = SessionLocal()
    try:
        tonton_list = db.query(Staff).filter(Staff.name == "とんとん").all()
        
        new_intro = """東京都出身、とんとんです！

普段の生活だけでなく、推し活などの特別な日にもあうメガネを紹介していければとおもいます！

店頭でもお待ちしてます♪"""

        new_image_url = "/images/staff/とんとん.jpg"

        if not tonton_list:
            print("Tonton not found!")
            return

        for tonton in tonton_list:
            print(f"Updating Tonton (ID: {tonton.id})...")
            tonton.introduction = new_intro
            tonton.image_url = new_image_url
            
        db.commit()
        print("Done")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_tonton_data()
