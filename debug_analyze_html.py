
import re

def parse_staff_list():
    path = "staff_list_page2.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex attempts
    # Looking for structure: 
    # <p class="staffName">Name</p>
    # <p class="shopName">Shop</p>
    # <img src="...">
    
    # Let's try to extract anything that looks like a name inside a tag
    # or just dump typical classes
    
    # Try to find repetitive blocks
    # usually <li> ... </li>
    # Let's count <li>
    print(f"Total <li> tokens: {content.count('<li')}")
    
    # Find classes used in <p> or <div>
    classes = re.findall(r'class="([^"]+)"', content)
    from collections import Counter
    c = Counter(classes)
    print("Most common classes:")
    for k, v in c.most_common(20):
        print(f"{k}: {v}")
        
    # Search for specific potential keywords
    keywords = ["staffName", "staff_name", "shopName", "shop_name", "name", "shop", "ph_staff"]
    for k in keywords:
        if k in content:
            print(f"Found keyword details for '{k}':")
            # print surrounding
            pos = content.find(k)
            print(content[pos-50:pos+100])

if __name__ == "__main__":
    parse_staff_list()
