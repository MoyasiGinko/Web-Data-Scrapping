import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Define the URL of the webpage to scrape
url = "https://www.yellowpages-uae.com/uae/prefabricated-houses"

# Send an HTTP request to get the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Create a new Excel workbook and sheet
wb = Workbook()
ws = wb.active
ws.title = "Website Data"

# Write the header row for the Excel sheet
headers = ["Company Name", "Location", "City", "P.O Box", "Phone", "Mobile", "Website", "Products/Services"]
ws.append(headers)

# Find all the cards containing the required information
# Assuming all cards are wrapped in a div with a certain class (you will adjust this according to actual HTML)
cards = soup.find_all('div', class_='flex flex-grow flex-col w-full')  # Change class name as needed

# Loop through each card and extract the relevant data
for card in cards:
    # Extract company name (title)
    company_name = card.find('a', title=True).get_text(strip=True)

    # Extract location, city, and P.O. Box
    location = card.find('p', string="Location : ").find_next('span').get_text(strip=True) if card.find('p', string="Location : ") else "N/A"
    city = card.find('span', string="City : ").find_next('span').get_text(strip=True) if card.find('span', string="City : ") else "N/A"
    po_box = card.find('span', string="P.O Box : ").find_next('span').get_text(strip=True) if card.find('span', string="P.O Box : ") else "N/A"

    # Extract phone number from the href attribute
    phone = card.find('a', href=True, title="Click to call", id=lambda x: x and x.startswith('lblPhone'))
    phone_number = phone['href'].replace('tel:', '') if phone else "N/A"

    # Extract mobile number from the href attribute
    mobile = card.find('a', href=True, title="Click to call", id=lambda x: x and x.startswith('lblMobile'))
    mobile_number = mobile['href'].replace('tel:', '') if mobile else "N/A"

    # Extract website URL
    website = card.find('button', class_='listing_button')["data-url"] if card.find('button', class_='listing_button') else "N/A"

    # Extract products/services
    services = ", ".join([a.get_text(strip=True) for a in card.find_all('a', class_='font-bold')])

    # Write the extracted data to the Excel sheet
    row = [company_name, location, city, po_box, phone_number, mobile_number, website, services]
    ws.append(row)

# Save the Excel file
wb.save("company_data.xlsx")

print("Data scraping and saving to Excel completed.")
