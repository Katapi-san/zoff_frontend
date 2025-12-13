import requests
from bs4 import BeautifulSoup
import sys
import os

# Add backend directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.store import Store

def scrape_zoff_stores():
    url = "https://tp-shoplist.zoff.co.jp/congestion?_gl=1*135gumy*_gcl_au*ODExNjkxMjY0LjE3NjE4MjcwODEuMjUyNDk3ODg5LjE3NjM4NjMzMTEuMTc2Mzg2MzMxOA..*_ga*MTc5NzI2MTA4MC4xNzYxODI3MDg2*_ga_XRCZE4TNYH*czE3NjQ1NDA5MzEkbzkkZzAkdDE3NjQ1NDA5MzEkajYwJGwwJGg2Nzg3NTIyMA.."
    
    print(f"Fetching {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    db = SessionLocal()
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    count = 0
    
    # Finding all elements that look like store names
    # Inspecting the "read_url_content" output again, it seems many stores are listed.
    # I will look for any element text that contains "Zoff "
    
    seen_names = set()

    for element in soup.find_all(['a', 'div', 'li', 'span', 'p']):
        text = element.get_text(strip=True)
        if "Zoff" in text and len(text) < 50: # Heuristic: Store names are usually short
            # Clean up text
            store_name = text
            if store_name in seen_names:
                continue
            
            # Simple parsing of prefecture/city is hard without structure.
            # I will just save the name for now and maybe try to infer prefecture if possible.
            # Or I can try to find headers (h2, h3) that might be prefectures.
            
            # For this MVP, let's just save the store name.
            # We can try to guess prefecture from common suffixes or a mapping, 
            # but for now let's just put "Unknown" or try to find a preceding header.
            
            # Attempt to find a preceding header for prefecture
            prefecture = "Unknown"
            # This is hard to do with just find_all loop.
            
            seen_names.add(store_name)
            
            store = Store(
                name=store_name,
                prefecture=prefecture, # Placeholder
                city="Unknown",      # Placeholder
                congestion_url=url
            )
            db.add(store)
            count += 1
            
    db.commit()
    print(f"Scraped {count} stores.")
    db.close()

if __name__ == "__main__":
    scrape_zoff_stores()
