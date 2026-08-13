"""Main application window."""

import tkinter as tk
from tkinter import ttk

class MainWindow:
    """Main application window for social media publishing."""
    
    def __init__(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title("AI Automation Post")
        self.root.geometry("800x600")
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize UI components
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and arrange UI components."""
        # Platform selection
        self.platform_frame = ttk.LabelFrame(self.main_frame, text="Platforms")
        self.platform_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Content input
        self.content_frame = ttk.LabelFrame(self.main_frame, text="Content")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Action buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
    def run(self):
        """Run the main application loop."""
        self.root.mainloop()