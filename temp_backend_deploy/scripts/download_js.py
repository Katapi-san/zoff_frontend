import requests

url = "https://www.zoff.co.jp/pages/staff_gallery/ver1.0.0/js/staff_list/staff_list.js"
try:
    response = requests.get(url, timeout=10)
    response.encoding = 'utf-8' # JS is likely UTF-8
    with open("staff_list.js", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Saved staff_list.js")
except Exception as e:
    print(f"Error: {e}")
