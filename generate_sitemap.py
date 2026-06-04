import os

domain = "https://rentit-seo-pages.onrender.com"

folder = "output"

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

for file in os.listdir(folder):

    if file.endswith(".html"):

        xml += f"""
<url>
<loc>{domain}/{file}</loc>
</url>
"""

xml += "\n</urlset>"

with open(
    "output/sitemap.xml",
    "w",
    encoding="utf-8"
) as f:
    f.write(xml)

print("Sitemap Generated")