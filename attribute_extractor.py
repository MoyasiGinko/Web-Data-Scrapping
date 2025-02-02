from bs4 import BeautifulSoup
from typing import List
import logging

logger = logging.getLogger(__name__)

class AttributeExtractor:
    def __init__(self, soup: BeautifulSoup):
        """
        Initialize the AttributeExtractor with a BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML
        """
        self.soup = soup

    def extract_attribute_values(self) -> List[str]:
        """
        Extract all data-attrib-val values from li elements with po-thumb-attribute class.

        Returns:
            List[str]: List of attribute values
        """
        try:
            # Find all li elements with class po-thumb-attribute
            attribute_elements = self.soup.find_all('li', class_='po-thumb-attribute')

            # Extract data-attrib-val values
            attributes = []
            for element in attribute_elements:
                attr_value = element.get('data-attrib-val')
                if attr_value:
                    attributes.append(attr_value)
                    # Log each found attribute
                    logger.info(f"Found attribute value: {attr_value}")

            # Log the total count
            # logger.info(f"Total attributes found: {len(attributes)}")
            return attributes

        except Exception as e:
            logger.error(f"Error extracting attribute values: {str(e)}")
            return []
