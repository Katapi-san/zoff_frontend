import json
import csv
import random
import os
import re

# File Paths
JSON_PATH = "zoff_staff_api_dump.json"
EXISTING_CSV_PATH = "../../zoff_staff_v5_enriched.csv"
OUTPUT_CSV_PATH = "new_staff_data.csv"

# Tag Categories
TAG_CATEGORIES = {
    "Technical Skills": [
        "認定眼鏡士", "加工技術", "フィッティング", "視力測定", "修理マイスター", 
        "調整技術", "コンタクト併用相談", "レンズ知識", "強度近視相談", "カラーレンズ知識"
    ],
    "Proposals/Styles": [
        "フレーム選定", "イエベ向け", "ブルベ向け", "丸顔におすすめ", "面長顔におすすめ", 
        "卵顔におすすめ", "逆三角顔におすすめ", "ベース顔におすすめ",
        "女性におすすめ", "男性におすすめ", "ユニセックスにおすすめ", 
        "初心者におすすめ", "上級者におすすめ", "お仕事にも使える", "おうち用におすすめ", 
        "だてメガネにおすすめ", "強度数におすすめ", "小顔効果", 
        "黒縁", "太縁", "べっこう柄", "クリアフレーム", "メタル", "プラスチック", "チタン", "コンビネーション",
        "クラシック", "モード", "カジュアル", "キレイめ", "スタイリッシュ", 
        "ヴィンテージ", "トレンド", "フレンチ", "韓国ファッション", "ミリタリー", "アメリカン", "ヴィンテージ風",
        "すぐに使えるサングラス", "サングラス", "春コーデにおすすめ", "夏コーデにおすすめ", "秋冬におすすめサングラス",
        "中顔面短縮みえ", "ビックシェイプ", "ラバテン"
    ],
    "Scenes/Uses": [
        "ビジネス", "デート", "旅行", "ドライブ", "スポーツ", "アウトドア", "学習用",
        "読書", "PC作業", "ゲーム", "おうち時間", "リモートワーク", "花粉対策", 
        "紫外線対策", "ギフト", "結婚式", "運転", "お仕事用"
    ],
    "Hobbies/Culture": [
        "カフェ巡り", "映画鑑賞", "音楽鑑賞", "読書", "写真", "アート", "アニメ", "ゲーム", 
        "旅行", "キャンプ", "サウナ", "筋トレ", "美容", "コスメ", "ファッション", 
        "古着", "スニーカー", "野球観戦", "ディズニー", "猫好き", "犬好き", "K-POP", 
        "料理", "ショッピング"
    ]
}

