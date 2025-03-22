from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
from typing import Dict, List, Optional
from ..config.settings import USER_AGENT, TIMEOUT, MAX_RETRIES

class WebpageAnalyzer:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument(f'user-agent={USER_AGENT}')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize the Selenium WebDriver."""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
    
    def analyze_page(self, url: str) -> Dict:
        """
        Analyze a webpage for various metrics and issues.
        
        Args:
            url (str): URL of the webpage to analyze
            
        Returns:
            Dict: Analysis results including performance metrics, broken links, and content issues
        """
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source and create BeautifulSoup object
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Collect various metrics
            analysis = {
                "url": url,
                "title": self._get_title(soup),
                "meta_description": self._get_meta_description(soup),
                "broken_links": self._find_broken_links(soup),
                "performance_metrics": self._get_performance_metrics(),
                "content_issues": self._analyze_content(soup),
                "seo_issues": self._analyze_seo(soup)
            }
            
            return analysis
            
        except Exception as e:
            return {
                "error": str(e),
                "url": url,
                "status": "failed"
            }
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.text if title_tag else ""
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '') if meta_desc else ""
    
    def _find_broken_links(self, soup: BeautifulSoup) -> List[Dict]:
        """Find broken links on the page."""
        broken_links = []
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            if href.startswith('http'):
                try:
                    response = requests.head(href, timeout=TIMEOUT)
                    if response.status_code >= 400:
                        broken_links.append({
                            "url": href,
                            "text": link.text,
                            "status_code": response.status_code
                        })
                except:
                    broken_links.append({
                        "url": href,
                        "text": link.text,
                        "status_code": "connection_error"
                    })
        
        return broken_links
    
    def _get_performance_metrics(self) -> Dict:
        """Get page performance metrics using Selenium."""
        performance = self.driver.execute_script("return window.performance.getEntries();")
        
        metrics = {
            "load_time": 0,
            "dom_content_loaded": 0,
            "first_paint": 0,
            "first_contentful_paint": 0
        }
        
        for entry in performance:
            if entry['name'] == 'navigationStart':
                metrics['load_time'] = entry['startTime']
            elif entry['name'] == 'domContentLoadedEventEnd':
                metrics['dom_content_loaded'] = entry['startTime']
            elif entry['name'] == 'first-paint':
                metrics['first_paint'] = entry['startTime']
            elif entry['name'] == 'first-contentful-paint':
                metrics['first_contentful_paint'] = entry['startTime']
        
        return metrics
    
    def _analyze_content(self, soup: BeautifulSoup) -> List[str]:
        """Analyze content for common issues."""
        issues = []
        
        # Check for empty paragraphs
        paragraphs = soup.find_all('p')
        if any(len(p.text.strip()) == 0 for p in paragraphs):
            issues.append("Empty paragraphs found")
        
        # Check for missing alt text in images
        images = soup.find_all('img')
        if any(not img.get('alt') for img in images):
            issues.append("Images missing alt text")
        
        # Check for heading hierarchy
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if not headings:
            issues.append("No headings found")
        elif len([h for h in headings if h.name == 'h1']) > 1:
            issues.append("Multiple h1 tags found")
        
        return issues
    
    def _analyze_seo(self, soup: BeautifulSoup) -> List[str]:
        """Analyze SEO elements."""
        issues = []
        
        # Check for missing meta description
        if not self._get_meta_description(soup):
            issues.append("Missing meta description")
        
        # Check for missing title
        if not self._get_title(soup):
            issues.append("Missing title tag")
        
        # Check for canonical URL
        if not soup.find('link', attrs={'rel': 'canonical'}):
            issues.append("Missing canonical URL")
        
        return issues
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit() 