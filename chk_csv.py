
import csv
import sys
import os

def check_csv_integrity():
    csv_path = "zoff_staff_v5_enriched.csv"
    print(f"Checking {csv_path}...")
    
    unique_names = set()
    row_count = 0
    
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                row_count += 1
                name = row.get('Name', '').strip()
                if name:
                    unique_names.add(name)
                
                if i % 10 == 0:
                    print(f"Row {i}: {name} (Line: {reader.line_num})")

        print(f"Total Rows Parsed: {row_count}")
        print(f"Unique Names Found: {len(unique_names)}")
    except Exception as e:
        print(f"Error parsing CSV: {e}")

if __name__ == "__main__":
    check_csv_integrity()
