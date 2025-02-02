from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class ColorExtractor:
    @staticmethod
    def extract_finish_options(url: str) -> List[str]:
        """
        Extract finish options from po-thumb-row.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the product page.

        Returns:
            List[str]: List of finish names.
        """
        try:
            # Set up Selenium WebDriver
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run in headless mode
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Open the webpage
            driver.get(url)

            # Find all <li> elements with data-attrib-name="finish"
            finish_elements = driver.find_elements(By.XPATH, '//li[@data-attrib-name="finish"]')

            # Extract data-attrib-val values
            finish_values = [element.get_attribute("data-attrib-val") for element in finish_elements]

            # logger.info(f"Extracted finish values from Selenium: {finish_values}")

            # Close the browser
            driver.quit()
            return finish_values

        except Exception as e:
            logger.error(f"Error extracting finish values using Selenium: {e}")
            return []


    @staticmethod
    def get_color_attributes(url: str) -> List[str]:
        """
        Extract color values (data-attrib-val) using Selenium.

        Args:
            url (str): URL of the webpage to scrape.

        Returns:
            List[str]: List of extracted color values.
        """
        try:
            # Set up Selenium WebDriver
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run in headless mode
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Open the webpage
            driver.get(url)

            # Find all <li> elements with data-attrib-name="color"
            color_elements = driver.find_elements(By.XPATH, '//li[@data-attrib-name="color"]')

            # Extract data-attrib-val values
            color_values = [element.get_attribute("data-attrib-val") for element in color_elements]

            # logger.info(f"Extracted color values from Selenium: {color_values}")

            # Close the browser
            driver.quit()
            return color_values

        except Exception as e:
            logger.error(f"Error extracting color values using Selenium: {e}")
            return []