# Load Existing Data for Deduplication
existing_keys = set()
if os.path.exists(EXISTING_CSV_PATH):
    with open(EXISTING_CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = f"{row.get('Name', '').strip()}_{row.get('Shop', '').strip()}"
            existing_keys.add(key)

print(f"Loaded {len(existing_keys)} existing staff records.")

# Load JSON Data
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    staff_list = json.load(f)

new_staff_data = []

def get_attribute_value(attributes, slug):
    for attr in attributes:
        if attr['user_attribute_type']['slug'] == slug:
            return attr['user_attribute_value']['display_value']
    return ""

def generate_tags(staff_info):
    profile_text = staff_info.get('profile', '') or ""
    attributes = staff_info.get('user_attributes', [])
    tags = []
    
    # 1. Technical Skills (2 tags)
    # Priority: finding in text -> random
    tech_candidates = [t for t in TAG_CATEGORIES["Technical Skills"] if t in profile_text]
    while len(tech_candidates) < 2:
        choice = random.choice(TAG_CATEGORIES["Technical Skills"])
        if choice not in tech_candidates:
            tech_candidates.append(choice)
    tags.extend(tech_candidates[:2])
    
    # 2. Proposals/Styles (2 tags)
    style_candidates = [t for t in TAG_CATEGORIES["Proposals/Styles"] if t in profile_text]
    
    # Add attributes based tags
    face_type = get_attribute_value(attributes, "profile1")
    if face_type:
        tag = f"{face_type}におすすめ"
        if tag not in style_candidates:
            style_candidates.append(tag)
            
    personal_color = get_attribute_value(attributes, "profile3")
    if personal_color:
        if "イエベ" in personal_color:
            if "イエベ向け" not in style_candidates: style_candidates.append("イエベ向け")
        elif "ブルベ" in personal_color:
            if "ブルベ向け" not in style_candidates: style_candidates.append("ブルベ向け")

    while len(style_candidates) < 2:
        choice = random.choice(TAG_CATEGORIES["Proposals/Styles"])
        if choice not in style_candidates:
            style_candidates.append(choice)
    tags.extend(style_candidates[:2])
    
    # 3. Scenes/Uses (2-4 tags)
    scene_candidates = [t for t in TAG_CATEGORIES["Scenes/Uses"] if t in profile_text]
    target_count = random.randint(2, 4)
    while len(scene_candidates) < target_count:
        choice = random.choice(TAG_CATEGORIES["Scenes/Uses"])
        if choice not in scene_candidates:
            scene_candidates.append(choice)
    tags.extend(scene_candidates[:target_count])
    
    # 4. Hobbies/Culture (2-4 tags)
    hobby_candidates = [t for t in TAG_CATEGORIES["Hobbies/Culture"] if t in profile_text]
    target_count = random.randint(2, 4)
    while len(hobby_candidates) < target_count:
        choice = random.choice(TAG_CATEGORIES["Hobbies/Culture"])
        if choice not in hobby_candidates:
            hobby_candidates.append(choice)
    tags.extend(hobby_candidates[:target_count])
    
    # Format tags with # and comma separated
    formatted_tags = ", ".join([f"#{t}" for t in tags])
    return "\"" + formatted_tags + "\"" # Quote specifically

count = 0
for item in staff_list:
    name = item.get('name', '').strip()
    shop = item.get('shop_name', '').strip()
    
    # Check deduplication
    key = f"{name}_{shop}"
    if key in existing_keys:
        continue
        
    # Extract attributes
    attributes = item.get('user_attributes', [])
    face_type = get_attribute_value(attributes, "profile1")
    eye_position = get_attribute_value(attributes, "profile2")
    personal_color = get_attribute_value(attributes, "profile3")
    
    # Comment
    comment = item.get('profile', '')
    # Quote comment if it contains newlines or commas
    if comment:
        comment = f"\"{comment}\""
    
    # Tags
    tags = generate_tags(item)
    
    # Images
    # Use 'l' size from resized_images if available, else 'img'
    image_url = item.get('img', '')
    if 'resized_images' in item:
        for img_ver in item['resized_images']:
            if img_ver.get('size') == 'l':
                image_url = img_ver.get('url')
                break
    
    user_id = item.get('user_id', '')
    source_url = f"https://www.zoff.co.jp/shop/contents/staff_list_detail.aspx?staff_id={user_id}"
    
    image_filename = f"{name}.jpg" # Simple naming, might collide if same name in different shops?
    # Ensure unique filename if multiple staff have same name
    # But for now assuming unique names or minimal collision. 
    # Actually, let's append user_id to be safe
    image_filename = f"{name}_{user_id}.jpg"

    new_staff_data.append({
        'Name': name,
        'Shop': shop,
        'Face_Type': face_type,
        'Personal_Color': personal_color,
        'Eye_Position': eye_position,
        'Hair_Style': "", # Empty
        'Tags': tags,
        'Comment': comment,
        'Image_Filename': image_filename,
        'Source_URL': source_url,
        'Image_URL': image_url 
    })
    count += 1

print(f"Processed {count} new unique staff records.")

# Write to CSV
fieldnames = ['Name', 'Shop', 'Face_Type', 'Personal_Color', 'Eye_Position', 'Hair_Style', 'Tags', 'Comment', 'Image_Filename', 'Source_URL', 'Image_URL']

with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    # We carefully formatted tags and comment with quotes manually in some cases, 
    # but csv writer handles quoting. 
    # Let's revert manual quoting for DictWriter to handle it correctly.
    
    for row in new_staff_data:
        # Remove manual quotes for DictWriter
        if row['Tags'].startswith('"') and row['Tags'].endswith('"'):
            row['Tags'] = row['Tags'][1:-1]
        if row['Comment'].startswith('"') and row['Comment'].endswith('"'):
            row['Comment'] = row['Comment'][1:-1]
            
        writer.writerow(row)

print(f"Saved to {OUTPUT_CSV_PATH}")
