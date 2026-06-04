import pandas as pd
import os
import re
import shutil
import requests
from bs4 import BeautifulSoup
# Fresh output folder every run
if os.path.exists("output3"):
    shutil.rmtree("output3")

os.makedirs("output3")

# Read Excel
df = pd.read_excel("properties3.xlsx")

# Read template
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()


def slugify(text):
    text = str(text).lower().strip()

    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)

    return text.strip("-")


used_filenames = set()
def get_field(html, field_name):

    import re

    pattern = rf"{field_name}</td>\s*<td.*?>(.*?)</td>"

    match = re.search(
        pattern,
        html,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return ""

    value = match.group(1)

    value = re.sub("<.*?>", "", value)

    return value.strip()


def scrape_property(url):

    response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )

    html = response.text

    rent = get_field(
        html,
        "Rent Amount"
    )

    floors = get_field(
        html,
        "No. of Floors"
    )

    parking = get_field(
        html,
        "Car Park"
    )

    furnished = get_field(
        html,
        "Furnished"
    )

    power = get_field(
        html,
        "Power Supply"
    )

    lift = get_field(
        html,
        "Lift"
    )

    servant = get_field(
        html,
        "Servant Quarters"
    )

    water = get_field(
        html,
        "Water Facility"
    )

    return {
        "rent": rent,
        "floors": floors,
        "parking": parking,
        "furnished": furnished,
        "power": power,
        "lift": lift,
        "servant": servant,
        "water": water
    }
for _, row in df.iterrows():

    title = str(row["Address"]).strip()

    locality = str(row["Locality"]).strip()

    builtup_area = str(row["Built Up Area"]).strip()

    url = str(row["URL"]).strip()

    # Extract clean address/title
    address = title.split("|")[0].strip()

    # Extract property type
    property_type = "Commercial Property"

    if "for Rent at" in address:
        property_type = address.split("for Rent at")[0].strip()

    elif "For Rent at" in address:
        property_type = address.split("For Rent at")[0].strip()

    extra = scrape_property(url)

    # Handle empty values
    extra["rent"] = extra["rent"].strip() if extra["rent"] else ""
    extra["floors"] = extra["floors"].strip() if extra["floors"] else ""
    extra["parking"] = extra["parking"].strip() if extra["parking"] else ""
    extra["furnished"] = extra["furnished"].strip() if extra["furnished"] else ""
    extra["power"] = extra["power"].strip() if extra["power"] else ""
    extra["lift"] = extra["lift"].strip() if extra["lift"] else ""
    extra["servant"] = extra["servant"].strip() if extra["servant"] else ""
    extra["water"] = extra["water"].strip() if extra["water"] else ""

    # Replace blanks
    if not extra["rent"]:
        extra["rent"] = "Rent yet to be Updated"

    if not extra["floors"]:
        extra["floors"] = "Not Available"

    if not extra["parking"]:
        extra["parking"] = "Not Available"

    if not extra["furnished"]:
        extra["furnished"] = "Not Available"

    if not extra["power"]:
        extra["power"] = "Not Available"

    if not extra["lift"]:
        extra["lift"] = "Not Available"

    if not extra["servant"]:
        extra["servant"] = "Not Available"

    if not extra["water"]:
        extra["water"] = "Not Available"

    seo_title = (
        f"{property_type} for Rent in "
        f"{locality} Chennai | RentIt"
    )

    meta_description = (
        f"{property_type} available for rent in "
        f"{locality}, Chennai. "
        f"Built-up area {builtup_area}. "
        f"Monthly rent {extra['rent']}."
    )

    html = template

    html = html.replace(
        "{{PROPERTY_TYPE}}",
        property_type
    )

    html = html.replace(
        "{{LOCALITY}}",
        locality
    )

    html = html.replace(
        "{{BUILTUP_AREA}}",
        builtup_area
    )

    html = html.replace(
        "{{ADDRESS}}",
        address
    )

    html = html.replace(
        "{{SEO_TITLE}}",
        seo_title
    )

    html = html.replace(
        "{{META_DESCRIPTION}}",
        meta_description
    )

    rent_display = (
        f"{extra['rent']} / Month"
        if extra["rent"] != "Rent yet to be Updated"
        else "Rent yet to be Updated"
    )

    html = html.replace(
        "{{RENT}}",
        rent_display
    )

    html = html.replace(
        "{{FLOORS}}",
        extra["floors"]
    )

    html = html.replace(
        "{{PARKING}}",
        extra["parking"]
    )

    html = html.replace(
        "{{FURNISHED}}",
        extra["furnished"]
    )

    html = html.replace(
        "{{POWER}}",
        extra["power"]
    )

    html = html.replace(
        "{{LIFT}}",
        extra["lift"]
    )

    html = html.replace(
        "{{SERVANT}}",
        extra["servant"]
    )

    html = html.replace(
        "{{WATER}}",
        extra["water"]
    )

    # Remove residential placeholders
    html = html.replace("{{BEDROOMS}}", "N/A")
    html = html.replace("{{BATHROOMS}}", "N/A")

    filename = (
        f"{slugify(property_type)}-rent-"
        f"{slugify(locality)}.html"
    )

    original_filename = filename
    counter = 1

    while filename in used_filenames:
        filename = original_filename.replace(
            ".html",
            f"-{counter}.html"
        )
        counter += 1

    used_filenames.add(filename)

    output_path = os.path.join(
        "output3",
        filename
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    print(f"Generated: {filename}")
print("\nDone!")
print(f"Generated {len(df)} SEO pages.")