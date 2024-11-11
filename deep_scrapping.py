import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urljoin

# Read the Excel file containing the website links
input_file = "scrapped_data/exhibitor_website_links.xlsx"
df = pd.read_excel(input_file)

# Function to extract contact details from a webpage (homepage or contact page)
async def extract_contact_details(url, session):
    try:
        # Simple User-Agent header to simulate a browser request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        # Send a GET request with the header
        async with session.get(url, headers=headers) as response:
            # Ensure the request was successful
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(await response.text(), 'html.parser')

            # Extract email addresses (look for 'mailto:')
            emails = []
            for tag in soup.find_all('a', href=True):
                if 'mailto:' in tag['href']:
                    email = tag['href'].replace('mailto:', '').strip()
                    emails.append(email)

            # Extract telephone numbers (look for 'tel:')
            phones = []
            for tag in soup.find_all('a', href=True):
                if 'tel:' in tag['href']:
                    phone = tag['href'].replace('tel:', '').strip()
                    phones.append(phone)

            return emails, phones

    except Exception as e:
        print(f"Error extracting contact details from {url}: {e}")
        return [], []

# Function to scrape details from each website
async def scrape_website_details(row, session):
    website_url = row["Visit Website Link"]
    exhibitor_page_url = row["Exhibitor Page URL"]

    contact_details = {"Email 1": "Not listed", "Email 2": "Not listed", "Telephone": "Not listed"}

    if website_url == "Not available" or website_url == "Error":
        return {
            "Exhibitor Page URL": exhibitor_page_url,
            "Website Name": "",
            "Industry Specialized": "",
            "Country": "UK",  # Assumed country
            **contact_details
        }

    # Extract the website name from the URL
    website_name = urlparse(website_url).netloc
    industry = "Not listed"  # Placeholder, update if you have a better way to extract this

    # Get contact details from the homepage
    emails, phones = await extract_contact_details(website_url, session)

    if emails:
        contact_details["Email 1"] = emails[0]
    if phones:
        contact_details["Telephone"] = phones[0]

    return {
        "Exhibitor Page URL": exhibitor_page_url,
        "Website Name": website_name,
        "Industry Specialized": industry,
        "Country": "UK",
        **contact_details
    }

# Main function to orchestrate scraping of multiple websites
async def main():
    async with aiohttp.ClientSession() as session:
        # List to store all scraped data
        scraped_data = []

        # Loop through each row in the DataFrame and scrape data asynchronously
        tasks = []
        for _, row in df.iterrows():
            tasks.append(scrape_website_details(row, session))

        # Wait for all tasks to complete and gather results
        scraped_data = await asyncio.gather(*tasks)

        # Convert the scraped data to a DataFrame
        scraped_df = pd.DataFrame(scraped_data)

        # Save the scraped data to a new Excel file
        output_file = "scrapped_data/scraped_exhibitor_details.xlsx"
        scraped_df.to_excel(output_file, index=False)

        print(f"Scraped data has been saved to {output_file}")

# Run the main function to start the scraping process
asyncio.run(main())
