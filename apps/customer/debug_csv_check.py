
import csv
import sys
import os

def check_csv_integrity():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "zoff_staff_v5_enriched.csv")
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
                
                # Debug Output every 10 rows to see progress
                if i < 5:
                    print(f"Row {i}: {name}")
                if i % 100 == 0:
                    print(f"Processed line {reader.line_num}...")

        print(f"Total Rows Parsed: {row_count}")
        print(f"Unique Names Found: {len(unique_names)}")
        print(f"Sample Names: {list(unique_names)[:10]}")
    except Exception as e:
        print(f"Error parsing CSV at aprox line {row_count}: {e}")

if __name__ == "__main__":
    check_csv_integrity()
