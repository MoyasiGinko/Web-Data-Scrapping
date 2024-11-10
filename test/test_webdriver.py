import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# List of URLs to scrape
urls = [
    "https://mcshow.co.uk/project-yonder-ltd/project-yonder-ltd",
    "https://mcshow.co.uk/exhibitor-list/redline-campers",
    "https://mcshow.co.uk/exhibitor-list/rolling-homes-camper-ltd",
    "https://mcshow.co.uk/s-l-motorhomes/s-l-motorhomes",
    "https://mcshow.co.uk/sherwood-campers-ltd/sherwood-campers-ltd"
]

# Function to scrape data from the external website
def scrape_external_website(website_url):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")

        # Initialize WebDriver with options
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(website_url)

        # Wait for the page to load
        time.sleep(2)

        # Scrape required data
        company_name = driver.find_element(By.TAG_NAME, 'h1').text if driver.find_elements(By.TAG_NAME, 'h1') else "Not listed"
        industry = driver.find_element(By.TAG_NAME, 'p').text if driver.find_elements(By.TAG_NAME, 'p') else "Industry information not available"
        email_1 = "Not listed"  # Email extraction logic to be added
        email_2 = "Not listed"  # Email extraction logic to be added
        telephone = "Not listed"  # Telephone extraction logic to be added
        website = website_url

        # Return the scraped data
        return {
            "Company": company_name,
            "Website_Link": website,
            "Website Status": "Active",
            "Industry Specialized": industry,
            "Country": "UK",
            "Email 1": email_1,
            "Email 2": email_2,
            "Telephone": telephone
        }
    except Exception as e:
        print(f"Error scraping website {website_url}: {e}")
        return None
    finally:
        driver.quit()

# Function to scrape data from exhibitor list pages
def scrape_data(url):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")

        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Find the "Visit Website" link
        try:
            visit_button = driver.find_element(By.XPATH, "//a[@class='link link--primary' and text()='Visit website']")
            website_url = visit_button.get_attribute("href")
        except Exception as e:
            print(f"Visit website link not found for {url}: {e}")
            driver.quit()
            return None

        # Now, visit the external website and scrape the data
        data = scrape_external_website(website_url)

        driver.quit()
        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Scrape each URL and store results
data = []
for url in urls:
    result = scrape_data(url)
    if result:
        data.append(result)

# Convert data to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel file
output_path = "company_details_mcshow.xlsx"
df.to_excel(output_path, index=False)

print(f"Data has been saved to {output_path}")
