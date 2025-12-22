
import csv

def inspect_katada():
    csv_path = "zoff_staff_v5_enriched.csv"
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name'] == '片田翔悟':
                print(f"Shop: {row['Shop']} | Comment Start: {row['Comment'][:20]}")

if __name__ == "__main__":
    inspect_katada()
