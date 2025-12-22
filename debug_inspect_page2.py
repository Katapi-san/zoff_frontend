
import os

def dump_html_snippet():
    path = "staff_list_page2.html"
    if not os.path.exists(path):
        print("File not found")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Look for common staff list markers
    # e.g. "staff_name", "staffName", "shop_name"
    # Or just find a known staff name if we knew one.
    # Page 2 content... I don't know names.
    # Let's search for "class=" to find container.
    
    # Let's print a chunk around "staff"
    idx = content.find("staff")
    if idx != -1:
        print(content[idx:idx+500])
    
    # Also look for image tag structure
    print("-" * 20)
    idx2 = content.find("<img")
    if idx2 != -1:
         print(content[idx2:idx2+500])

if __name__ == "__main__":
    dump_html_snippet()
