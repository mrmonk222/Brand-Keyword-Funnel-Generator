"""
Brand / Keyword Funneling Static Landing Page Generator
------------------------------------------------------
- Reads `brandlist.txt` (one keyword per line) and `photolist.txt` (one image URL per line).
- User only needs to input: MAIN_SITE_URL and TARGET_SITE_URL at the top.
- For each keyword (line i) it creates a landing page `output/<slug>.html` using an HTML template.
- Each keyword is paired with photo line i (if photos shorter, loop them).
- Generates `output/sitemap.xml` with <loc>MAIN_SITE_URL/slug</loc>

Usage:
1. Put this script in the same folder as `brandlist.txt` and `photolist.txt`.
2. Set MAIN_SITE_URL and TARGET_SITE_URL below.
3. Run: python3 brand_keyword_funnel_generator.py
4. Output in ./output/ (HTML files + sitemap.xml)
"""

import os
import re
import html
from urllib.parse import quote

MAIN_SITE_URL = "https://laptop.com"   # main domain
TARGET_SITE_URL = "https://target.com"  # external target site for sponsored links
WORDLIST = "brandlist.txt"
PHOTOS = "photolist.txt"
OUTPUT_DIR = "output"

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s)
    return s or "keyword"

def read_lines(filename: str) -> list:
    if not os.path.isfile(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

HTML_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>$TITLE</title>
  <meta name="description" content="$DESCRIPTION" />
  <link rel="canonical" href="$MAIN_URL/$SLUG" />
  <style>
    body{font-family:Arial,sans-serif;margin:0;padding:0;background:#f8f8f8}
    .wrap{max-width:900px;margin:24px auto;padding:20px;background:#fff;border-radius:8px;box-shadow:0 4px 10px rgba(0,0,0,0.1)}
    .product{display:grid;grid-template-columns:1fr 300px;gap:20px}
    .product img{width:100%;height:auto;border-radius:6px}
    h1{margin:0 0 12px;font-size:22px}
    p{line-height:1.5}
    .cta{display:inline-block;margin-top:15px;padding:12px 20px;border-radius:6px;background:#0077cc;color:#fff;text-decoration:none}
    @media(max-width:700px){.product{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <main class="wrap">
    <article class="product">
      <section>
        <h1>$TITLE</h1>
        <p>$DESCRIPTION</p>
        <a class="cta" href="$MAIN_URL/$SLUG">Buy $KEYWORD Now</a>
      </section>
      <aside>
        <img src="$IMAGE" alt="$ALT_TEXT" loading="lazy"/>
      </aside>
    </article>
  </main>
</body>
</html>'''

def make_page(keyword: str, image: str) -> tuple:
    safe_keyword = html.escape(keyword)
    slug = slugify(keyword)
    title = f"Buy NOW <a href=\"#\" rel=\"nofollow\">{safe_keyword}</a> with special price this month"
    description = (f"With <a href=\"{TARGET_SITE_URL}\" rel=\"sponsored\">{safe_keyword}</a> you can purchase with special price "
                   f"and this good offers only valid for this month. Grab your <a href=\"{TARGET_SITE_URL}\" rel=\"sponsored\">{safe_keyword}</a> laptop now!")
    alt_text = f"{safe_keyword} laptop special offer"
    content = HTML_TEMPLATE.replace("$TITLE", title)
    content = content.replace("$DESCRIPTION", description)
    content = content.replace("$IMAGE", image)
    content = content.replace("$KEYWORD", safe_keyword)
    content = content.replace("$SLUG", slug)
    content = content.replace("$MAIN_URL", MAIN_SITE_URL)
    content = content.replace("$ALT_TEXT", alt_text)
    return slug, content

def build_all():
    keywords = read_lines(WORDLIST)
    photos = read_lines(PHOTOS)
    if not keywords:
        print(f"ERROR: No keywords in {WORDLIST}")
        return
    if not photos:
        print(f"WARNING: No photos in {PHOTOS}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    sitemap_lines = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
    ]

    for i, kw in enumerate(keywords):
        photo = photos[i % len(photos)] if photos else ""
        slug, page_html = make_page(kw, photo)
        filename = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page_html)
        full_url = f"{MAIN_SITE_URL}/{quote(slug)}"
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{full_url}</loc>")
        sitemap_lines.append("  </url>")
        print(f"Generated: {filename}")

    sitemap_lines.append("</urlset>")
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as sf:
        sf.write("\n".join(sitemap_lines))
    print("Sitemap generated.")

if __name__ == '__main__':
    build_all()
