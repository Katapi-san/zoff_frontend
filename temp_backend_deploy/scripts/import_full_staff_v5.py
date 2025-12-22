
import sys
import os
import csv
import traceback
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models.store import Staff, Store, Tag, StaffTag

def import_full_staff_v5():
    db = SessionLocal()
    try:
        # Settings
        KEYWORDS_TECH = ["認定眼鏡士", "加工", "フィッティング", "視力", "調整", "修理", "レンズ", "コンタクト", "知識"]
        KEYWORDS_STYLE = ["丸顔", "面長", "卵顔", "四角", "ベース", "逆三角", "イエベ", "ブルベ", "春", "夏", "秋", "冬", "PD", "目", "髪"]
        KEYWORDS_HOBBY = ["ゲーム", "アニメ", "サウナ", "猫", "犬", "旅行", "カフェ", "K-POP", "映画", "読書", "音楽", "キャンプ", "ショッピング", "筋トレ", "美容", "ディズニー", "写真", "料理", "スニーカー", "古着", "ストリート"]
        
        TARGET_COUNTS = {"tech": 2, "style": 2, "scene": 3, "hobby": 3}
        DEFAULTS = {
            "tech": ["#加工技術", "#視力測定", "#フィッティング", "#調整技術", "#レンズ知識", "#修理マイスター", "#コンタクト併用相談", "#強度近視相談"],
            "style": ["#丸顔", "#面長", "#イエベ", "#ブルベ", "#似合わせ", "#トレンド", "#フレンチ", "#クラシック", "#モード"],
            "scene": ["#ビジネス", "#ドライブ", "#デート", "#おうち時間", "#ユニセックスにおすすめ", "#女性におすすめ", "#男性におすすめ", "#初心者におすすめ", "#お仕事にも使える"],
            "hobby": ["#ゲーム", "#アニメ", "#サウナ", "#旅行", "#カフェ巡り", "#映画鑑賞", "#読書", "#K-POP", "#キャンプ", "#写真"]
        }
        
        RANGE_TECH = (1, 50)
        RANGE_STYLE = (51, 100)
        RANGE_SCENE = (101, 200)
        RANGE_HOBBY = (201, 999)

        def get_category_id_range(tag_name):
            for k in KEYWORDS_TECH:
                if k in tag_name: return RANGE_TECH
            for k in KEYWORDS_STYLE:
                if k in tag_name: return RANGE_STYLE
            for k in KEYWORDS_HOBBY:
                if k in tag_name: return RANGE_HOBBY
            return RANGE_SCENE

        def get_category_name(tag_id):
            if RANGE_TECH[0] <= tag_id <= RANGE_TECH[1]: return "tech"
            if RANGE_STYLE[0] <= tag_id <= RANGE_STYLE[1]: return "style"
            if RANGE_SCENE[0] <= tag_id <= RANGE_SCENE[1]: return "scene"
            if RANGE_HOBBY[0] <= tag_id: return "hobby"
            return "scene"

        # 1. Load CSV and Aggregate
        print("Loading CSV...")
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zoff_staff_v5_enriched.csv")
        
        staff_data = {}
        all_csv_tags = set()
        
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Name'].strip()
                if not name: continue
                if name not in staff_data:
                    staff_data[name] = {
                        "name": name, "shop": row['Shop'], "image": row['Image_Filename'],
                        "comment": row['Comment'], "tags": set()
                    }
                
                # Collect tags logic
                row_tags = set()
                if row.get('Face_Type'): row_tags.add(f"#{row['Face_Type']}")
                if row.get('Personal_Color'): row_tags.add(f"#{row['Personal_Color']}")
                if row.get('Eye_Position'): row_tags.add(f"#{row['Eye_Position']}")
                if row.get('Hair_Style'): row_tags.add(f"#{row['Hair_Style']}")
                if row.get('Tags'):
                    for t in row['Tags'].replace("、", ",").split(","):
                        t = t.strip().replace('"', '').replace("'", "")
                        if t:
                            if not t.startswith("#"): t = "#" + t
                            row_tags.add(t)
                
                staff_data[name]["tags"].update(row_tags)
                all_csv_tags.update(row_tags)

        print(f"Aggregated {len(staff_data)} unique staff.")
        
        # 2. Prepare Tags (Pre-create all missing tags)
        print("Preparing Tags...")
        
        # Add default tags to set to ensure they exist
        for d_list in DEFAULTS.values():
            all_csv_tags.update(d_list)

        # Clear existing mappings only? No, we clear everything to be clean
        # But we want to reuse existing tags if possible to keep IDs stable?
        # Actually, previous script failed so maybe DB is dirty. Let's reuse.
        
        tag_map = {t.name: t for t in db.query(Tag).all()}
        
        # Create missing mappings
        tags_to_create = []
        # Sort to keep ID assignment deterministic
        for t_name in sorted(list(all_csv_tags)):
            if t_name not in tag_map:
                tags_to_create.append(t_name)
        
        for t_name in tags_to_create:
            id_range = get_category_id_range(t_name)
            # Find free ID
            existing_ids = {t.id for t in tag_map.values() if id_range[0] <= t.id <= id_range[1]}
            free_id = -1
            for i in range(id_range[0], id_range[1] + 1):
                if i not in existing_ids:
                    free_id = i
                    break
            
            if free_id != -1:
                new_tag = Tag(id=free_id, name=t_name, type="GENERAL")
            else:
                new_tag = Tag(name=t_name, type="GENERAL")
            
            db.add(new_tag)
            # We must flush to occupy the ID for next iteration in this loop
            db.flush() 
            tag_map[t_name] = new_tag
        
        db.commit() # Commit all tags first
        print("Tags prepared.")

        # 3. Clear Staff Data
        print("Clearing old staff data...")
        db.query(StaffTag).delete()
        db.query(Staff).delete()
        db.commit()

        # 4. Insert Staff
        print("Inserting Staff...")
        store_map = {s.name: s.id for s in db.query(Store).all()}
        def find_store_id(shop_name):
            if not shop_name: return None
            shop_name = shop_name.replace("Zoff", "").strip()
            for db_name, sid in store_map.items():
                if shop_name in db_name: return sid
            return None

        count = 0
        for name, info in staff_data.items():
            store_id = find_store_id(info['shop'])
            
            new_staff = Staff(
                name=name, display_name=name, store_id=store_id,
                image_url=f"/images/staff/{info['image']}" if info['image'] else None,
                introduction=info['comment'], role="スタッフ"
            )
            db.add(new_staff)
            db.flush()

            # Assign Tags
            staff_tag_objs = [tag_map[t] for t in info['tags'] if t in tag_map]
            
            # Categorize
            categorized = {"tech": [], "style": [], "scene": [], "hobby": []}
            for t_obj in staff_tag_objs:
                cat = get_category_name(t_obj.id)
                categorized[cat].append(t_obj)

            # Fill Quotas
            final_tags = []
            for cat, limit in TARGET_COUNTS.items():
                current = categorized[cat] # List of objects
                if len(current) < limit:
                    import random
                    defaults = DEFAULTS[cat]
                    random.shuffle(defaults) 
                    for d_name in defaults:
                        if len(current) >= limit: break
                        d_obj = tag_map[d_name]
                        # Check exist in current
                        if d_obj.id not in [x.id for x in current]:
                            current.append(d_obj)
                final_tags.extend(current[:limit])

            # Add relations
            added_ids = set()
            for t_obj in final_tags:
                if t_obj.id in added_ids: continue
                st = StaffTag(staff_id=new_staff.id, tag_id=t_obj.id)
                db.add(st)
                added_ids.add(t_obj.id)

            count += 1
        
        db.commit()
        print(f"Staff insertion complete. Total: {count}")

        # 5. Fixes
        tonton = db.query(Staff).filter(Staff.name == "とんとん").first()
        if tonton:
            tonton.introduction = "東京都出身、とんとんです！\n\n普段の生活だけでなく、推し活などの特別な日にもあうメガネを紹介していければとおもいます！\n\n店頭でもお待ちしてます♪"
            tonton.image_url = "/images/staff/とんとん.jpg"
            ofuna = db.query(Store).filter(Store.name.like("%大船%")).first()
            if ofuna: tonton.store_id = ofuna.id
            
        gucci = db.query(Staff).filter(Staff.name == "ぐっち").first()
        if gucci: gucci.store_id = 123
        
        db.commit()
        print("Success.")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_full_staff_v5()
