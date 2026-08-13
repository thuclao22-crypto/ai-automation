"""Main application entry point."""

import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.social_media import SocialMediaPublisher
from src.browser.automation import BrowserAutomator
from src.ui.main_window import MainWindow

class AIAutomationPost:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.publisher = SocialMediaPublisher()
        self.browser = BrowserAutomator()
        self.ui = MainWindow()
        
    def run(self):
        """Run the application."""
        self.ui.run()

if __name__ == "__main__":
    app = AIAutomationPost()
    app.run()