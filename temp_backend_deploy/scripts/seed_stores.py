import os
import sys
import re

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.store import Store

def parse_and_seed():
    files = ["store_data.txt", "store_data_part2.txt", "store_data_part3.txt", "store_data_part4.txt", "store_data_kinki.txt"]
    lines = []
    for filename in files:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(file_path):
            print(f"Reading {filename}...")
            with open(file_path, "r", encoding="utf-8") as f:
                lines.extend([line.strip() for line in f.readlines()])
        else:
            print(f"Warning: {filename} not found.")

    db = SessionLocal()
    
    print("Deleting existing stores...")
    db.query(Store).delete()
    db.commit()

    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ]

    current_prefecture = ""
    current_store = None
    state = "start" # start, address, details, hours, remarks

    stores_to_add = []

    def save_store(store_data):
        if not store_data:
            return
        
        # Extract city
        address = store_data["address"]
        city = "Unknown"
        
        # Remove prefecture from address if present
        cleaned_addr = address
        if store_data["prefecture"] and address.startswith(store_data["prefecture"]):
            cleaned_addr = address[len(store_data["prefecture"]):]
        
        # Match City, Ward, Town, Village
        # Prioritize City > Ward > Town/Village
        # Example: "札幌市中央区" -> "札幌市"
        # "西多摩郡日の出町" -> "西多摩郡" (or "日の出町"?) -> Let's take the first chunk.
        match = re.match(r"^(.+?[市区町村])", cleaned_addr)
        if match:
            city = match.group(1)
        
        # Clean up fields
        name = store_data["name"].replace("Zoff ", "", 1) if store_data["name"].startswith("Zoff ") else store_data["name"]
        # Wait, user list has "Zoff Name". I should probably keep "Zoff" or remove it?
        # The previous scraping kept it. The UI says "Zoff {store.name}".
        # If I keep it, UI will say "Zoff Zoff Name".
        # Let's remove "Zoff " prefix for the name field, so UI "Zoff {name}" works nicely.
        
        new_store = Store(
            name=name,
            prefecture=store_data["prefecture"],
            city=city,
            address=address,
            opening_hours=store_data["opening_hours"].strip(),
            phone_number=store_data["phone_number"],
            remarks=store_data["remarks"].strip()
        )
        stores_to_add.append(new_store)

    for i, line in enumerate(lines):
        if not line:
            continue

        if line in prefectures:
            if current_store:
                save_store(current_store)
                current_store = None
            current_prefecture = line
            continue

        if line.startswith("Zoff"):
            if current_store:
                save_store(current_store)
            
            current_store = {
                "name": line,
                "prefecture": current_prefecture,
                "address": "",
                "opening_hours": "",
                "phone_number": None,
                "remarks": ""
            }
            state = "address"
            continue

        if state == "address":
            current_store["address"] = line
            state = "details"
            continue

        if state == "details" or state == "hours" or state == "remarks":
            if line.startswith("営業時間：") or line.startswith("営業時間:"):
                val = line.split("：")[-1] if "：" in line else line.split(":")[-1]
                current_store["opening_hours"] = val
                state = "hours"
            elif line.startswith("電話番号") or "電話番号" in line:
                # Handle "電話番号：03-..." or "電話番号 03-..."
                # Find where number starts
                # Simple heuristic: split by colon or space
                val = line
                if "：" in line:
                    val = line.split("：")[-1]
                elif ":" in line:
                    val = line.split(":")[-1]
                else:
                    # Maybe "電話番号 03..."
                    parts = line.split()
                    if len(parts) > 1:
                        val = parts[-1]
                
                current_store["phone_number"] = val.strip()
                state = "remarks"
            elif state == "hours":
                current_store["opening_hours"] += "\n" + line
            elif state == "remarks":
                 current_store["remarks"] += "\n" + line
            elif state == "details":
                 # If we encounter text before "営業時間", it might be part of hours or remarks?
                 # But usually it's empty lines (handled) or maybe "【...】"
                 # Let's assume it's part of opening hours if it looks like it, or remarks.
                 # For now, append to opening_hours as a fallback
                 current_store["opening_hours"] += "\n" + line

    if current_store:
        save_store(current_store)

    print(f"Seeding {len(stores_to_add)} stores...")
    db.add_all(stores_to_add)
    db.commit()
    db.close()
    print("Done.")

if __name__ == "__main__":
    # Ensure tables exist (schema update)
    Base.metadata.create_all(bind=engine)
    parse_and_seed()
