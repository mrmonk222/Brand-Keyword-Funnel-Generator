import os
import sys
from datetime import datetime

def load_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def generate_html(main_site, target_site, keyword, photo_url, output_dir):
    filename = f"{keyword.lower()}.html"
    filepath = os.path.join(output_dir, filename)

    short_desc = f"Grab your {keyword} laptop at special price this month!"
    if len(short_desc) > 150:
        short_desc = short_desc[:147] + "..."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="{short_desc}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buy NOW <a href="#" rel="nofollow">{keyword}</a> with special price this month</title>
</head>
<body>
    <h1>Buy NOW <a href="#" rel="nofollow">{keyword}</a> with special price this month</h1>
    <p>With <a href="{target_site}" rel="sponsored">{keyword}</a> you can purchase with special price and this good offers only valid for this month. 
    Grab your <a href="{target_site}" rel="sponsored">{keyword}</a> laptop now!</p>
    <img src="{photo_url}" alt="{keyword} laptop special offer">
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filename

def generate_sitemap(main_site, keywords, output_dir):
    sitemap_path = os.path.join(output_dir, "sitemap.xml")
    urls = [f"{main_site}/{kw.lower()}" for kw in keywords]

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f"  <url><loc>{url}</loc></url>\n"
    sitemap += "</urlset>"

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)

def main():
    if len(sys.argv) != 5:
        print("Usage: python main.py <main_site_url> <target_site_url> <brandlist.txt> <photolist.txt>")
        sys.exit(1)

    main_site = sys.argv[1].rstrip("/")
    target_site = sys.argv[2]
    brandlist_file = sys.argv[3]
    photolist_file = sys.argv[4]

    keywords = load_list(brandlist_file)
    photos = load_list(photolist_file)

    if len(keywords) != len(photos):
        print("Error: brandlist.txt and photolist.txt must have the same number of lines.")
        sys.exit(1)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for kw, photo in zip(keywords, photos):
        generate_html(main_site, target_site, kw, photo, output_dir)

    generate_sitemap(main_site, keywords, output_dir)
    print(f"Generated {len(keywords)} landing pages + sitemap.xml in '{output_dir}'")

if __name__ == "__main__":
    main()
