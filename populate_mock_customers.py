import sqlite3
import random
import os
import shutil
import datetime
import json

# Configuration
DB_PATH = 'zoff_scope_v3.db'
GUEST_DB_PATH = r'C:\Users\hkata\Documents\Tech0\PENTASCOPE（ペンタスコープ）\zoff-scope-root\GuestDB'
PUBLIC_IMG_PATH = r'C:\Users\hkata\Documents\Tech0\PENTASCOPE（ペンタスコープ）\zoff-scope-root\apps\customer\public\images\customers'

# Customer Data [ID, Name, Gender, ImageFile]
CUSTOMERS_DATA = [
    (1, 'ときゅ', '男性', '1.jpg'),
    (2, 'とっきー', '男性', '2.jpg'),
    (3, 'のぶ', '男性', '3.jpg'),
    (4, 'りゅーや', '男性', '4.png'),
    (5, 'かたぴ', '男性', '5.png'),
    (6, 'りじちょー', '男性', '6.png'),
    (7, 'りーえー', '女性', '7.png'),
    (8, 'くろす', '男性', '8.png'),
    (9, 'おしょうさ', '男性', '9.png'),
    (10, 'リョースケ', '男性', '10.jpg')
]

FRAME_MODELS = ['Zoff SMART', 'Zoff CLASSIC', 'Zoff ATHLETE', 'Disney Collection', 'UNITED ARROWS']
LENS_TYPES = ['Standard 1.55', 'Thin 1.60', 'Super Thin 1.67', 'Blue Light Cut', 'Color Lens']

