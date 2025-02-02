from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import logging
import re

logger = logging.getLogger(__name__)

class VariantExtractor:
    def __init__(self, soup: BeautifulSoup):
        """Initialize with BeautifulSoup object"""
        self.soup = soup

    def extract_variants(self) -> List[str]:
        """Extract all size values directly from size_value divs"""
        try:
            # Directly find all divs with class 'size_value'
            size_divs = self.soup.find_all('div', class_='size_value')

            # Extract and store the text from each div
            variants = [div.text.strip() for div in size_divs if div and div.text.strip()]

            # Debug print
            # print(f"Found {len(size_divs)} size divs")
            # print(f"Extracted variants: {variants}")

            return variants

        except Exception as e:
            logger.error(f"Error extracting variants: {str(e)}")
            print(f"Error while extracting variants: {str(e)}")
            return []

    def categorize_variants(self, variants: List[str]) -> Dict[str, List[str]]:
        """Categorize variants into different types"""
        try:
            categories = {
                'sizes': [],
                'voltages': [],
                'angles': [],
                'temperatures': [],
                'others': []
            }

            for variant in variants:
                variant = str(variant).strip()

                # Check sizes (patterns like 1", 1.5", 2.5")
                if re.search(r'^\d+\.?\d*”$', variant):
                    categories['sizes'].append(variant)

                # Check voltages (patterns like 120V, 240v)
                elif re.search(r'^\d+\.?\d*[vV]$', variant):
                    categories['voltages'].append(variant)

                # Check angles (patterns like 40°, 90°)
                elif re.search(r'^\d+\.?\d*°$', variant):
                    categories['angles'].append(variant)

                # Check temperatures (patterns like 1000K, 300k)
                elif re.search(r'^\d+\.?\d*[kK]$', variant):
                    categories['temperatures'].append(variant)

                # Check for only numbers (patterns like 100, 200)
                elif re.search(r'^\d+$', variant):
                    categories['numbers'].append(variant)

                # Check for with only alphabets (patterns like Small, Medium)
                elif re.search(r'^[a-zA-Z]+$', variant):
                    categories['words'].append(variant)

                # If no match found, add to others
                else:
                    categories['others'].append(variant)

            # Log the categorization results
            for category, items in categories.items():
                if items:  # Only log non-empty categories
                    logger.info(f"{category}: {items}")

            return categories

        except Exception as e:
            logger.error(f"Error categorizing variants: {str(e)}")
            return {
                'sizes': [],
                'voltages': [],
                'angles': [],
                'temperatures': [],
                'numbers': [],
                'words': [],
                'others': []
            }

    def get_categorized_variants(self) -> Dict[str, List[str]]:
        """Extract and categorize variants in one step"""
        variants = self.extract_variants()
        return self.categorize_variants(variants)