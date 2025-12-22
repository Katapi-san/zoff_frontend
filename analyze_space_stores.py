import sqlite3
import os

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

    print(f"Analyzing {len(BAD_IDS)} IDs...")
    
    found_targets = []
    missing_targets = []

    for bit_id in BAD_IDS:
        cursor.execute("SELECT name FROM stores WHERE id = ?", (bit_id,))
        row = cursor.fetchone()
        if not row:
            print(f"ID {bit_id}: Not found in DB")
            continue
        
        name = row[0]
        # Check if it starts with space
        if not name.startswith(" "):
            # Special check for 626 or others that might have hidden chars or user description was slightly off
            # But user said "Like ' 札幌...'"
            # Let's try stripping whitespace
            cleaned = name.strip()
            if cleaned == name:
                 print(f"ID {bit_id}: Name '{name}' does not start with space. Skipping auto-detect.")
                 continue
        else:
            cleaned = name.strip() # Remove leading/trailing spaces
            
        # Try to find target
        cursor.execute("SELECT id, name FROM stores WHERE name = ? AND id != ?", (cleaned, bit_id))
        targets = cursor.fetchall()
        
        if len(targets) == 1:
            target_id = targets[0][0]
            print(f"MATCH: '{name}' ({bit_id}) -> '{targets[0][1]}' ({target_id})")
            found_targets.append((bit_id, target_id))
        elif len(targets) > 1:
            print(f"AMBIGUOUS: '{name}' ({bit_id}) -> Found {len(targets)} matches: {targets}")
        else:
            # Try searching with LIKE just in case
            print(f"NO MATCH: '{name}' ({bit_id}) -> No exact match for '{cleaned}'")
            missing_targets.append(bit_id)

    conn.close()
    
    print(f"\nFound {len(found_targets)} valid merge pairs.")
    print(f"Missing targets for {len(missing_targets)} IDs.")

if __name__ == "__main__":
    analyze_stores()