def setup_directories():
    if not os.path.exists(PUBLIC_IMG_PATH):
        os.makedirs(PUBLIC_IMG_PATH)
    
    # Copy images
    for cid, name, gender, img_file in CUSTOMERS_DATA:
        src = os.path.join(GUEST_DB_PATH, img_file)
        dst = os.path.join(PUBLIC_IMG_PATH, img_file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {img_file}")
        else:
            print(f"Warning: {img_file} not found in GuestDB")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def create_tables(conn):
    c = conn.cursor()
    
    # Customers Table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        kana TEXT,
        gender TEXT,
        age INTEGER,
        profile TEXT,
        image_url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Purchase History
    c.execute('''CREATE TABLE IF NOT EXISTS purchase_histories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        purchase_date DATE,
        frame_model TEXT,
        lens_r TEXT,
        lens_l TEXT,
        warranty_info TEXT,
        prescription_pd REAL,
        prescription_r_sph REAL,
        prescription_r_cyl REAL,
        prescription_r_axis INTEGER,
        prescription_l_sph REAL,
        prescription_l_cyl REAL,
        prescription_l_axis INTEGER,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )''')

    # Customer Preferred Tags
    c.execute('''CREATE TABLE IF NOT EXISTS customer_preferred_tags (
        customer_id INTEGER,
        tag_id INTEGER,
        PRIMARY KEY (customer_id, tag_id),
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(tag_id) REFERENCES tags(id)
    )''')

    # Reservations
    c.execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER,
        customer_id INTEGER,
        staff_id INTEGER,
        reservation_time DATETIME,
        status TEXT, -- 'Reserved', 'Check-in', 'Completed', 'Cancelled'
        memo TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(store_id) REFERENCES stores(id),
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(staff_id) REFERENCES staff(id)
    )''')
    
    conn.commit()

def generate_random_prescription():
    sph = round(random.uniform(-6.0, -0.5) * 4) / 4
    cyl = round(random.uniform(-2.0, 0.0) * 4) / 4 if random.random() > 0.5 else 0.0
    axis = random.randint(0, 180) if cyl != 0 else 0
    return sph, cyl, axis

def populate_customers(conn):
    c = conn.cursor()
    
    # Clear existing customers to avoid duplicates for this run (or update)
    # For safety, let's delete customers 1-10
    c.execute("DELETE FROM customers WHERE id <= 10")
    c.execute("DELETE FROM purchase_histories WHERE customer_id <= 10")
    c.execute("DELETE FROM customer_preferred_tags WHERE customer_id <= 10")
    # c.execute("DELETE FROM reservations") # Don't wipe all reservations maybe? Or yes, for clean state.
    # checking user request: "First make customer DB... then make reservation DB". 
    # Let's wipe reservations for the target dates to avoid overlap, but maybe full wipe is cleaner for demo.
    c.execute("DELETE FROM reservations") 

    # Fetch Tags
    c.execute("SELECT id FROM tags")
    all_tags = [row[0] for row in c.fetchall()]
    
    # Categorize Tags (Assuming IDs)
    tech_tags = [t for t in all_tags if t <= 50]
    prop_tags = [t for t in all_tags if 51 <= t <= 100]
    scene_tags = [t for t in all_tags if 101 <= t <= 200]
    hobby_tags = [t for t in all_tags if t > 200]

    for cid, name, gender, img_file in CUSTOMERS_DATA:
        # 1. Insert Customer
        age = random.randint(20, 50)
        profile = f"{age}代{gender} / 東京都在住" # Generic profile
        image_url = f"/images/customers/{img_file}"
        
        c.execute("INSERT INTO customers (id, name, gender, age, profile, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                  (cid, name, gender, age, profile, image_url))
        
        # 2. Insert Purchase History
        p_date = datetime.date(2024, random.randint(1, 12), random.randint(1, 28))
        model = random.choice(FRAME_MODELS)
        lens = random.choice(LENS_TYPES)
        pd = 60 + random.randint(-4, 4)
        r_sph, r_cyl, r_axis = generate_random_prescription()
        l_sph, l_cyl, l_axis = generate_random_prescription()
        
        c.execute('''INSERT INTO purchase_histories (
            customer_id, purchase_date, frame_model, lens_r, lens_l, warranty_info,
            prescription_pd, prescription_r_sph, prescription_r_cyl, prescription_r_axis,
            prescription_l_sph, prescription_l_cyl, prescription_l_axis
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            cid, p_date, model, lens, lens, "フレーム・レンズ保証期間中",
            pd, r_sph, r_cyl, r_axis, l_sph, l_cyl, l_axis
        ))

        # 3. Insert Preferred Tags
        selected_tags = []
        if tech_tags: selected_tags.extend(random.sample(tech_tags, min(1, len(tech_tags))))
        if prop_tags: selected_tags.extend(random.sample(prop_tags, min(1, len(prop_tags))))
        if scene_tags: selected_tags.extend(random.sample(scene_tags, min(2, len(scene_tags))))
        if hobby_tags: selected_tags.extend(random.sample(hobby_tags, min(4, len(hobby_tags))))
        
        for tid in selected_tags:
            c.execute("INSERT INTO customer_preferred_tags (customer_id, tag_id) VALUES (?, ?)", (cid, tid))

    conn.commit()
    print("Customers & Purchases populated.")

