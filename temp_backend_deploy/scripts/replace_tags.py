import sys
import os
from sqlalchemy import text

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.store import Tag, StaffTag, Base

def replace_tags():
    db = SessionLocal()
    try:
        print("Clearing existing staff_tags and tags...")
        # Clear foreign key dependents first
        db.query(StaffTag).delete()
        db.query(Tag).delete()
        db.commit()
        
        print("Inserting new tags...")
        
        # Define the tags data
        # Mapping: id, name, type, certification_source
        tags_data = [
            # 技術スキル (1-50)
            (1, '#フィッティング', 'EXPERT', 'LMS'),
            (2, '#視力測定', 'EXPERT', 'LMS'),
            (3, '#レンズ知識', 'EXPERT', 'LMS'),
            (4, '#加工・修理', 'EXPERT', 'LMS'),
            (5, '#遠近両用', 'EXPERT', 'LMS'),
            (6, '#強度近視対応', 'EXPERT', 'LMS'),
            (7, '#英語対応', 'EXPERT', 'SELF'),

            # 提案・スタイル (51-100)
            (51, '#色彩検定', 'OFFICIAL', 'LMS'),
            (52, '#パーソナルカラー', 'OFFICIAL', 'SELF'),
            (53, '#顔タイプ診断', 'OFFICIAL', 'SELF'),
            (54, '#似合わせ提案', 'OFFICIAL', 'SELF'),
            (55, '#トレンド', 'OFFICIAL', 'SELF'),
            (56, '#キッズ対応', 'OFFICIAL', 'SELF'),
            (57, '#ギフト選び', 'OFFICIAL', 'SELF'),
            (58, '#初めてのメガネ', 'OFFICIAL', 'SELF'),

            # シーン・用途 (101-150)
            (101, '#ビジネス', 'CASUAL', 'SELF'),
            (102, '#スポーツ', 'CASUAL', 'SELF'),
            (103, '#PC・ゲーミング', 'CASUAL', 'SELF'),
            (104, '#ドライブ', 'CASUAL', 'SELF'),
            (105, '#サウナ・温泉', 'CASUAL', 'SELF'),
            (106, '#アウトドア', 'CASUAL', 'SELF'),
            (107, '#花粉対策', 'CASUAL', 'SELF'),
            (108, '#サングラス', 'CASUAL', 'SELF'),

            # 趣味・カルチャー (201-)
            (201, '#カフェ巡り', 'CASUAL', 'SELF'),
            (202, '#サウナ', 'CASUAL', 'SELF'),
            (203, '#キャンプ', 'CASUAL', 'SELF'),
            (204, '#旅行', 'CASUAL', 'SELF'),
            (205, '#ゴルフ', 'CASUAL', 'SELF'),
            (206, '#釣り', 'CASUAL', 'SELF'),
            (207, '#野球観戦', 'CASUAL', 'SELF'),
            (208, '#サッカー観戦', 'CASUAL', 'SELF'),
            (209, '#ゲーム', 'CASUAL', 'SELF'),
            (210, '#推し活', 'CASUAL', 'SELF'),
            (211, '#マンガ・アニメ', 'CASUAL', 'SELF'),
            (212, '#読書', 'CASUAL', 'SELF'),
            (213, '#映画鑑賞', 'CASUAL', 'SELF'),
            (214, '#音楽・フェス', 'CASUAL', 'SELF'),
            (215, '#ファッション', 'CASUAL', 'SELF'),
            (216, '#古着', 'CASUAL', 'SELF'),
            (217, '#スニーカー', 'CASUAL', 'SELF'),
            (218, '#カメラ・写真', 'CASUAL', 'SELF'),
            (219, '#料理・グルメ', 'CASUAL', 'SELF'),
            (220, '#犬派', 'CASUAL', 'SELF'),
            (221, '#猫派', 'CASUAL', 'SELF'),
            (222, '#DIY', 'CASUAL', 'SELF')
        ]
        
        for t in tags_data:
            tag = Tag(id=t[0], name=t[1], type=t[2], certification_source=t[3])
            db.add(tag)
        
        db.commit()
        print("Tags updated successfully.")
        
    except Exception as e:
        print(f"Error updating tags: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    replace_tags()
