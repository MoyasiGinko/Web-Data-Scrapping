import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl as px

# List of URLs to scrape
urls = [
    "https://mcshow.co.uk/project-yonder-ltd/project-yonder-ltd",
    "https://mcshow.co.uk/exhibitor-list/redline-campers",
    "https://mcshow.co.uk/exhibitor-list/rolling-homes-camper-ltd",
    "https://mcshow.co.uk/s-l-motorhomes/s-l-motorhomes",
    "https://mcshow.co.uk/sherwood-campers-ltd/sherwood-campers-ltd"
]

# Function to scrape data from each URL
def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data
        company_name = soup.find('h1').text.strip() if soup.find('h1') else "Not listed"
        website = soup.find('a', href=True, text="Website")['href'] if soup.find('a', href=True, text="Website") else "Not listed"
        industry = soup.find('p').text.strip() if soup.find('p') else "Industry information not available"

        # Set default values
        country = "UK"
        email_1 = "Not listed"
        email_2 = "Not listed"
        telephone = "Not listed"

        # Return scraped data as a dictionary
        return {
            "Company": company_name,
            "Website_Link": website,
            "Website Status": "Active",
            "Industry Specialized": industry,
            "Country": country,
            "Email 1": email_1,
            "Email 2": email_2,
            "Telephone": telephone
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {
            "Company": "Not listed",
            "Website_Link": "Not listed",
            "Website Status": "Not listed",
            "Industry Specialized": "Not listed",
            "Country": "Not listed",
            "Email 1": "Not listed",
            "Email 2": "Not listed",
            "Telephone": "Not listed"
        }

# Scrape each URL and store results
data = [scrape_data(url) for url in urls]

# Convert data to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel file
output_path = "company_details_mcshow.xlsx"
df.to_excel(output_path, index=False)

print(f"Data has been saved to {output_path}")
