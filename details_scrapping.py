import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

# Read the Excel file containing the website links
input_file = "scrapped_data/exhibitor_website_links.xlsx"
df = pd.read_excel(input_file)

# Function to extract website details (industry, email, telephone, etc.)
def scrape_website_details(website_url):
    try:
        # Send a GET request to the external website
        response = requests.get(website_url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract website name (domain)
        parsed_url = urlparse(website_url)
        website_name = parsed_url.netloc

        # Extract industry specialized (if available)
        industry = soup.find('p')  # Modify this based on actual HTML structure
        if industry:
            industry = industry.text.strip()
        else:
            industry = "Not listed"

        # Extract email addresses (simple regex approach)
        emails = []
        email_tags = soup.find_all('a', href=True)
        for tag in email_tags:
            href = tag['href']
            if 'mailto:' in href:
                emails.append(href.replace('mailto:', '').strip())

        # Extract telephone (simple search for phone numbers)
        telephone = "Not listed"
        phone_tags = soup.find_all('a', href=True)
        for tag in phone_tags:
            href = tag['href']
            if 'tel:' in href:
                telephone = href.replace('tel:', '').strip()
                break

        # Extract country (This can be hardcoded as "UK" if the exhibitor list is in the UK)
        country = "UK"

        # Return the scraped details
        return {
            "Website Name": website_name,
            "Industry Specialized": industry,
            "Country": country,
            "Email 1": emails[0] if emails else "Not listed",
            "Email 2": emails[1] if len(emails) > 1 else "Not listed",
            "Telephone": telephone
        }

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {website_url}: {e}")
        return None

# List to store the final scraped data
scraped_data = []

# Loop through each row in the DataFrame and scrape the details for each website
for index, row in df.iterrows():
    website_url = row["Visit Website Link"]

    # If there's no website link, we append the row with empty details
    if website_url == "Not available" or website_url == "Error":
        scraped_data.append({
            "Exhibitor Page URL": row["Exhibitor Page URL"],
            "Website Name": "",
            "Industry Specialized": "",
            "Country": "UK",  # Assumed country
            "Email 1": "",
            "Email 2": "",
            "Telephone": ""
        })
    else:
        # Otherwise, scrape the website details
        data = scrape_website_details(website_url)
        if data:
            scraped_data.append({
                "Exhibitor Page URL": row["Exhibitor Page URL"],
                **data
            })

# Convert the scraped data to a DataFrame
scraped_df = pd.DataFrame(scraped_data)

# Save the scraped data to a new Excel file
output_file = "scrapped_data/scraped_exhibitor_details.xlsx"
scraped_df.to_excel(output_file, index=False)

print(f"Scraped data has been saved to {output_file}")