def populate_reservations(conn):
    c = conn.cursor()
    
    # 1. Identify Stores with >= 3 Staff
    c.execute("SELECT store_id, COUNT(*) as cnt FROM staff GROUP BY store_id HAVING cnt >= 3")
    target_stores = [row[0] for row in c.fetchall()]
    print(f"Found {len(target_stores)} stores with >= 3 staff.")
    
    dates = [datetime.date(2025, 12, 17), datetime.date(2025, 12, 18)]
    hours = list(range(10, 19)) # 10:00 to 18:00 start times

    reservation_count = 0
    
    for store_id in target_stores:
        # Get staff for this store
        c.execute("SELECT id FROM staff WHERE store_id = ?", (store_id,))
        store_staff_ids = [row[0] for row in c.fetchall()]
        
        for d in dates:
            num_reservations = random.randint(4, 8)
            
            # Create a pool of (hour, staff) slots to avoid overlapping staff double-booking?
            # Or just simplified: random customer, random staff, random hour.
            # Allow multiple reservations per slot if needed, but let's try to spread them.
            
            for _ in range(num_reservations):
                customer_id = random.randint(1, 10) # Reuse the 10 VIPs
                staff_id = random.choice(store_staff_ids)
                hour = random.choice(hours)
                res_time = datetime.datetime.combine(d, datetime.time(hour, 0))
                
                c.execute('''INSERT INTO reservations (
                    store_id, customer_id, staff_id, reservation_time, status, memo
                ) VALUES (?, ?, ?, ?, ?, ?)''', (
                    store_id, customer_id, staff_id, res_time, 'Reserved', 'アプリからの予約'
                ))
                reservation_count += 1

    conn.commit()
    print(f"Created {reservation_count} reservations (Random phase).")

    # --- CUSTOM FIXES FOR USER REQUEST ---
    print("Applying custom fixes...")
    target_date = datetime.date(2025, 12, 17)
    target_store_id = 287
    
    # Check if store 287 exists
    c.execute("SELECT id FROM stores WHERE id = ?", (target_store_id,))
    if not c.fetchone():
        # Fallback: find any store with staff
        c.execute("SELECT store_id FROM staff GROUP BY store_id HAVING COUNT(*) >= 1 LIMIT 1")
        row = c.fetchone()
        if row:
            print(f"Store {target_store_id} not found, using {row[0]} instead for custom fixes.")
            target_store_id = row[0]
        else:
            print("No suitable stores found! Skipping custom fixes.")
            conn.commit()
            return

    start_of_day = datetime.datetime.combine(target_date, datetime.time(0, 0))
    end_of_day = datetime.datetime.combine(target_date, datetime.time(23, 59, 59))
    
    # Delete conflicting reservations
    # 1. Any existing for Customer 1 (Tokyu) or 10 (Ryosuke) on this day
    # 2. Any reservation at 15:00 on this day (to make room/ensure cleanliness)
    c.execute("DELETE FROM reservations WHERE (customer_id IN (1, 10) OR reservation_time = ?) AND reservation_time BETWEEN ? AND ?", 
              (datetime.datetime.combine(target_date, datetime.time(15, 0)), start_of_day, end_of_day))

    # Get a staff member for assignment
    c.execute("SELECT id FROM staff WHERE store_id = ? LIMIT 1", (target_store_id,))
    staff_row = c.fetchone()
    staff_id = staff_row[0] if staff_row else None
    
    # 1. Tokyu (ID 1): Adjustment, Unassigned
    # Using existing logic: if staff_id is NULL, it will be Unassigned in UI
    c.execute('''INSERT INTO reservations (
        store_id, customer_id, staff_id, reservation_time, status, memo
    ) VALUES (?, ?, ?, ?, ?, ?)''', (
        target_store_id, 1, None, 
        datetime.datetime.combine(target_date, datetime.time(11, 0)), 
        'Reservation', '調整・メンテナンス'
    ))

    # 2. Ryosuke (ID 10): 10:00 only. Assigned.
    c.execute('''INSERT INTO reservations (
        store_id, customer_id, staff_id, reservation_time, status, memo
    ) VALUES (?, ?, ?, ?, ?, ?)''', (
        target_store_id, 10, staff_id, 
        datetime.datetime.combine(target_date, datetime.time(10, 0)), 
        'Reservation_Nomination' if staff_id else 'Reservation', 'メガネ作成・調整'
    ))

    # 3. Someone else (ID 6 Rijicho) at 15:00
    c.execute('''INSERT INTO reservations (
        store_id, customer_id, staff_id, reservation_time, status, memo
    ) VALUES (?, ?, ?, ?, ?, ?)''', (
        target_store_id, 6, staff_id, 
        datetime.datetime.combine(target_date, datetime.time(15, 0)), 
        'Reservation_Nomination' if staff_id else 'Reservation', 'メガネ作成・調整'
    ))

    conn.commit()
    print("Applied custom fixes for Tokyu & Ryosuke.")

def main():
    setup_directories()
    conn = get_db_connection()
    create_tables(conn)
    populate_customers(conn)
    populate_reservations(conn)
    conn.close()

if __name__ == "__main__":
    main()
