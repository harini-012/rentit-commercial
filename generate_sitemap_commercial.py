import os
from datetime import date

domain = "https://rentit-seo-pages.onrender.com"
folder = "output3"

today = date.today().isoformat()

xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

for file in os.listdir(folder):

    if file.endswith(".html"):

        xml += f"""
<url>
    <loc>{domain}/{file}</loc>
    <lastmod>{today}</lastmod>
</url>
"""

xml += """
</urlset>
"""

with open(
    os.path.join(folder, "sitemap-commercial.xml"),
    "w",
    encoding="utf-8"
) as f:
    f.write(xml)

print("Commercial sitemap generated successfully!")
print(f"Saved as: {folder}/sitemap-commercial.xml")