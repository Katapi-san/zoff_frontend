
import re

def find_staff_links():
    path = "staff_list_page2.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find matches for detail URLs
    # href="/shop/contents/staff_gallery_detail.aspx?cid=..."
    # or full URL
    
    matches = re.findall(r'href="([^"]*staff_[^"]*detail\.aspx[^"]*)"', content)
    print(f"Found {len(matches)} staff detail links.")
    for m in matches[:5]:
        print(m)
        
    # Now let's try to capture the block containing one of these links
    if matches:
        first_link = matches[0]
        # Find where this link is
        idx = content.find(first_link)
        # Print a large window around it to see the HTML structure
        start = max(0, idx - 1000)
        end = min(len(content), idx + 1000)
        print("\n--- Snippet ---")
        print(content[start:end])

if __name__ == "__main__":
    find_staff_links()
