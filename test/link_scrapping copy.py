import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of URLs to scrape
urls = [
    "https://mcshow.co.uk/project-yonder-ltd/project-yonder-ltd",
    "https://mcshow.co.uk/exhibitor-list/redline-campers",
    "https://mcshow.co.uk/exhibitor-list/rolling-homes-camper-ltd",
    "https://mcshow.co.uk/s-l-motorhomes/s-l-motorhomes",
    "https://mcshow.co.uk/sherwood-campers-ltd/sherwood-campers-ltd"
]

# Function to fetch the "Visit Website" link
def fetch_website_link(url):
    try:
        # Send a GET request to the page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the "Visit Website" link
        visit_button = soup.find('a', class_='link link--primary', text='Visit website')

        if visit_button:
            website_url = visit_button.get('href')
        else:
            website_url = "Not available"

        # Return the URL found
        return website_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return "Error"

# List to store the scraped data
data = []

# Loop through each URL and fetch the website link
for url in urls:
    website_url = fetch_website_link(url)
    data.append({
        "Exhibitor Page URL": url,
        "Visit Website Link": website_url
    })

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_path = "scrapped_data/exhibitor_website_links.xlsx"
df.to_excel(output_path, index=False)

print(f"Website links have been saved to {output_path}")
