
import sys
import os
import csv
import re
from sqlalchemy import text

# Add parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Store, Tag, StaffTag

def import_full_staff_v3():
    db = SessionLocal()
    
    # Keyword classification for auto-tagging new tags
    # If a tag exists in DB, we use its ID. If not, we assign ID based on these keywords.
    # Also used for sorting staff tags into categories to meet the quota.
    
    KEYWORDS_TECH = ["認定眼鏡士", "加工", "フィッティング", "視力", "調整", "修理", "レンズ", "コンタクト", "知識"]
    KEYWORDS_STYLE = ["丸顔", "面長", "卵顔", "四角", "ベース", "逆三角", "イエベ", "ブルベ", "春", "夏", "秋", "冬", "PD", "目", "髪"] # Also logic from columns
    KEYWORDS_HOBBY = ["ゲーム", "アニメ", "サウナ", "猫", "犬", "旅行", "カフェ", "K-POP", "映画", "読書", "音楽", "キャンプ", "ショッピング", "筋トレ", "美容", "ディズニー", "写真", "料理", "スニーカー", "古着", "ストリート"]
    KEYWORDS_SCENE = ["ビジネス", "デート", "おうち", "仕事", "運転", "ユニセックス", "女性", "男性", "初心者", "上級者", "ギフト", "学習", "花粉", "PC", "強度", "ダテ", "サングラス", "トレンド", "フレンチ", "モード", "カジュアル", "キレイめ", "スタイリッシュ", "ヴィンテージ", "クラシック", "ラバテン", "Zoff", "黒縁", "太縁", "べっこう", "メタル", "プラスチック", "コンビネーション", "チタン"]

    TARGET_COUNTS = {
        "tech": 2,
        "style": 2,
        "scene": 3,
        "hobby": 3
    }
    
    # ID Ranges
    RANGE_TECH = (1, 50)
    RANGE_STYLE = (51, 100)
    RANGE_SCENE = (101, 200)
    RANGE_HOBBY = (201, 999)

    # Popular tags for fallback filling
    DEFAULTS = {
        "tech": ["#加工技術", "#視力測定", "#フィッティング", "#調整技術", "#レンズ知識", "#修理マイスター", "#コンタクト併用相談", "#強度近視相談"],
        "style": ["#丸顔", "#面長", "#イエベ", "#ブルベ", "#似合わせ", "#トレンド", "#フレンチ", "#クラシック", "#モード"],
        "scene": ["#ビジネス", "#ドライブ", "#デート", "#おうち時間", "#ユニセックスにおすすめ", "#女性におすすめ", "#男性におすすめ", "#初心者におすすめ", "#お仕事にも使える"],
        "hobby": ["#ゲーム", "#アニメ", "#サウナ", "#旅行", "#カフェ巡り", "#映画鑑賞", "#読書", "#K-POP", "#キャンプ", "#写真"]
    }

    def get_category_id_range(tag_name):
        for k in KEYWORDS_TECH:
            if k in tag_name: return RANGE_TECH
        for k in KEYWORDS_STYLE:
            if k in tag_name: return RANGE_STYLE
        for k in KEYWORDS_HOBBY:
            if k in tag_name: return RANGE_HOBBY
        # Default to Scene for unclassified but likely attribute-related
        return RANGE_SCENE

    def get_category_name(tag_id):
        if RANGE_TECH[0] <= tag_id <= RANGE_TECH[1]: return "tech"
        if RANGE_STYLE[0] <= tag_id <= RANGE_STYLE[1]: return "style"
        if RANGE_SCENE[0] <= tag_id <= RANGE_SCENE[1]: return "scene"
        if RANGE_HOBBY[0] <= tag_id: return "hobby"
        return "scene" # fallback

    try:
        print("Loading CSV...")
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zoff_staff_v5_enriched.csv")
        
        # 1. Aggregate Staff Data
        staff_data = {} # name -> {info..., tags: set()}
        
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Name'].strip()
                if not name: continue
                
                # Normalize name if needed? Assuming 'Name' is unique identifier for person
                
                if name not in staff_data:
                    staff_data[name] = {
                        "name": name,
                        "shop": row['Shop'],
                        "image": row['Image_Filename'],
                        "comment": row['Comment'],
                        "tags": set()
                    }
                
                # Collect Tags from various columns
                # Face Type & Personal Color -> Style Tags
                if row.get('Face_Type'): staff_data[name]["tags"].add(f"#{row['Face_Type']}")
                if row.get('Personal_Color'): staff_data[name]["tags"].add(f"#{row['Personal_Color']}")
                # Eye/Hair -> maybe style?
                if row.get('Eye_Position'): staff_data[name]["tags"].add(f"#{row['Eye_Position']}")
                if row.get('Hair_Style'): staff_data[name]["tags"].add(f"#{row['Hair_Style']}")

                # Tags Column
                if row.get('Tags'):
                    # Handle comma separated, remove quotes if any
                    raw_tags = row['Tags'].replace("、", ",").split(",")
                    for t in raw_tags:
                        t = t.strip().replace('"', '').replace("'", "")
                        if t:
                            if not t.startswith("#"): t = "#" + t
                            staff_data[name]["tags"].add(t)

        print(f"Found {len(staff_data)} unique staff profiles.")

        # 2. Prepare DB
        # Only clear mapping, or maybe clear Staff too? User asked to "register remaining members". 
        # Safest is to sync. Let's delete all staff and recreate to ensure clean slate, 
        # or update existing. Given the duplication issue, clearing is cleaner.
        # But we must preserve Store data if possible, or link to it.
        
        print("Clearing Staff and StaffTag tables...")
        db.query(StaffTag).delete()
        db.query(Staff).delete()
        db.commit()

        # Pre-load Tags to dict
        all_tags = db.query(Tag).all()
        tag_map = {t.name: t for t in all_tags}
        
        # Helper to get/create tag
        def ensure_tag(name):
            if name in tag_map:
                return tag_map[name]
            
            # Create new
            id_range = get_category_id_range(name)
            
            # Find free ID
            existing_ids = {t.id for t in tag_map.values() if id_range[0] <= t.id <= id_range[1]}
            free_id = -1
            for i in range(id_range[0], id_range[1] + 1):
                if i not in existing_ids:
                    free_id = i
                    break
            
            if free_id == -1:
                # No space in range, let auto-inc handle it (overflow to > last max, effectively Hobby/Other or error)
                # But we should try to fit loosely. If Hobby is 201+, just use any large ID.
                # If Tech/Style full, overflow to Scene?
                print(f"Warning: No ID space for {name} in {id_range}. Allowing DB to assign.")
                new_tag = Tag(name=name, type="GENERAL")
            else:
                new_tag = Tag(id=free_id, name=name, type="GENERAL")
            
            try:
                db.add(new_tag)
                db.flush() # Use flush to get ID, commit later
                db.refresh(new_tag)
                tag_map[name] = new_tag
                return new_tag
            except Exception as e:
                # db.rollback() # Don't rollback whole session
                print(f"Failed to create tag {name}: {e}")
                return None

        # Pre-load Stores
        store_map = {s.name: s.id for s in db.query(Store).all()} # Exact match
        
        # Fuzzy match helper
        def find_store_id(shop_name):
            if not shop_name: return None
            # Normalize
            shop_name = shop_name.replace("Zoff", "").strip()
            # Try exact
            for db_name, sid in store_map.items():
                if shop_name in db_name:
                    return sid
            return None

        # 3. Insert Data
        count = 0
        for name, info in staff_data.items():
            store_id = find_store_id(info['shop'])
            
            # Handle special overrides if needed (e.g. Tonton's store)
            if name == "とんとん" and not store_id:
                 # fallback to Ofuna if not found
                 pass # will be handled or null
            
            new_staff = Staff(
                name=name,
                display_name=name,
                store_id=store_id,
                image_url=f"/images/staff/{info['image']}" if info['image'] else None,
                introduction=info['comment'],
                role="スタッフ"
            )
            db.add(new_staff)
            db.flush() # Get ID
            db.refresh(new_staff)
            
            # Process Tags
            # Collect all Tag objects first
            staff_tag_objs = []
            for t_name in info['tags']:
                t_obj = ensure_tag(t_name)
                if t_obj:
                    staff_tag_objs.append(t_obj)
            
            # Categorize
            categorized = {"tech": [], "style": [], "scene": [], "hobby": []}
            for t_obj in staff_tag_objs:
                cat = get_category_name(t_obj.id)
                categorized[cat].append(t_obj)
            
            # Select Quota and FILL if missing
            final_tags = []
            for cat, limit in TARGET_COUNTS.items():
                # Get existing ones
                current_list = categorized[cat]
                
                # Fill if short
                if len(current_list) < limit:
                    shortage = limit - len(current_list)
                    # Pick from defaults
                    defaults = DEFAULTS[cat]
                    import random
                    # Shuffle defaults and pick ones not already in current_list (by name/id)
                    existing_names = {t.name for t in current_list}
                    candidates = [d for d in defaults if d not in existing_names]
                    
                    # Need to tag objects for candidates
                    filled_count = 0
                    for c_name in candidates:
                        if filled_count >= shortage: break
                        t_obj = ensure_tag(c_name)
                        if t_obj:
                            current_list.append(t_obj)
                            filled_count += 1
                
                # Select limit (or less if still short, but defaults should cover)
                selected = current_list[:limit]
                final_tags.extend(selected)
            
            # Add to many-to-many
            added_tag_ids = set()
            for t in final_tags:
                if t.id in added_tag_ids: continue
                st = StaffTag(staff_id=new_staff.id, tag_id=t.id)
                db.add(st)
                added_tag_ids.add(t.id)
            
            count += 1
            if count % 10 == 0:
                print(f"Propagating {count} staff...")

        db.commit()
        print(f"Import Finished. Total Staff: {count}")

        # Post-Import Updates
        tonton = db.query(Staff).filter(Staff.name == "とんとん").first()
        if tonton:
            tonton.introduction = """東京都出身、とんとんです！

普段の生活だけでなく、推し活などの特別な日にもあうメガネを紹介していければとおもいます！

店頭でもお待ちしてます♪"""
            tonton.image_url = "/images/staff/とんとん.jpg"
            ofuna = db.query(Store).filter(Store.name.like("%大船%")).first()
            if ofuna: tonton.store_id = ofuna.id
            
        gucci = db.query(Staff).filter(Staff.name == "ぐっち").first()
        if gucci:
            gucci.store_id = 123
        
        db.commit()

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Critical Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_full_staff_v3()
