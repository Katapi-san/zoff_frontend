import sqlite3
import os
import sys

# Set output encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = 'backend/downloaded_zoff_scope_v3.db'

BAD_IDS = [
    568, 571, 575, 576, 577, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 
    594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 
    614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633
]

def analyze_stores():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    merges = []

    for bit_id in BAD_IDS:
        cursor.execute("SELECT name FROM stores WHERE id = ?", (bit_id,))
        row = cursor.fetchone()
        if not row:
            print(f"# ID {bit_id}: Not found")
            continue
        
        name = row[0]
        cleaned = name.strip()
        
        # Try finding exact match for cleaned name
        cursor.execute("SELECT id, name FROM stores WHERE name = ? AND id != ?", (cleaned, bit_id))
        targets = cursor.fetchall()
        
        if len(targets) == 1:
            target_id = targets[0][0]
            merges.append((target_id, bit_id))
            print(f"        ({target_id}, {bit_id}), # {cleaned}")
        elif len(targets) > 1:
            # If duplicates, pick one? Or unsafe?
            # User rule says: "同名の店舗”札幌アピア店”". If there are multiple, any is likely fine if they are duplicates, but let's see.
            print(f"# AMBIGUOUS for {bit_id} '{name}': Found IDs {[t[0] for t in targets]}")
            # Heuristic: Pick the smallest ID (likely original)
            best_target = min(targets, key=lambda x: x[0])
            merges.append((best_target[0], bit_id))
            print(f"        ({best_target[0]}, {bit_id}), # {cleaned} (Chosen from ambiguous)")
        else:
            # Try removing 'Zoff ' prefix if present in cleaned
            if cleaned.startswith("Zoff "):
                no_zoff = cleaned[5:]
                cursor.execute("SELECT id, name FROM stores WHERE name = ? AND id != ?", (no_zoff, bit_id))
                targets_nz = cursor.fetchall()
                if len(targets_nz) == 1:
                    merges.append((targets_nz[0][0], bit_id))
                    print(f"        ({targets_nz[0][0]}, {bit_id}), # {cleaned} (Assuming match without 'Zoff ' prefix)")
                    continue
            
            # OR try ADDING 'Zoff '?
            with_zoff = "Zoff " + cleaned
            cursor.execute("SELECT id, name FROM stores WHERE name = ? AND id != ?", (with_zoff, bit_id))
            targets_wz = cursor.fetchall()
            if len(targets_wz) == 1:
                merges.append((targets_wz[0][0], bit_id))
                print(f"        ({targets_wz[0][0]}, {bit_id}), # {cleaned} (Assuming match WITH 'Zoff ' prefix)")
                continue

            print(f"# NO MATCH for {bit_id} '{name}' -> Cleaned '{cleaned}'")

    with open("generated_merges.py", "w", encoding="utf-8") as f:
        f.write("GENERATED_MERGES = [\n")
        f.write("    # (Keep ID, Delete ID), # Name\n")
        
        for keep, delete in merges:
            # Re-fetch name for comment
            cursor.execute("SELECT name FROM stores WHERE id = ?", (keep,))
            k_name = cursor.fetchone()[0]
            f.write(f"    ({keep}, {delete}), # {k_name}\n")
            
        f.write("]\n")
    
    print(f"Start: {len(BAD_IDS)}, Found: {len(merges)}")
    conn.close()

if __name__ == "__main__":
    analyze_stores()
