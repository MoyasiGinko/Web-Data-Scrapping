import requests
from bs4 import BeautifulSoup

# Function to search for the website URL of each company
def find_website(company_name):
    try:
        # Prepare the search query URL (this is for Google, but you can modify it for other search engines)
        search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}+website"

        # Send GET request to the search URL
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content of the search results
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first result link (this may vary based on the structure of the search engine page)
        link = soup.find('a', href=True)

        # If a valid link is found, return it
        if link:
            website_link = link['href']
            # Filtering out unwanted Google redirects
            if 'url?q=' in website_link:
                website_link = website_link.split('url?q=')[1].split('&')[0]
            return website_link
        else:
            return None
    except Exception as e:
        print(f"Error finding website for {company_name}: {e}")
        return None

# List of company names
companies = [
    "TRADERSTON FZE", "KARMICA GLOBAL", "AL AYDI TENTS AND METAL INDUSTRY", "CAR PARKING SHADES & TENTS",
    "AL BADAYER RETREAT", "KINGFISHER RETREAT", "BHARAT TENT MANUFACTURERS", "AYANCHEM FZE",
    "AL AMEERA TENTS & SHADES", "APM SHADES", "AL FARES INTERNATIONAL TENTS", "BAIT AL MALAKI TENTS AND SHADES",
    "AZIRA INTERNATIONAL", "UMAIR TENTS & SHADES 00971557781265", "ARASCA MEDICAL EQUIPMENT TRADING LLC",
    "ABDUL JABBAR GENERAL CONTRACTING LLC", "BAIT AL NOKHADA TENTS & FABRIC SHADE LLC", "LINK MIDDLE EAST LTD",
    "ROYAL SHADE LLC", "ACE CENTRO ENTERPRISES", "EXCEL TRADING LLC (OPC)", "DOORS & SHADE SYSTEMS",
    "SPARK TECHNICAL SUPPLIES FZE", "GULF SAFETY EQUIPS TRADING LLC", "JAVED TENTS", "DALAIL AL KHAIR TENTS"
]

# Search and collect websites
websites = {}
for company in companies:
    website = find_website(company)
    if website:
        websites[company] = website

# Print the results
for company, website in websites.items():
    print(f"{company}: {website}")
