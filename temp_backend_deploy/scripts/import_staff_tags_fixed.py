
import sys
import os
import csv
import argparse

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.store import Staff, Tag, StaffTag, Store, Base
from sqlalchemy import text

# Tag Definition from Enrichment Script
TAG_MASTER = {
    "technical": {
        "range_start": 1,
        "range_end": 50,
        "tags": [
            "#認定眼鏡士", "#フィッティング", "#加工技術", "#視力測定", "#レンズ知識", 
            "#修理マイスター", "#調整技術", "#遠近両用", "#カラーレンズ知識", "#フレーム選定",
            "#コンタクト併用相談", "#お子様メガネ", "#強度近視相談"
        ]
    },
    "style": {
        "range_start": 51,
        "range_end": 100,
        "tags": [
            "#トレンド", "#クラシック", "#モード", "#フェミニン", "#ビジネス", 
            "#カジュアル", "#ストリート", "#ミニマル", "#ヴィンテージ", "#シンプル", 
            "#個性派", "#韓国ファッション", "#アメリカン", "#フレンチ", "#レトロ",
            "#イエベ春", "#イエベ秋", "#ブルベ夏", "#ブルベ冬",
            "#丸顔", "#面長", "#三角顔", "#四角顔"
        ]
    },
    "scene": {
        "range_start": 101,
        "range_end": 200,
        "tags": [
            "#お仕事用", "#PC作業", "#ドライブ", "#アウトドア", "#スポーツ", 
            "#デート", "#読書", "#おうち時間", "#旅行", "#ギフト", 
            "#サングラス", "#花粉対策", "#リモートワーク", "#運転", "#学習用"
        ]
    },
    "hobby": {
        "range_start": 201,
        "range_end": 300,
        "tags": [
            "#カフェ巡り", "#サウナ", "#映画鑑賞", "#音楽鑑賞", "#K-POP", 
            "#キャンプ", "#写真", "#古着", "#アニメ", "#ゲーム", 
            "#料理", "#旅行", "#読書", "#アート", "#筋トレ", 
            "#スニーカー", "#ディズニー", "#ショッピング", "#美容", "#犬好き", "#猫好き"
        ]
    }
}

def import_staff_with_fixed_tags(csv_file_path):
    print(f"Importing from {csv_file_path}...")
    db = SessionLocal()
    
    # 1. Clear Data
    print("Clearing existing staff/tag data...")
    db.query(StaffTag).delete()
    db.query(Staff).delete()
    db.query(Tag).delete()
    db.commit()
    
    # Reset Auto Increment? (SQLite specific)
    try:
        db.execute(text("DELETE FROM sqlite_sequence WHERE name='tags'"))
        db.execute(text("DELETE FROM sqlite_sequence WHERE name='staff'"))
        db.commit()
    except:
        pass

    # 2. Seed Master Tags
    print("Seeding master tags with specific IDs...")
    tag_name_to_id = {}
    used_ids = set()

    # Pre-register known tags
    for cat, data in TAG_MASTER.items():
        current_id = data["range_start"]
        max_id = data["range_end"]
        
        for name in data["tags"]:
            # Find next available ID
            while current_id in used_ids:
                current_id += 1
            
            if current_id > max_id:
                print(f"Warning: ID range overflow for {cat}. Using {current_id}")
            
            # Determine TYPE
            tag_type = "EXPERT" if cat == "technical" else "OFFICIAL" if cat == "style" else "CASUAL"
            
            tag = Tag(id=current_id, name=name, type=tag_type, certification_source="SYSTEM")
            db.add(tag)
            used_ids.add(current_id)
            tag_name_to_id[name] = current_id
            
            current_id += 1
    
    db.commit()

    # Helper to get or create tag (for unknown tags)
    # Unknown tags default to "Style" category (51-100) or overflow
    style_cursor = TAG_MASTER["style"]["range_start"]
    style_max = TAG_MASTER["style"]["range_end"]

    def get_or_create_tag_id(name):
        nonlocal style_cursor
        if name in tag_name_to_id:
            return tag_name_to_id[name]
        
        # New tag logic
        # Find a slot in Style range
        while style_cursor in used_ids:
            style_cursor += 1
        
        # If simple style range full, try Scene, then Hobby... or just increment
        new_id = style_cursor
        
        tag = Tag(id=new_id, name=name, type="CASUAL", certification_source="CSV")
        db.add(tag)
        db.commit()
        
        used_ids.add(new_id)
        tag_name_to_id[name] = new_id
        return new_id

    # 3. Import Staff
    # Helper to resolve store ID (borrowed from import_staff_csv.py)
    existing_store_map = {} # cache
    
    def get_store_id(name_part):
        if not name_part:
            return db.query(Store).first().id
        
        # Manual fix same as before
        manual_map = {
            "サクラマチクマモト店": "サクラマチ クマモト店"
        }
        if name_part in manual_map:
            name_part = manual_map[name_part]
        elif "サクラマチ" in name_part:
            name_part = "サクラマチ クマモト店"
        elif "大船" in name_part and "ルミネ" in name_part:
            # Fuzzy match for Ofuna variations
            store = db.query(Store).filter(Store.name.like("%大船%"), Store.name.like("%ルミネ%")).first()
            if store: return store.id

        if name_part in existing_store_map:
            return existing_store_map[name_part]

        store = db.query(Store).filter(Store.name.like(f"%{name_part}%")).first()
        if not store:
            # Special case for 本社
            if name_part == "本社":
                 # Check/Create HQ
                 hq = db.query(Store).filter(Store.name == "本社").first()
                 if not hq:
                     hq = Store(name="本社", prefecture="東京都", city="港区", opening_hours="9-18")
                     db.add(hq)
                     db.commit()
                 store = hq
            else:
                 # Fallback
                 store = db.query(Store).first()
        
        if store:
            existing_store_map[name_part] = store.id
            return store.id
        return 1

    print("Reading CSV and creating staff...")
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get('Name'): continue
            
            store_id = get_store_id(row.get('Shop', '').strip())
            
            staff = Staff(
                name=row['Name'],
                display_name=row['Name'],
                real_name=row['Name'],
                role="スタッフ",
                image_url=f"/images/staff/{row.get('Image_Filename', '')}" if row.get('Image_Filename') else "",
                scope_score=80,
                introduction=row.get('Comment', ''),
                store_id=store_id
            )
            db.add(staff)
            db.commit()
            db.refresh(staff)
            
            # Tags
            raw_tags = row.get('Tags', '')
            tag_list = [t.strip() for t in raw_tags.split(',') if t.strip()]
            
            for t_name in tag_list:
                if not t_name.startswith("#"): t_name = "#" + t_name
                tid = get_or_create_tag_id(t_name)
                
                # Check duplication
                # (Ideally use unique constraint on DB, but simple check here)
                exists = db.query(StaffTag).filter_by(staff_id=staff.id, tag_id=tid).first()
                if not exists:
                    st = StaffTag(staff_id=staff.id, tag_id=tid)
                    db.add(st)
            
            db.commit()
            
    print("Import completed.")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = "zoff_staff_v5_enriched.csv"
    
    if os.path.exists(f):
        import_staff_with_fixed_tags(f)
    else:
        print(f"File {f} not found.")
