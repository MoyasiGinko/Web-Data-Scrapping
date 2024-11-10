import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read the URLs from the Excel file
input_file = "raw_links.xlsx"  # Path to the input Excel file with the URLs
df = pd.read_excel(input_file)

# Ensure the DataFrame has a column for the URLs (adjust this if necessary)
urls = df['import_links'].tolist()  # Assuming the column with URLs is named 'Exhibitor Page URL'

# Function to fetch the "Visit Website" link and website name
def fetch_website_info(url):
    try:
        # Send a GET request to the page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the "Visit Website" link
        visit_button = soup.find('a', class_='link link--primary', text='Visit website')
        website_url = visit_button.get('href') if visit_button else "Not available"

        # Extract the website name from the page header
        website_name_tag = soup.find('div', class_='page-header__meta').find('h2') if soup.find('div', class_='page-header__meta') else None
        website_name = website_name_tag.text.strip() if website_name_tag else "Not listed"

        # Return the extracted information
        return website_url, website_name
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return "Error", "Error"

# List to store the scraped data
data = []

# Loop through each URL and fetch the website link and name
for url in urls:
    website_url, website_name = fetch_website_info(url)
    data.append({
        "Exhibitor Page URL": url,
        "Visit Website Link": website_url,
        "Website Name": website_name
    })

# Convert the data to a pandas DataFrame
df_output = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_path = "scrapped_data/exhibitor_website_links.xlsx"
df_output.to_excel(output_path, index=False)

print(f"Website links and names have been saved to {output_path}")
