import requests
from bs4 import BeautifulSoup
import time

# Constants
LIST_URL = "https://www.zoff.co.jp/shop/contents/staff_list.aspx"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

url = f"{LIST_URL}?page=1"
print(f"Scraping page 1: {url}")
soup = get_soup(url)
if soup:
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    print("Saved HTML to page_dump.html")
