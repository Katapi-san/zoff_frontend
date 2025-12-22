
import sys
import os
import traceback
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Store, Tag, StaffTag

def import_page2_staff():
    db = SessionLocal()
    try:
        # Load page 2 data
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "page2_data.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            scraped_data = json.load(f)
        
        print(f"Loaded {len(scraped_data)} staff items from JSON.")

        # Settings for Quota Fill
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

        KEYWORDS_TECH = ["認定眼鏡士", "加工", "フィッティング", "視力", "調整", "修理", "レンズ", "コンタクト", "知識"]
        KEYWORDS_STYLE = ["丸顔", "面長", "卵顔", "四角", "ベース", "逆三角", "イエベ", "ブルベ", "春", "夏", "秋", "冬", "PD", "目", "髪"]
        KEYWORDS_HOBBY = ["ゲーム", "アニメ", "サウナ", "猫", "犬", "旅行", "カフェ", "K-POP", "映画", "読書", "音楽", "キャンプ", "ショッピング", "筋トレ", "美容", "ディズニー", "写真", "料理", "スニーカー", "古着", "ストリート"]

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

        # Pre-load existing Tags and Staff
        tag_map = {t.name: t for t in db.query(Tag).all()}
        existing_staff = {s.name for s in db.query(Staff).all()}
        store_map = {s.name: s.id for s in db.query(Store).all()}

        def find_store_id(shop_name):
            if not shop_name: return None
            shop_name_clean = shop_name.replace("Zoff", "").strip()
            # Try fuzzy
            for db_name, sid in store_map.items():
                if shop_name_clean in db_name: return sid
            return None

        def ensure_tag(name):
            if name in tag_map: return tag_map[name]
            id_range = get_category_id_range(name)
            # Find free ID
            existing_ids = {t.id for t in tag_map.values() if t.id is not None and id_range[0] <= t.id <= id_range[1]}
            free_id = -1
            for i in range(id_range[0], id_range[1] + 1):
                if i not in existing_ids:
                    free_id = i
                    break
            
            # Simple fallback if full
            if free_id == -1: free_id = None # Let auto-increment handle overflow or error? 
            # Actually use a generic overflow range if needed, but let's assume space
            
            new_tag = Tag(id=free_id, name=name, type="GENERAL")
            try:
                db.add(new_tag)
                db.flush()
                tag_map[name] = new_tag
                return new_tag
            except:
                db.rollback()
                return None

        # Process each scraped item
        count_added = 0
        for item in scraped_data:
            # Parse text
            raw = item['all_text'].split('\n')
            lines = [l.strip() for l in raw if l.strip()]
            
            # Heuristic: 
            # Line 0: Name
            # Last Line: Shop
            # Middle lines: Tags (Face type, etc.)
            
            if not lines: continue
            
            name = lines[0]
            shop_name = lines[-1]
            
            if name in existing_staff:
                # Skip duplicate names to avoid confusion unless we want to update?
                # User said "Add 30 staff". If they exist, maybe we shouldn't duplicate.
                # But check if it's the SAME person (same shop).
                # For now, skip to avoid "IntegrityError" on unique constraints if any (Name isn't unique but logic assumes distinct).
                print(f"Skipping existing staff: {name}")
                continue
                
            store_id = find_store_id(shop_name)
            
            # Create Staff
            new_staff = Staff(
                name=name,
                display_name=name,
                store_id=store_id,
                image_url=item['img_src'],
                introduction=f"こんにちは、{name}です！\n{shop_name}で働いています。", # Generic intro
                role="スタッフ"
            )
            db.add(new_staff)
            db.flush()
            
            # Process Tags from middle lines
            # Example: "卵顔ブルベ", "普通", "寄り目"
            # Split these into potential tags
            # "卵顔ブルベ" -> "卵顔", "ブルベ" (Need to split manually or just treat as one?)
            # Usually "卵顔" and "ブルベ" are separate concepts but written together.
            # I'll create tags for whatever text is there.
            
            initial_tags = []
            for l in lines[1:-1]:
                # Split commonly combined words?
                # For now just take the line as a tag if it looks like one
                t_name = f"#{l}"
                t_obj = ensure_tag(t_name)
                if t_obj: initial_tags.append(t_obj)
            
            # Fill Quotas
            # Group current tags
            categorized = {"tech": [], "style": [], "scene": [], "hobby": []}
            for t_obj in initial_tags:
                cat = get_category_name(t_obj.id)
                categorized[cat].append(t_obj)
            
            final_tags = []
            import random
            for cat, limit in TARGET_COUNTS.items():
                current = categorized[cat]
                if len(current) < limit:
                     defaults = DEFAULTS[cat]
                     random.shuffle(defaults)
                     for d in defaults:
                         if len(current) >= limit: break
                         d_obj = ensure_tag(d)
                         if d_obj and d_obj.id not in [x.id for x in current]:
                             current.append(d_obj)
                final_tags.extend(current[:limit])
            
            # Relation
            added_ids = set()
            for t in final_tags:
                if t.id in added_ids: continue
                st = StaffTag(staff_id=new_staff.id, tag_id=t.id)
                db.add(st)
                added_ids.add(t.id)
            
            count_added += 1
            print(f"Added {name} ({shop_name})")

        db.commit()
        print(f"Import page 2 finished. Added {count_added} new staff.")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_page2_staff()
