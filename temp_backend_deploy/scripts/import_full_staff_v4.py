
import sys
import os
import csv
import re
import traceback
from sqlalchemy import text

# Add parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.store import Staff, Store, Tag, StaffTag

def import_full_staff_v4():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "import_log.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        def log_print(msg):
            print(msg)
            log.write(msg + "\n")
            log.flush()

        db = SessionLocal()
        
        # Keywords settings (Same as before)
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

        try:
            log_print("Loading CSV...")
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zoff_staff_v5_enriched.csv")
            
            staff_data = {}
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
                    if row.get('Face_Type'): staff_data[name]["tags"].add(f"#{row['Face_Type']}")
                    if row.get('Personal_Color'): staff_data[name]["tags"].add(f"#{row['Personal_Color']}")
                    if row.get('Eye_Position'): staff_data[name]["tags"].add(f"#{row['Eye_Position']}")
                    if row.get('Hair_Style'): staff_data[name]["tags"].add(f"#{row['Hair_Style']}")
                    if row.get('Tags'):
                        for t in row['Tags'].replace("、", ",").split(","):
                            t = t.strip().replace('"', '').replace("'", "")
                            if t:
                                if not t.startswith("#"): t = "#" + t
                                staff_data[name]["tags"].add(t)

            log_print(f"Found {len(staff_data)} unique staff profiles.")

            log_print("Clearing tables...")
            db.query(StaffTag).delete()
            db.query(Staff).delete()
            db.commit()

            all_tags = db.query(Tag).all()
            tag_map = {t.name: t for t in all_tags}

            def ensure_tag(name):
                if name in tag_map: return tag_map[name]
                id_range = get_category_id_range(name)
                existing_ids = {t.id for t in tag_map.values() if id_range[0] <= t.id <= id_range[1]}
                free_id = -1
                for i in range(id_range[0], id_range[1] + 1):
                    if i not in existing_ids:
                        free_id = i
                        break
                
                if free_id == -1:
                    new_tag = Tag(name=name, type="GENERAL")
                else:
                    new_tag = Tag(id=free_id, name=name, type="GENERAL")
                
                try:
                    db.add(new_tag)
                    db.flush()
                    db.refresh(new_tag)
                    tag_map[name] = new_tag
                    return new_tag
                except Exception as e:
                    log_print(f"Tag creation failed: {e}")
                    return None

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
                new_staff = Staff(name=name, display_name=name, store_id=store_id,
                                  image_url=f"/images/staff/{info['image']}" if info['image'] else None,
                                  introduction=info['comment'], role="スタッフ")
                db.add(new_staff)
                db.flush()
                db.refresh(new_staff)

                staff_tag_objs = []
                for t_name in info['tags']:
                    t_obj = ensure_tag(t_name)
                    if t_obj: staff_tag_objs.append(t_obj)

                categorized = {"tech": [], "style": [], "scene": [], "hobby": []}
                for t_obj in staff_tag_objs:
                    cat = get_category_name(t_obj.id)
                    categorized[cat].append(t_obj)

                final_tags = []
                for cat, limit in TARGET_COUNTS.items():
                    current = categorized[cat]
                    if len(current) < limit:
                        defaults = DEFAULTS[cat]
                        existing_names = {t.name for t in current}
                        candidates = [d for d in defaults if d not in existing_names]
                        import random # Actually shuffling might be better but order is fine here as list is static
                        for c_name in candidates:
                            if len(current) >= limit: break
                            t_obj = ensure_tag(c_name)
                            if t_obj: current.append(t_obj)
                    final_tags.extend(current[:limit])

                added_ids = set()
                for t in final_tags:
                    if t.id in added_ids: continue
                    st = StaffTag(staff_id=new_staff.id, tag_id=t.id)
                    db.add(st)
                    added_ids.add(t.id)

                count += 1
                if count % 10 == 0:
                    log_print(f"Propagating {count}...")

            db.commit()
            log_print(f"Import Finished. Total Staff: {count}")
            
            # Post-updates
            tonton = db.query(Staff).filter(Staff.name == "とんとん").first()
            if tonton:
                tonton.introduction = "東京都出身、とんとんです！\n\n普段の生活だけでなく、推し活などの特別な日にもあうメガネを紹介していければとおもいます！\n\n店頭でもお待ちしてます♪"
                tonton.image_url = "/images/staff/とんとん.jpg"
                ofuna = db.query(Store).filter(Store.name.like("%大船%")).first()
                if ofuna: tonton.store_id = ofuna.id
            
            gucci = db.query(Staff).filter(Staff.name == "ぐっち").first()
            if gucci: gucci.store_id = 123
            
            db.commit()
            log_print("Post updates finished.")

        except Exception as e:
            log_print(f"CRITICAL ERROR: {e}")
            traceback.print_exc(file=log)
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    import_full_staff_v4()
