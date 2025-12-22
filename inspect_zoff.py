import requests
from bs4 import BeautifulSoup
import sys

URL = "https://www.zoff.co.jp/shop/contents/staff_list.aspx?gender=&keyword=&shop=&sort=pv&page=1"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
print(f"Fetching {URL} with headers...")
try:
    resp = requests.get(URL, headers=headers, timeout=10)
    resp.encoding = resp.apparent_encoding # Fix encoding

    resp.raise_for_status()
except Exception as e:
    print(f"Error fetching: {e}")
    sys.exit(1)

soup = BeautifulSoup(resp.content, "html.parser")

# Find staff items
# Based on output snippet, maybe <li class="item">?





print("Page Text contains 'staff'?", "staff" in soup.get_text().lower())

all_links = soup.find_all("a")
print(f"Total links: {len(all_links)}")
for i, l in enumerate(all_links[:10]):
    print(f"Link {i}: {l.get('href')}")





