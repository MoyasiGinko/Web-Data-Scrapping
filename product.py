import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json
import time
import logging
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ProductScraper:
    def __init__(self):
        self.driver = self._setup_selenium_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.all_products = []

    def _setup_selenium_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver

    def extract_variants_from_soup(self, soup):
        try:
            # Find all divs with size_value class
            size_divs = soup.find_all('div', class_='size_value')
            variants = [div.text.strip() for div in size_divs if div and div.text.strip()]

            # Categorize the variants
            categories = {
                'sizes': [],
                'voltages': [],
                'angles': [],
                'temperatures': [],
                'numbers': [],
                'words': [],
                'others': []
            }

            import re
            for variant in variants:
                if re.search(r'\d+\.?\d*”', variant):
                    categories['sizes'].append(variant)
                elif re.search(r'\d+\.?\d*[vV]', variant):
                    categories['voltages'].append(variant)
                elif re.search(r'\d+\.?\d*°', variant):
                    categories['angles'].append(variant)
                elif re.search(r'\d+\.?\d*[kK]', variant):
                    categories['temperatures'].append(variant)
                elif variant.isdigit():
                    categories['numbers'].append(variant)
                elif variant.isalpha():
                    categories['words'].append(variant)
                else:
                    categories['others'].append(variant)

            return categories
        except Exception as e:
            logger.error(f"Error extracting variants: {e}")
            return {
                'sizes': [],
                'voltages': [],
                'angles': [],
                'temperatures': [],
                'numbers': [],
                'words': [],
                'others': []
            }

    def extract_attributes(self, soup):
        try:
            attribute_elements = soup.find_all('li', class_='po-thumb-attribute')
            return [elem.get('data-attrib-val') for elem in attribute_elements if elem.get('data-attrib-val')]
        except Exception as e:
            logger.error(f"Error extracting attributes: {e}")
            return []

    def extract_finish_and_colors(self, soup):
        try:
            finish_elements = soup.find_all('li', attrs={'data-attrib-name': 'finish'})
            color_elements = soup.find_all('li', attrs={'data-attrib-name': 'color'})

            finishes = [elem.get('data-attrib-val') for elem in finish_elements if elem.get('data-attrib-val')]
            colors = [elem.get('data-attrib-val') for elem in color_elements if elem.get('data-attrib-val')]

            return finishes, colors
        except Exception as e:
            logger.error(f"Error extracting finishes and colors: {e}")
            return [], []

    def scrape_product(self, url, product_id):
        try:
            self.driver.get(url)
            time.sleep(3)  # Increased wait time
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Extract all data using the soup object
            finishes, colors = self.extract_finish_and_colors(soup)
            categories = self.extract_variants_from_soup(soup)
            attributes = self.extract_attributes(soup)

            product_data = {
                'product_id': product_id,
                'url': url,
                'finish_options': finishes,
                'color_attributes': colors,
                'attributes': attributes,
                'categories': categories
            }

            self.all_products.append(product_data)

            # Print the data
            print("==================START===================")
            print("URL:", url)
            print("Finish Options:", finishes)
            print("Color Attributes:", colors)
            print("Attributes:", attributes)
            for category, items in categories.items():
                print(f"{category.capitalize()}:", items)
            print("==================END===================")

            return product_data

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    def scrape_all_products(self, input_file):
        try:
            df = pd.read_excel(input_file)

            for index, row in df.iterrows():
                product_id = index + 1
                url = row['URL']
                logger.info(f"Scraping product {product_id}: {url}")
                self.scrape_product(url, product_id)
                time.sleep(2)

            # Save all products to a single JSON file
            with open('all_products.json', 'w', encoding='utf-8') as f:
                json.dump(self.all_products, f, indent=4, ensure_ascii=False)

            logger.info("All products data saved to all_products.json")

        except Exception as e:
            logger.error(f"Process error: {e}")
        finally:
            self.driver.quit()

def main():
    scraper = ProductScraper()
    scraper.scrape_all_products('product_urls.xlsx')

if __name__ == "__main__":
    main()