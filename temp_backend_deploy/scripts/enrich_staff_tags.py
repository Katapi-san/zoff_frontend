
import csv
import random
import os
import sys

# Define Tag Masters with Categories
# Based on ID ranges:
# 1-50: Technical Skills
# 51-100: Proposal / Style
# 101-200: Scene / Use
# 201+: Hobby / Culture

TAG_MASTER = {
    "technical": {
        "range": (1, 50),
        "tags": [
            "#認定眼鏡士", "#フィッティング", "#加工技術", "#視力測定", "#レンズ知識", 
            "#修理マイスター", "#調整技術", "#遠近両用", "#カラーレンズ知識", "#フレーム選定",
            "#コンタクト併用相談", "#お子様メガネ", "#強度近視相談"
        ]
    },
    "style": {
        "range": (51, 100),
        "tags": [
            "#トレンド", "#クラシック", "#モード", "#フェミニン", "#ビジネス", 
            "#カジュアル", "#ストリート", "#ミニマル", "#ヴィンテージ", "#シンプル", 
            "#個性派", "#韓国ファッション", "#アメリカン", "#フレンチ", "#レトロ",
            "#イエベ春", "#イエベ秋", "#ブルベ夏", "#ブルベ冬", # Personal colors mapped here
            "#丸顔", "#面長", "#三角顔", "#四角顔" # Face types mapped here
        ]
    },
    "scene": {
        "range": (101, 200),
        "tags": [
            "#お仕事用", "#PC作業", "#ドライブ", "#アウトドア", "#スポーツ", 
            "#デート", "#読書", "#おうち時間", "#旅行", "#ギフト", 
            "#サングラス", "#花粉対策", "#リモートワーク", "#運転", "#学習用"
        ]
    },
    "hobby": {
        "range": (201, 300),
        "tags": [
            "#カフェ巡り", "#サウナ", "#映画鑑賞", "#音楽鑑賞", "#K-POP", 
            "#キャンプ", "#写真", "#古着", "#アニメ", "#ゲーム", 
            "#料理", "#旅行", "#読書", "#アート", "#筋トレ", 
            "#スニーカー", "#ディズニー", "#ショッピング", "#美容", "#犬好き", "#猫好き" # Added generic hobbies
        ]
    }
}

# Mapping keywords in comments to tags
KEYWORD_MAP = {
    "フィッティング": "#フィッティング",
    "調整": "#調整技術",
    "加工": "#加工技術",
    "認定": "#認定眼鏡士",
    "遠近": "#遠近両用",
    "レンズ": "#レンズ知識",
    "修理": "#修理マイスター",
    "トレンド": "#トレンド",
    "クラシック": "#クラシック",
    "モード": "#モード",
    "ビジネス": "#ビジネス",
    "仕事": "#お仕事用",
    "PC": "#PC作業",
    "パソコン": "#PC作業",
    "ドライブ": "#ドライブ",
    "アウトドア": "#アウトドア",
    "キャンプ": "#キャンプ",
    "サウナ": "#サウナ",
    "カフェ": "#カフェ巡り",
    "映画": "#映画鑑賞",
    "音楽": "#音楽鑑賞",
    "K-POP": "#K-POP",
    "韓国": "#韓国ファッション",
    "アニメ": "#アニメ",
    "古着": "#古着",
    "写真": "#写真",
    "カメラ": "#写真",
    "旅行": "#旅行"
}

def enrich_tags():
    input_file = "zoff_staff_v4_tags.csv"
    output_file = "zoff_staff_v5_enriched.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print("Enriching staff tags...")
    
    enriched_data = []
    
    with open(input_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        # We will append a new column 'Enriched_Tags' (JSON-like string or just comma separated) 
        # But import script needs to handle it. 
        # Actually, let's just update 'Tags' column.
        
        for row in reader:
            comment = row.get('Comment', '') or ''
            existing_tags = row.get('Tags', '')
            existing_tag_list = [t.strip() for t in existing_tags.replace('、', ',').split(',') if t.strip()]

            # Categorize existing tags (loose matching)
            current_tags = {
                "technical": [],
                "style": [],
                "scene": [],
                "hobby": []
            }

            # Helper to assign existing tags to categories if they match master
            # If not in master, assign to 'style' or 'scene' by heuristics or drop?
            # Let's keep them and map to nearest category or 'style' as regex bucket
            for t in existing_tag_list:
                assigned = False
                for cat, master in TAG_MASTER.items():
                    if t in master["tags"]:
                        current_tags[cat].append(t)
                        assigned = True
                        break
                if not assigned:
                    # Heuristic: mostly proposal/style or scene
                    # If starts with #, keep it.
                    if "おすすめ" in t:
                        current_tags["scene"].append(t)
                    elif "イエベ" in t or "ブルベ" in t:
                        current_tags["style"].append(t)
                    else:
                        current_tags["style"].append(t) 

            # Enrich from Comment keywords
            for kw, tag in KEYWORD_MAP.items():
                if kw in comment:
                    # Find category for this tag
                    for cat, master in TAG_MASTER.items():
                        if tag in master["tags"] and tag not in current_tags[cat]:
                            current_tags[cat].append(tag)

            # Ensure counts
            # Technical: 2
            while len(current_tags["technical"]) < 2:
                t = random.choice(TAG_MASTER["technical"]["tags"])
                if t not in current_tags["technical"]:
                    current_tags["technical"].append(t)
            current_tags["technical"] = current_tags["technical"][:2]

            # Style: 2
            while len(current_tags["style"]) < 2:
                t = random.choice(TAG_MASTER["style"]["tags"])
                if t not in current_tags["style"]:
                    current_tags["style"].append(t)
            current_tags["style"] = current_tags["style"][:2]

            # Scene: 2
            while len(current_tags["scene"]) < 2:
                t = random.choice(TAG_MASTER["scene"]["tags"])
                if t not in current_tags["scene"]:
                    current_tags["scene"].append(t)
            current_tags["scene"] = current_tags["scene"][:2]

            # Hobby: 3-4
            target_hobby_count = random.randint(3, 4)
            while len(current_tags["hobby"]) < target_hobby_count:
                t = random.choice(TAG_MASTER["hobby"]["tags"])
                if t not in current_tags["hobby"]:
                    current_tags["hobby"].append(t)
            current_tags["hobby"] = current_tags["hobby"][:target_hobby_count]

            # Combine all tags
            all_tags = []
            all_tags.extend(current_tags["technical"])
            all_tags.extend(current_tags["style"])
            all_tags.extend(current_tags["scene"])
            all_tags.extend(current_tags["hobby"])
            
            row['Tags'] = ", ".join(all_tags)
            enriched_data.append(row)

    # Write to new CSV
    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_data)

    print(f"Enriched data written to {output_file}")

if __name__ == "__main__":
    enrich_tags()
