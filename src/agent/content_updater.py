from typing import Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
import logging
from src.config.settings import API_KEY

logger = logging.getLogger(__name__)

class ContentUpdater:
    def __init__(self):
        self.api_key = API_KEY
        self.cache = {}  # Simple cache for API responses

    def fetch_updated_data(self, api_endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Fetch updated data from external API."""
        try:
            # Check cache first
            cache_key = f"{api_endpoint}:{str(params)}"
            if cache_key in self.cache:
                return self.cache[cache_key]

            response = requests.get(
                api_endpoint,
                params=params,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
            self.cache[cache_key] = data
            return data
        except Exception as e:
            logger.error(f"Error fetching data from API: {str(e)}")
            return None

    def update_content(self, html_content: str, updates: Dict[str, Any]) -> str:
        """Update webpage content with new data."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Update prices
            for price_element in soup.find_all(class_='price'):
                product_id = price_element.get('data-product-id')
                if product_id and product_id in updates.get('prices', {}):
                    price_element.string = str(updates['prices'][product_id])

            # Update other dynamic content
            for element in soup.find_all(class_='dynamic-content'):
                content_id = element.get('data-content-id')
                if content_id and content_id in updates.get('content', {}):
                    element.string = updates['content'][content_id]

            return str(soup)
        except Exception as e:
            logger.error(f"Error updating content: {str(e)}")
            return html_content

    def validate_content(self, content: str, rules: Dict[str, Any]) -> bool:
        """Validate updated content against rules."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check required elements
            for element, required in rules.get('required_elements', {}).items():
                if required and not soup.find(element):
                    return False

            # Validate content structure
            if rules.get('structure'):
                for selector, validation in rules['structure'].items():
                    element = soup.select_one(selector)
                    if not element or not validation(element):
                        return False

            return True
        except Exception as e:
            logger.error(f"Error validating content: {str(e)}")
            return False 