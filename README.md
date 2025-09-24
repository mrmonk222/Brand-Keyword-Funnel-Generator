# Brand / Keyword Funnel Generator

This tool generates SEO-friendly landing pages from a list of brands/keywords and images, plus a sitemap.

## Requirements
- Python 3.8+
- Virtual environment recommended

## Setup
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## USAGE
```
python main.py <main_site_url> <target_site_url> brandlist.txt photolist.txt
```

## Example:
```
python main.py https://laptop.com https://targetsite.com brandlist.txt photolist.txt
```

Output:
One HTML landing page per keyword
sitemap.xml file
