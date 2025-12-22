"""
顧客データと購入履歴、予約データを作成するスクリプト
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Customer, PurchaseHistory, Reservation, CustomerPreferredTag, Tag
from datetime import datetime, timedelta
import random

# テーブル作成
Base.metadata.create_all(bind=engine)

def create_sample_customers(db: Session):
    """サンプル顧客データを作成"""
    
    # 既存の顧客を削除
    db.query(CustomerPreferredTag).delete()
    db.query(Reservation).delete()
    db.query(PurchaseHistory).delete()
    db.query(Customer).delete()
    db.commit()
    
    print("Creating sample customers...")
    
    sample_customers = [
        {
            "name": "田中 太郎",
            "kana": "タナカ タロウ",
            "gender": "男性",
            "age": 35,
            "profile": "アウトドアが趣味のIT企業勤務。スポーツサングラスに興味あり。",
            "image_url": None
        },
        {
            "name": "佐藤 花子",
            "kana": "サトウ ハナコ",
            "gender": "女性",
            "age": 28,
            "profile": "ファッション業界勤務。トレンドに敏感でデザイン重視。",
            "image_url": None
        },
        {
            "name": "鈴木 一郎",
            "kana": "スズキ イチロウ",
            "gender": "男性",
            "age": 45,
            "profile": "経営者。ビジネスシーンでの使用が中心。品質重視。",
            "image_url": None
        },
        {
            "name": "高橋 美咲",
            "kana": "タカハシ ミサキ",
            "gender": "女性",
            "age": 22,
            "profile": "大学生。カジュアルでかわいいデザインを好む。",
            "image_url": None
        },
        {
            "name": "伊藤 健太",
            "kana": "イトウ ケンタ",
            "gender": "男性",
            "age": 52,
            "profile": "会社員。老眼対策で遠近両用レンズを使用。",
            "image_url": None
        },
        {
            "name": "渡辺 真理",
            "kana": "ワタナベ マリ",
            "gender": "女性",
            "age": 38,
            "profile": "主婦。子育て中でブルーライトカット機能を重視。",
            "image_url": None
        },
        {
            "name": "ときゅ",
            "kana": "トキュ",
            "gender": "男性",
            "age": 25,
            "profile": "デモ用顧客。アプリ開発エンジニア。",
            "image_url": None
        },
        {
            "name": "りじちょー",
            "kana": "リジチョー",
            "gender": "男性",
            "age": 40,
            "profile": "デモ用顧客。経営者。",
            "image_url": None
        },
        {
            "name": "かたやま",
            "kana": "カタヤマ",
            "gender": "男性",
            "age": 31,
            "profile": "デモ用顧客。メガネ作成・調整。",
            "image_url": None
        },
        {
            "name": "とっきー",
            "kana": "トッキー",
            "gender": "男性",
            "age": 20,
            "profile": "デモ用顧客。",
            "image_url": None
        }
    ]
    
    customers = []
    for data in sample_customers:
        customer = Customer(**data)
        db.add(customer)
        customers.append(customer)
    
    db.commit()
    print(f"Created {len(customers)} customers")
    
    # 購入履歴を作成
    create_purchase_histories(db, customers)
    
    # 顧客の好みタグを作成
    create_customer_preferred_tags(db, customers)
    
    # 予約データを作成
    create_reservations(db, customers)
    
    return customers

def create_purchase_histories(db: Session, customers: list):
    """購入履歴を作成"""
    print("Creating purchase histories...")
    
    frame_models = [
        "ZA231010", "ZA231011", "ZA231012", "ZA231013", "ZA231014",
        "ZA231015", "ZA231016", "ZN231001", "ZN231002", "ZN231003"
    ]
    
    lens_types = [
        "1.60薄型非球面", "1.67超薄型非球面", "1.74最薄型非球面",
        "調光レンズ", "ブルーライトカットレンズ", "遠近両用レンズ"
    ]
    
    histories = []
    for customer in customers:
        # 各顧客に1〜3件の購入履歴を作成
        num_purchases = random.randint(1, 3)
        
        for i in range(num_purchases):
            days_ago = random.randint(30, 730)  # 過去30日〜2年
            purchase_date = datetime.now().date() - timedelta(days=days_ago)
            
            history = PurchaseHistory(
                customer_id=customer.id,
                purchase_date=purchase_date,
                frame_model=random.choice(frame_models),
                lens_r=random.choice(lens_types),
                lens_l=random.choice(lens_types),
                warranty_info="1年保証",
                prescription_pd=random.uniform(60, 70),
                prescription_r_sph=random.uniform(-5.0, 2.0),
                prescription_r_cyl=random.uniform(-2.0, 0),
                prescription_r_axis=random.randint(0, 180),
                prescription_l_sph=random.uniform(-5.0, 2.0),
                prescription_l_cyl=random.uniform(-2.0, 0),
                prescription_l_axis=random.randint(0, 180)
            )
            db.add(history)
            histories.append(history)
    
    db.commit()
    print(f"Created {len(histories)} purchase histories")

def create_customer_preferred_tags(db: Session, customers: list):
    """顧客の好みタグを作成"""
    print("Creating customer preferred tags...")
    
    # タグを取得
    tags = db.query(Tag).all()
    if not tags:
        print("No tags found. Skipping preferred tags creation.")
        return
    
    preferred_tags = []
    for customer in customers:
        # 各顧客に2〜5個のタグを割り当て
        num_tags = random.randint(2, 5)
        selected_tags = random.sample(tags, min(num_tags, len(tags)))
        
        for tag in selected_tags:
            pref_tag = CustomerPreferredTag(
                customer_id=customer.id,
                tag_id=tag.id
            )
            db.add(pref_tag)
            preferred_tags.append(pref_tag)
    
    db.commit()
    print(f"Created {len(preferred_tags)} customer preferred tags")

def create_reservations(db: Session, customers: list):
    """予約データを作成"""
    print("Creating reservations...")
    
    # 店舗IDを1〜10と仮定（実際の店舗数に応じて調整）
    # 店舗IDを1〜10と特定のID（UI確認用）とする
    store_ids = list(range(1, 11)) + [256, 287]
    
    # スタッフIDを1〜50と仮定（実際のスタッフ数に応じて調整）
    staff_ids = list(range(1, 51))
    
    statuses = ["confirmed", "completed", "cancelled", "pending"]
    
    reservations = []
    reservation_counter = 0  # カウンターで半々を管理
    
    for customer in customers:
        # 各顧客に0〜2件の予約を作成
        num_reservations = random.randint(0, 2)
        
        for i in range(num_reservations):
            # 未来または過去の予約
            if random.random() < 0.7:  # 70%は未来の予約
                days_ahead = random.randint(1, 30)
                reservation_time = datetime.now() + timedelta(days=days_ahead, hours=random.randint(10, 18))
                status = random.choice(["confirmed", "pending"])
            else:  # 30%は過去の予約
                days_ago = random.randint(1, 90)
                reservation_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(10, 18))
                status = random.choice(["completed", "cancelled"])
            
            # 指名予約と指名なしを半々に (ただし特定顧客は強制的に指名なし)
            if customer.name in ["ときゅ", "りじちょー", "かたやま", "とっきー"]:
                has_staff = False
            else:
                has_staff = (reservation_counter % 2 == 0)
            
            reservation = Reservation(
                store_id=random.choice(store_ids),
                customer_id=customer.id,
                staff_id=random.choice(staff_ids) if has_staff else None,
                reservation_time=reservation_time,
                status=status,
                memo=f"顧客メモ: {customer.name}様の予約" if random.random() < 0.5 else None
            )
            db.add(reservation)
            reservations.append(reservation)
            reservation_counter += 1
    
    db.commit()
    print(f"Created {len(reservations)} reservations")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        customers = create_sample_customers(db)
        print("\n✅ Sample customer data created successfully!")
        print(f"Total customers: {len(customers)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()
