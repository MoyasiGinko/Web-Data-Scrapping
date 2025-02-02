import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import logging
from typing import List, Dict, Optional, Union
from urllib.parse import urlparse
from color_extractor import ColorExtractor
from variant_extractor import VariantExtractor
from attribute_extractor import AttributeExtractor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AdvancedProductScraper:
    def __init__(self):
        self.driver = self._setup_selenium_driver()
        self.wait = WebDriverWait(self.driver, 10)
        # Define the exact order of columns
        self.columns = [
            'Who did it',
            'Length of entry',
            'Products Url',
            'Handle',
            'Title',
            'Variant Metafield: details.description [multi_line_text_field]',
            'Vendor',
            'Option2 Name',
            'Option2 Value',
            'Option3 Name',
            'Option3 Value',
            'Option4 Name',
            'Option4 Value',
            'Variant Metafield: vendor.part_number [single_line_text_field]',
            'Variant Price',
            'Variant Compare At Price',
            'Image Src',
            'Variant Metafield: variant.dimensions [single_line_text_field]',
            'Variant Metafield: variant.weight [single_line_text_field]',
            'Variant Metafield: variant.finish [single_line_text_field]',
            'Variant Metafield: variant.bulbs_number [single_line_text_field]',
            'Variant Metafield: variant.bulbs_type [single_line_text_field]',
            'Variant Metafield: variant.bulbs_base [single_line_text_field]',
            'Variant Metafield: variant.max_wattage [single_line_text_field]',
            'Variant Metafield: variant.bulbs_included [single_line_text_field]',
            'Variant Metafield: variant.bulbs_dimmable [single_line_text_field]',
            'Variant Metafield: variant.width [single_line_text_field]',
            'Variant Metafield: variant.height [single_line_text_field]',
            'Variant Metafield: variant.length [single_line_text_field]',
            'Variant Metafield: variant.width_range [single_line_text_field]',
            'Variant Metafield: variant.height_range [single_line_text_field]',
            'Image Src 1',
            'Image Src 2',
            'Image Src 3',
            'Image Src 4'
        ]

    def _setup_selenium_driver(self):
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

    def _safe_find_element(self, by: By, value: str, default: str = 'N/A') -> str:
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            return element.text.strip() or default
        except (TimeoutException, NoSuchElementException):
            return default

    def _get_field_value(self, soup: BeautifulSoup, field_name: str) -> str:
        """Centralized method to get field values based on field name"""
        field_selectors = {
            # Basic Information
            'Title': {'selector': 'h1.product-title, div.product-name', 'attr': 'text'},
            'Handle': {'selector': 'link[rel="canonical"]', 'attr': 'href'},
            'Vendor': {'selector': 'div.vendor-name, a.vendor-link', 'attr': 'text'},

            # Description and Part Number
            'Variant Metafield: details.description [multi_line_text_field]': {
                'selector': 'div.product-description, div[data-product-description]',
                'attr': 'text'
            },
            'Variant Metafield: vendor.part_number [single_line_text_field]': {
                'selector': 'div.part-number, span[data-part-number]',
                'attr': 'data-value'
            },

            # Pricing
            'Variant Price': {'selector': 'span.price, [data-product-price]', 'attr': 'text'},
            'Variant Compare At Price': {'selector': 'span.compare-price', 'attr': 'text'},

            # Dimensions and Physical Attributes
            'Variant Metafield: variant.dimensions [single_line_text_field]': {
                'selector': 'div.dimensions, [data-dimensions]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.weight [single_line_text_field]': {
                'selector': 'div.weight, [data-weight]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.width [single_line_text_field]': {
                'selector': 'div.width, [data-width]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.height [single_line_text_field]': {
                'selector': 'div.height, [data-height]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.length [single_line_text_field]': {
                'selector': 'div.length, [data-length]',
                'attr': 'data-value'
            },

            # Range Measurements
            'Variant Metafield: variant.width_range [single_line_text_field]': {
                'selector': 'div.width-range, [data-width-range]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.height_range [single_line_text_field]': {
                'selector': 'div.height-range, [data-height-range]',
                'attr': 'data-value'
            },

            # Bulb Details
            'Variant Metafield: variant.bulbs_number [single_line_text_field]': {
                'selector': 'div.bulb-count, [data-bulb-count]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.bulbs_type [single_line_text_field]': {
                'selector': 'div.bulb-type, [data-bulb-type]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.bulbs_base [single_line_text_field]': {
                'selector': 'div.bulb-base, [data-bulb-base]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.max_wattage [single_line_text_field]': {
                'selector': 'div.max-wattage, [data-wattage]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.bulbs_included [single_line_text_field]': {
                'selector': 'div.bulbs-included, [data-bulbs-included]',
                'attr': 'data-value'
            },
            'Variant Metafield: variant.bulbs_dimmable [single_line_text_field]': {
                'selector': 'div.dimmable, [data-dimmable]',
                'attr': 'data-value'
            },

            # Finish
            'Variant Metafield: variant.finish [single_line_text_field]': {
                'selector': 'div.finish, [data-finish]',
                'attr': 'data-value'
            }
        }

        if field_name not in field_selectors:
            return 'N/A'

        selector_info = field_selectors[field_name]
        element = soup.select_one(selector_info['selector'])

        if not element:
            return 'N/A'

        if selector_info['attr'] == 'text':
            return element.text.strip()
        else:
            return element.get(selector_info['attr'], 'N/A')

    def _get_options(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract options 2-4 with names and values"""
        options = {}
        for i in range(2, 5):
            option_container = soup.find('div', {'product-option-title': str(i)})
            if option_container:
                name = option_container.find('h2')
                value = option_container.find('select') or option_container.find('input')
                options[f'Option{i} Name'] = name.text.strip() if name else 'N/A'
                options[f'Option{i} Value'] = value.get('value', 'N/A') if value else 'N/A'
            else:
                options[f'Option{i} Name'] = 'N/A'
                options[f'Option{i} Value'] = 'N/A'
        return options

    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract all product images"""
        images = []
        image_elements = soup.find_all('img', class_=re.compile(r'product-image|gallery-image'))
        for img in image_elements:
            src = img.get('src', img.get('data-src', ''))
            if src and src not in images:
                images.append(src)

        # Ensure we have exactly 5 image slots (main + 4 additional)
        while len(images) < 5:
            images.append('N/A')

        return images

    def scrape_product_details(self, url: str) -> List[Dict]:
        try:
            self.driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')


            # Log color options
            color_extractor = ColorExtractor()
            finish = color_extractor.extract_finish_options(url)
            color_atr = color_extractor.get_color_attributes(url)
            # logger.info(f"Finish found for {url}: {finish}")
            # logger.info(f"Color attributes found: {color_atr}")


            # Create an instance
            extractor = VariantExtractor(soup)

            # Method 1: Two-step process
            variants = extractor.extract_variants()
            categories = extractor.categorize_variants(variants)

            # Method 2: One-step process
            categories = extractor.get_categorized_variants()



            attribute_extractor = AttributeExtractor(soup)
            # Get all attribute values
            attributes = attribute_extractor.extract_attribute_values()
            # logger.info(f"All attribute values found: {attributes}")

            # Access specific categories
            print("==================START===================")
            print("URL:", url)
            print("Finish Options:", finish)
            print("Color Attributes:", color_atr)
            print("Attributes:", attributes)
            print("Sizes:", categories['sizes'])
            print("Voltages:", categories['voltages'])
            print("Angles:", categories['angles'])
            print("Temperatures:", categories['temperatures'])
            print("Numbers:", categories['numbers'])
            print("Words:", categories['words'])
            print("Others:", categories['others'])
            print("==================END===================")



            # variant_extractor = VariantExtractor(soup)
            # variants = variant_extractor.extract_variants()
            # logger.info(f"Variants found for {url}: {variants}")


            # Rest of your existing scraping code...
            product_details = {
                'Who did it': 'Moyasi',
                'Length of entry': 'medium',
                'Products Url': url
            }

            # Get all field values using the centralized method
            for field in self.columns:
                if field not in ['Who did it', 'Length of entry', 'Products Url']:
                    if 'Image Src' in field:
                        continue
                    product_details[field] = self._get_field_value(soup, field)

            # Handle images
            images = self._extract_images(soup)
            product_details['Image Src'] = images[0]
            for i in range(1, 5):
                product_details[f'Image Src {i}'] = images[i]

            # Get options
            options = self._get_options(soup)
            product_details.update(options)

            # Ensure all columns are present and in correct order
            ordered_details = {column: product_details.get(column, 'N/A') for column in self.columns}

            return [ordered_details]

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []

    def scrape_multiple_products(self, input_file: str, output_file: str):
        try:
            df_input = pd.read_excel(input_file)
            all_products = []

            for url in df_input['URL']:
                logger.info(f"Scraping: {url}")
                products = self.scrape_product_details(url)
                all_products.extend(products)
                time.sleep(2)

            df_output = pd.DataFrame(all_products, columns=self.columns)
            df_output.to_excel(output_file, index=False)
            logger.info(f"Data saved to {output_file}")

        except Exception as e:
            logger.error(f"Process error: {e}")
        finally:
            self.driver.quit()

def main():
    scraper = AdvancedProductScraper()
    scraper.scrape_multiple_products('product_urls.xlsx', 'scraped_product_details.xlsx')

if __name__ == "__main__":
    main()