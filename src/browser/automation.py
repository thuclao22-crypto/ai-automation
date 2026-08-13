"""Browser automation and content extraction."""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class BrowserAutomator:
    """Handles browser automation tasks."""
    
    def __init__(self):
        """Initialize the browser automator."""
        self.driver = None
        
    def start_browser(self, headless=False):
        """Start the browser instance.
        
        Args:
            headless (bool): Run browser in headless mode if True
        """
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=Service(), options=options)
        
    def stop_browser(self):
        """Stop the browser instance."""
        if self.driver:
            self.driver.quit()
            
    def extract_content(self, url, selector):
        """Extract content from a webpage.
        
        Args:
            url (str): URL to extract content from
            selector (str): CSS selector for target content
            
        Returns:
            str: Extracted content or None if not found
        """
        if not self.driver:
            return None
            
        self.driver.get(url)
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text
        except:
            return None