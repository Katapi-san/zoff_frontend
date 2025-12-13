import sys
import os

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.store import Staff, Tag, StaffTag, Store, Base

def seed_data():
    db = SessionLocal()

    # Create tables if they don't exist (just in case)
    Base.metadata.create_all(bind=engine)

    print("Clearing existing staff and tags...")
    db.query(StaffTag).delete()
    db.query(Staff).delete()
    db.query(Tag).delete()
    db.commit()

    print("Seeding Tags...")
    tags_data = [
        {"name": "#フィッティング", "type": "EXPERT", "certification_source": "LMS"},
        {"name": "#色彩検定", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#キッズ", "type": "CASUAL", "certification_source": "SELF"},
        {"name": "#レンズ知識", "type": "EXPERT", "certification_source": "LMS"},
        {"name": "#修理", "type": "EXPERT", "certification_source": "LMS"},
        {"name": "#スポーツ", "type": "CASUAL", "certification_source": "SELF"},
        {"name": "#調整", "type": "EXPERT", "certification_source": "LMS"},
        {"name": "#色彩検定1級", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#キッズ対応", "type": "CASUAL", "certification_source": "SELF"},
        {"name": "#イエベ春", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#骨格ストレート", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#顔タイプキュート", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#卵顔", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#普通", "type": "CASUAL", "certification_source": "SELF"},
        {"name": "#イエベ", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#寄り目", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#面長顔", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#ブルベ", "type": "OFFICIAL", "certification_source": "SELF"},
        {"name": "#三角顔", "type": "OFFICIAL", "certification_source": "SELF"},
    ]

    tag_ids = {}
    for t_data in tags_data:
        tag = Tag(**t_data)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        tag_ids[t_data["name"]] = tag.id

    print("Seeding Staff...")
    
    def get_store_id(name_part):
        store = db.query(Store).filter(Store.name.like(f"%{name_part}%")).first()
        if store:
            return store.id
        # Fallback to first store if not found
        return db.query(Store).first().id

    staff_data = [
        {
            "name": "つなかん",
            "display_name": "つなかん",
            "real_name": "つなかん",
            "role": "スタッフ",
            "store_name_query": "渋谷マークシティ",
            "image_url": "/images/staff/tsunakan.jpg",
            "tags": ["#色彩検定1級", "#キッズ対応", "#イエベ春", "#骨格ストレート", "#顔タイプキュート"],
            "scope_score": 95,
            "introduction": "📍神奈川県出身｜販売歴6年目\n👓 メガネ選びをもっと楽しく、ハッピーに✨\n🔥 STAFF OF THE YEAR 2025 物販部門 第2位 🥈\n\n📏 159cm\n🎨 パーソナルカラー：イエベ春（2nd ブルベ冬）\n💎 骨格タイプ：ストレート\n💖 顔タイプ：キュート"
        },
        {
            "name": "Ayako",
            "display_name": "Ayako",
            "real_name": "Ayako",
            "role": "スタッフ",
            "store_name_query": "ミカン下北",
            "image_url": "/images/staff/ayako.jpg",
            "tags": ["#卵顔", "#寄り目", "#イエベ"],
            "scope_score": 88,
            "introduction": "販売歴1年目🌸\nイエベ春/卵顔/求心顔PD57\n\n歴が浅い分お客様と同じ視点で\nオススメフレームご紹介しています𓈒𓏸\n\n綺麗め上品なメタルフレームや\n中顔面短縮見えのビッグシェイプ\nが好みです𓍯𓈒𓏸\n\nミカン下北店でお待ちしてます౨ৎ ݁˖ . ݁"
        },
        {
            "name": "とらいあんぐる",
            "display_name": "とらいあんぐる",
            "real_name": "とらいあんぐる",
            "role": "スタッフ",
            "store_name_query": "橿原",
            "image_url": "/images/staff/triangle.jpg",
            "tags": ["#面長顔", "#普通", "#イエベ"],
            "scope_score": 85,
            "introduction": "奈良県出身。\n2児の父親です。\n\n眼鏡常用者なので\n日常使いしやすい眼鏡、\n飽きがこない眼鏡の提案が得意です。\n\n趣味は\n野球観戦⚾\n麻雀🀄\n\nエッホエッホ\n眼鏡の良さを伝えなきゃ。"
        },
        {
            "name": "ぽりん",
            "display_name": "ぽりん",
            "real_name": "ぽりん",
            "role": "スタッフ",
            "store_name_query": "渋谷",
            "image_url": "/images/staff/porin.jpg",
            "tags": ["#卵顔", "#普通", "#イエベ"],
            "scope_score": 80,
            "introduction": "皆様のメガネ選びの参考になれば嬉しいです¨̮⃝"
        },
        {
            "name": "guppy",
            "display_name": "guppy",
            "real_name": "guppy",
            "role": "スタッフ",
            "store_name_query": "本社",
            "image_url": "/images/staff/guppy.jpg",
            "tags": ["#卵顔", "#普通", "#ブルベ"],
            "scope_score": 82,
            "introduction": "guppyです☺︎\n顔のカタチ（タマゴ型）に似合うボストンやウェリントンの眼鏡をよくかけています!!皆様の眼鏡選びの参考になると嬉しいです。\n\nよろしければInstagramもチェックしてみてください✔︎"
        },
        {
            "name": "Haru",
            "display_name": "Haru",
            "real_name": "Haru",
            "role": "スタッフ",
            "store_name_query": "イオンモール京都桂川",
            "image_url": "/images/staff/haru.jpg",
            "tags": ["#三角顔", "#普通", "#イエベ"],
            "scope_score": 80,
            "introduction": "京都出身　入社歴1年です！\n普段はライブやカフェ巡りなど外に出かけるのがとにかく好きでカジュアルコーデや綺麗目なモノトーンコーデなど色々着てます！"
        }
    ]

    for s_data in staff_data:
        tag_names = s_data.pop("tags")
        store_query = s_data.pop("store_name_query")
        s_data["store_id"] = get_store_id(store_query)
        
        staff = Staff(**s_data)
        db.add(staff)
        db.commit()
        db.refresh(staff)

        for tag_name in tag_names:
            if tag_name in tag_ids:
                staff_tag = StaffTag(staff_id=staff.id, tag_id=tag_ids[tag_name])
                db.add(staff_tag)
        db.commit()

    print("Done seeding staff and tags.")
    db.close()

if __name__ == "__main__":
    seed_data()
