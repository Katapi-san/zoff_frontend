import requests
from bs4 import BeautifulSoup

URL = "https://www.zoff.co.jp/shop/contents/staff_list.aspx?gender=&keyword=&shop=&sort=pv&page=1"
resp = requests.get(URL)
soup = BeautifulSoup(resp.content, "html.parser")

classes = set()
for tag in soup.find_all(['li', 'div', 'ul']):
    if tag.get('class'):
        classes.update(tag.get('class'))

print("Classes found:", list(classes)[:50])

# Dump hierarchy for first few elements with class 'staff' something
staff_elements = soup.select("[class*='staff']")
print(f"Elements with 'staff' in class: {len(staff_elements)}")
for el in staff_elements[:5]:
    print(el.name, el.get('class'))
