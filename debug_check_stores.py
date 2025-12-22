
import csv
import collections
import os

def check_store_consistency():
    csv_path = "zoff_staff_v5_enriched.csv"
    staff_stores = collections.defaultdict(set)
    
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            shop = row.get('Shop', '').strip()
            if name and shop:
                staff_stores[name].add(shop)
    
    print("Staff with multiple stores:")
    found = False
    for name, shops in staff_stores.items():
        if len(shops) > 1:
            print(f"{name}: {shops}")
            found = True
    
    if not found:
        print("No staff with multiple stores found in CSV.")
    else:
        print("\nPlease verify which store is correct based on the URL provided by the user.")

if __name__ == "__main__":
    check_store_consistency()
