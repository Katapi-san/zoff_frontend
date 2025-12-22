import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import re

# Constants
BASE_URL = "https://www.zoff.co.jp"
LIST_URL = "https://www.zoff.co.jp/shop/contents/staff_list.aspx"
EXISTING_CSV_PATH = "../../zoff_staff_v5_enriched.csv"
OUTPUT_CSV_PATH = "new_staff_raw.csv"

# existing staff set for deduplication
existing_staff = set()

if os.path.exists(EXISTING_CSV_PATH):
    with open(EXISTING_CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a unique key using Name and Shop
            key = f"{row.get('Name', '').strip()}_{row.get('Shop', '').strip()}"
            existing_staff.add(key)

print(f"Loaded {len(existing_staff)} existing staff records.")

new_staff_data = []

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def clean_text(text):
    if not text:
        return ""
    return text.strip()

# Pages to scrape
pages = [1, 2, 3, 4, 5]

for page in pages:
    url = f"{LIST_URL}?page={page}"
    print(f"Scraping page {page}: {url}")
    soup = get_soup(url)
    if not soup:
        continue

    # Identify staff blocks
    # Based on observation, staff list items might be in <li> with class starting with 'staff-list' or similar
    # Or parsing generic structure if classes are obfuscated.
    # Looking at provided info: "staff__thum" is for images.
    
    # Assuming standard structure based on common patterns or simple search
    # This might need adjustment if HTML structure is complex.
    # Let's try to find elements that contain .staff__thum
    
    staff_items = soup.select('.staffList .StaffItem') # Hypothetical selector
    if not staff_items:
        # Fallback to broader search
        staff_items = soup.select('li')
        # Filter for those having staff__thum
        staff_items = [li for li in staff_items if li.select_one('.staff__thum')]

    print(f"Found {len(staff_items)} items on page {page}.")

    for item in staff_items:
        try:
            # Extract basic info
            image_node = item.select_one('.staff__thum img')
            image_url = image_node['src'] if image_node else ""
            if image_url and not image_url.startswith('http'):
                image_url = BASE_URL + image_url
            
            # Name and Shop often in .staff__name, .staff__shop or similar
            # If not specific, get text lines.
            
            name_node = item.select_one('.staff__name')
            name = clean_text(name_node.text) if name_node else "Unknown"
            
            shop_node = item.select_one('.staff__shop')
            shop = clean_text(shop_node.text) if shop_node else "Unknown"
            
            # Detail Link
            link_node = item.select_one('a')
            detail_url = ""
            if link_node and 'href' in link_node.attrs:
                detail_url = link_node['href']
                if not detail_url.startswith('http'):
                    detail_url = BASE_URL + detail_url

            # Deduplication Check
            key = f"{name}_{shop}"
            if key in existing_staff:
                # print(f"Skipping existing: {name} at {shop}")
                continue

            print(f"New staff found: {name} at {shop}")

            # Fetch Detail Page
            face_type = ""
            personal_color = ""
            eye_position = ""
            hair_style = "" # Not always available
            comment = ""
            
            if detail_url:
                time.sleep(0.5) # Be polite
                detail_soup = get_soup(detail_url)
                if detail_soup:
                    # Parse attributes from detail page
                    # Usually in a definition list <dl> or table
                    # Example placeholders:
                    # <dt>顔型</dt><dd>丸顔</dd>
                    
                    # Extract full text for context
                    full_text = detail_soup.get_text()
                    
                    # Try to find attributes
                    # This part is heuristics based on Japanese keywords
                    
                    # Comment
                    comment_node = detail_soup.select_one('.staff__comment, .commentArea')
                    if comment_node:
                        comment = clean_text(comment_node.text)
                    else:
                        # Fallback try to get large text block
                        pass

                    # Parsing attributes from specific blocks if possible
                    # Assuming there's a spec list
                    specs = detail_soup.select('dl.staff__spec dt')
                    for dt in specs:
                        label = clean_text(dt.text)
                        dd = dt.find_next_sibling('dd')
                        value = clean_text(dd.text) if dd else ""
                        
                        if "顔型" in label:
                            face_type = value
                        elif "パーソナルカラー" in label:
                            personal_color = value
                        # Add more mappings as needed

            # Store data
            new_staff_data.append({
                'Name': name,
                'Shop': shop,
                'Face_Type': face_type,
                'Personal_Color': personal_color,
                'Eye_Position': eye_position,
                'Hair_Style': hair_style,
                'Tags': "", # To be filled later
                'Comment': comment,
                'Image_Filename': f"{name}_{len(new_staff_data)}.jpg", # Placeholder
                'Source_URL': detail_url,
                'Image_URL': image_url
            })

        except Exception as e:
            print(f"Error parsing item: {e}")
            continue

print(f"Total new unique staff found: {len(new_staff_data)}")

# Write to CSV
fieldnames = ['Name', 'Shop', 'Face_Type', 'Personal_Color', 'Eye_Position', 'Hair_Style', 'Tags', 'Comment', 'Image_Filename', 'Source_URL', 'Image_URL']

with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_staff_data)

print(f"Saved to {OUTPUT_CSV_PATH}")
