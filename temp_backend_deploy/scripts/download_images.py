import os
import requests

def download_image(url, filename):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.zoff.co.jp/"
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

images = {
    "ayako.jpg": "https://static.staff-start.com/img/staff/icon/388/1ae8c1230927306644490548d3c6577a-128778/34407bc3657b98d000b0e527d7042502.jpg",
    "triangle.jpg": "https://static.staff-start.com/img/staff/icon/388/1ae8c1230927306644490548d3c6577a-125041/14078877119293816766782348545806.jpg",
    "tsunakan.jpg": "https://static.staff-start.com/img/staff/icon/388/1ae8c1230927306644490548d3c6577a-128776/c36ca597f8ce9627c241f1f1e4e5d56a.jpg",
    "porin.jpg": "https://static.staff-start.com/img/staff/icon/388/1ae8c1230927306644490548d3c6577a-128780/c36ca597f8ce9627c241f1f1e4e5d56a.jpg"
}

output_dir = r"c:\Users\hkata\Documents\Tech0\PENTASCOPE（ペンタスコープ）\zoff-scope-root\apps\customer\public\images\staff"
os.makedirs(output_dir, exist_ok=True)

for name, url in images.items():
    download_image(url, os.path.join(output_dir, name))
