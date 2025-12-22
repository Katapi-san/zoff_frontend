
import re
import os

def parse_html_staff():
    html_path = "staff_list.html"
    if not os.path.exists(html_path):
        print("staff_list.html not found.")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Try multiple Encodings if utf-8 fails or produces garbage? 
    # Usually Japanese sites are UTF-8 or Shift-JIS.
    # If the file read above worked, we process. If generic error, we retry.
    
    # Regex for staff block
    # Pattern likely: <p class="staffName">Name</p> ... <p class="shopName">Shop</p>
    # or similar structure. Let's list all text around "店" or known names.
    
    # Let's clean the HTML tags locally to see structure? No, simple regex first.
    
    # Look for patterns like:
    # <div class="staff_name">...</div>
    # <div class="staff_shop">...</div>
    
    # Since I don't know the exact class names, I will dump a snippet first.
    pass

def dump_sample():
    html_path = "staff_list.html"
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        with open(html_path, "r", encoding="shift_jis") as f:
            content = f.read()

    # Find "片田翔悟" in the content and print surroundings
    idx = content.find("片田翔悟")
    if idx != -1:
        print(content[idx-200:idx+200])
    else:
        print("Name not found in HTML.")
        # Print random snippet
        print(content[:500])

if __name__ == "__main__":
    dump_sample()
