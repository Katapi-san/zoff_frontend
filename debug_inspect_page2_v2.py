
import re

def inspect_structure():
    path = "staff_list_page2.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find img tags that look like staff photos (/images/staff/...)
    # or just any img inside a list
    # The previous valid staff images were like "つなかん.jpeg".
    # Let's search for typical image extensions or keywords.
    # Actually, let's look for "img" tags and print their class or parent class.
    
    # regex for <img ... class="..." ...>
    imgs = re.findall(r'<img[^>]+class="([^"]+)"[^>]*>', content)
    print("Image classes found:")
    for c in set(imgs):
        print(c)
        
    # Search for "スタッフ" text to find the list container.
    idx = content.find("スタッフ")
    if idx != -1:
        print("\nContext around 'スタッフ':")
        print(content[idx:idx+200])

    # Search for any known staff name from Page 1 if Page 2 repeats structure?
    # Page 2 should have different names.
    # Let's dump all text inside <p> tags to see if we spot names.
    text_in_p = re.findall(r'<p[^>]*>(.*?)</p>', content)
    print("\nText in <p> tags (first 20):")
    for t in text_in_p[:20]:
        print(t)

if __name__ == "__main__":
    inspect_structure()
