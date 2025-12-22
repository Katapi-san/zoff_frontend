
import csv
import collections
import re
from datetime import datetime

def check_store_consistency_with_dates():
    csv_path = "zoff_staff_v5_enriched.csv"
    staff_stores = collections.defaultdict(list)
    
    date_pattern = re.compile(r'20\d{2}\.\d{2}\.\d{2}')

    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            shop = row.get('Shop', '').strip()
            comment = row.get('Comment', '')
            
            # Find date
            match = date_pattern.search(comment)
            date_obj = datetime.min
            if match:
                try:
                    date_obj = datetime.strptime(match.group(), '%Y.%m.%d')
                except:
                    pass
            
            if name and shop:
                staff_stores[name].append({
                    'shop': shop,
                    'date': date_obj,
                    'raw_date': match.group() if match else "None"
                })
    
    print("Conflict Resolution Proposal:")
    overrides = {}
    
    for name, entries in staff_stores.items():
        shops = {e['shop'] for e in entries}
        if len(shops) > 1:
            # Sort by date descending
            entries.sort(key=lambda x: x['date'], reverse=True)
            latest = entries[0]
            print(f"Name: {name}")
            print(f"  Conflict Shops: {shops}")
            print(f"  Latest (by date): {latest['shop']} ({latest['raw_date']})")
            overrides[name] = latest['shop']
            print("-" * 20)
            
    return overrides

if __name__ == "__main__":
    check_store_consistency_with_dates()
