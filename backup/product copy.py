import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import itertools
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AdvancedProductScraper:
    def __init__(self):
        """Initialize the web scraper with Selenium WebDriver"""
        self.driver = self._setup_selenium_driver()

    def _setup_selenium_driver(self):
        """Set up Chrome WebDriver with advanced bot detection bypass"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)

        return driver

    def _extract_comprehensive_variants(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Intelligent and dynamic variant extraction
        Extracts all possible variant parameters
        """
        variant_params = {
            'Color': [],
            'Color Temperature': [],
            'Finish': [],
            'Size': [],
            'Width': [],
            'Height': [],
            'Length': [],
            'Glass': [],
            'Crystal': []
        }

        # Comprehensive variant parameter detection
        variant_mappings = [
            ('Color', ['color', 'variant-color', 'dyn_color_name']),
            ('Color Temperature', ['color-temp', 'temperature', 'dyn_prod_lamp_kelvin']),
            ('Finish', ['finish', 'variant-finish', 'dyn_finish_name']),
            ('Size', ['size', 'variant-size']),
            ('Width', ['width', 'dyn_prod_width']),
            ('Height', ['height', 'dyn_prod_height']),
            ('Length', ['length', 'dyn_prod_length']),
            ('Glass', ['glass', 'variant-glass']),
            ('Crystal', ['crystal', 'variant-crystal'])
        ]

        # Intelligent variant detection
        for param_name, class_patterns in variant_mappings:
            for pattern in class_patterns:
                elements = soup.find_all(['div', 'span'], class_=re.compile(pattern))
                values = [
                    elem.get('data-value', elem.text.strip())
                    for elem in elements
                    if elem.get('data-value') or elem.text.strip()
                ]

                if values:
                    variant_params[param_name].extend(values)
                    break

        # Remove duplicates and clean parameters
        for key in variant_params:
            variant_params[key] = list(dict.fromkeys(variant_params[key]))

        # Generate all possible variant combinations
        variant_keys = [k for k, v in variant_params.items() if v]
        variant_values = [variant_params[key] for key in variant_keys]

        variants = [
            dict(zip(variant_keys, combination))
            for combination in itertools.product(*variant_values)
        ]

        return variants if variants else [{}]

    def _determine_entry_length(self, variant_count):
        """Determine entry length based on variant count"""
        if variant_count <= 7:
            return 'small'
        elif variant_count <= 15:
            return 'medium'
        else:
            return 'large'

    def scrape_product_details(self, url: str) -> List[Dict]:
        """
        Comprehensive product details scraping with intelligent variant handling
        """
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'dyn_prod_name'))
            )
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Base product details
            base_details = {
                'Who did it': 'Moyasi',
                'Products Url': url,
                'Title': soup.find('h1', class_='dyn_prod_name').text.strip() if soup.find('h1', class_='dyn_prod_name') else 'N/A',
                'Vendor': soup.find('a', class_='vendor-name').text.strip() if soup.find('a', class_='vendor-name') else 'N/A'
            }

            # Extract comprehensive variants
            variants = self._extract_comprehensive_variants(soup)

            # Determine entry length
            base_details['Length of entry'] = self._determine_entry_length(len(variants))

            # Detailed products with variants
            detailed_products = []

            for variant in variants:
                product_variant = base_details.copy()
                product_variant.update(variant)

                # Populate variant-specific details
                metadata_mappings = {
                    'Variant Metafield: variant.color [single_line_text_field]': variant.get('Color', 'N/A'),
                    'Variant Metafield: variant.cct [single_line_text_field]': variant.get('Color Temperature', 'N/A'),
                    'Variant Metafield: variant.finish [single_line_text_field]': variant.get('Finish', 'N/A'),
                    'Variant Metafield: variant.width [single_line_text_field]': variant.get('Width', 'N/A'),
                    'Variant Metafield: variant.height [single_line_text_field]': variant.get('Height', 'N/A'),
                    'Variant Metafield: variant.length [single_line_text_field]': variant.get('Length', 'N/A'),
                    'Variant Metafield: variant.glass [single_line_text_field]': variant.get('Glass', 'N/A'),
                    'Variant Metafield: variant.crystal [single_line_text_field]': variant.get('Crystal', 'N/A')
                }
                product_variant.update(metadata_mappings)

                detailed_products.append(product_variant)

            return detailed_products

        except Exception as e:
            logger.error(f"Scraping error for {url}: {e}")
            return []

    def scrape_multiple_products(self, input_file: str, output_file: str):
        """
        Scrape multiple products from an input Excel file
        """
        try:
            df_input = pd.read_excel(input_file)
            all_products = []

            for url in df_input['URL']:
                logger.info(f"Scraping: {url}")
                products = self.scrape_product_details(url)
                all_products.extend(products)
                time.sleep(2)

            df_output = pd.DataFrame(all_products)
            df_output.to_excel(output_file, index=False)
            logger.info(f"Scraped data saved to {output_file}")

        except Exception as e:
            logger.error(f"Scraping process error: {e}")
        finally:
            self.driver.quit()

def main():
    scraper = AdvancedProductScraper()
    scraper.scrape_multiple_products('product_urls.xlsx', 'scraped_product_details.xlsx')

if __name__ == "__main__":
    main()