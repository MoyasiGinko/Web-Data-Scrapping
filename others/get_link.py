import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from each website URL
def get_website_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the name (found in the <strong> tag within the contact-body)
        name_tag = soup.find('div', class_='contact-body')
        name = name_tag.find('strong').text.strip() if name_tag else 'N/A'
        print(f"Name: {name}")  # Debugging print

        # Extract the contact number
        contact_number = None
        phone_icon_div = soup.find('div', class_='fa-phone')
        if phone_icon_div:
            contact_div = phone_icon_div.find_next('div', class_='contact-body')
            if contact_div:
                contact_p = contact_div.find('p')
                if contact_p:
                    contact_number = contact_p.text.strip().split("\n")[1].strip()
        print(f"Contact Number: {contact_number}")  # Debugging print

        # Extract the website link
        website_link = None
        globe_icon_div = soup.find('div', class_='fa-globe')
        if globe_icon_div:
            website_div = globe_icon_div.find_next('div', class_='contact-body')
            if website_div:
                # Find the <a> tag and extract the href attribute
                a_tag = website_div.find('a', href=True)
                if a_tag:
                    website_link = a_tag['href'].strip()  # Correctly extract the href
        print(f"Website Link: {website_link}")  # Debugging print

        return {
            'Name': name,
            'Contact Number': contact_number,
            'Website Link': website_link
        }

    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL {url}: {e}")
        return None

# Load URLs from an Excel file
input_file = 'raw_links.xlsx'  # Update file name if needed
df = pd.read_excel(input_file)

# Ensure URLs are in a column named 'import_links'
urls = df['import_links'].tolist()

# Collect the scraped data
scraped_data = []

# Iterate through each URL and scrape data
for url in urls:
    data = get_website_data(url)
    if data:
        scraped_data.append(data)

# Convert to DataFrame and save to Excel
scraped_df = pd.DataFrame(scraped_data)
scraped_df.to_excel('scraped_data.xlsx', index=False)

print("Scraping complete. Data saved to 'scraped_data.xlsx'.")
