"""Main application window."""

import tkinter as tk
from src.ui.theme import theme
from src.ui.components.icon_button import IconButton
from src.ui.components.avatar import Avatar
from src.ui.sidebar import Sidebar
from src.ui.router import Router
from src.ui.screens.placeholder_screen import register_all_placeholders
from src.ui.screens.dashboard_screen import build_dashboard_screen
from src.ui.screens.facebook_module import build_facebook_module_screen


class MainWindow:
    """Main application window for social media publishing."""

    def __init__(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title("AI AUTOMATION POST")
        self.root.configure(bg=theme["colors"]["bg_primary"])
        self.root.minsize(1400, 900)
        self.root.resizable(True, True)

        # Create top bar
        self._create_top_bar()

        # Create body (sidebar and content areas)
        self._create_body()

    def _create_top_bar(self):
        """Create the top bar with logo, text, and action buttons."""
        top_bar = tk.Frame(
            self.root,
            height=64,
            bg=theme["colors"]["bg_card"]
        )
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)  # Maintain fixed height

        # Left container: logo mark and text block
        left_container = tk.Frame(top_bar, bg=theme["colors"]["bg_card"])
        left_container.pack(side=tk.LEFT, padx=theme["spacing"]["md"], pady=theme["spacing"]["sm"])

        # Logo mark (placeholder icon box)
        logo_mark = tk.Frame(
            left_container,
            width=40,
            height=40,
            bg=theme["colors"]["bg_primary"]
        )
        logo_mark.pack(side=tk.LEFT, padx=(0, theme["spacing"]["sm"]))
        logo_mark.pack_propagate(False)  # Keep fixed size

        # Text block: two-line text
        text_block = tk.Frame(left_container, bg=theme["colors"]["bg_card"])
        text_block.pack(side=tk.LEFT)

        # First line: "AI AUTOMATION POST"
        title_label = tk.Label(
            text_block,
            text="AI AUTOMATION POST",
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_h2"],
                theme["typography"]["font_weight_bold"]
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"]
        )
        title_label.pack(anchor="w")

        # Second line: "All-in-One Social Media Automation"
        subtitle_label = tk.Label(
            text_block,
            text="All-in-One Social Media Automation",
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"]
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"]
        )
        subtitle_label.pack(anchor="w")

        # Right container: action buttons
        right_container = tk.Frame(top_bar, bg=theme["colors"]["bg_card"])
        right_container.pack(side=tk.RIGHT, padx=theme["spacing"]["md"], pady=theme["spacing"]["sm"])

        # Button container for IconButtons with 12px gaps
        button_container = tk.Frame(right_container, bg=theme["colors"]["bg_card"])
        button_container.pack(side=tk.LEFT)

        # Notification bell
        bell_button = IconButton(
            button_container,
            icon="bell",
            size=24
        )
        bell_button.pack(side=tk.LEFT, padx=(0, 6))  # 6px right padding -> 12px gap between buttons

        # Theme toggle (sun/moon placeholder)
        theme_button = IconButton(
            button_container,
            icon="sun",
            size=24
        )
        theme_button.pack(side=tk.LEFT, padx=(0, 6))

        # Avatar (profile picture placeholder)
        avatar = Avatar(
            button_container,
            size=24,
            fallback_text="HT"
        )
        avatar.pack(side=tk.LEFT)

    def _create_body(self):
        """Create the body with sidebar and content regions."""
        body = tk.Frame(self.root, bg=theme["colors"]["bg_primary"])
        body.pack(fill=tk.BOTH, expand=True)

        # Content area (remaining space) - created first so we can pass it to router
        self.content_area = tk.Frame(
            body,
            bg=theme["colors"]["bg_primary"]
        )
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize router with content area
        self.router = Router(self.content_area)

        # Register placeholder screens for all non-Dashboard screens
        register_all_placeholders(self.router)

        # Register the real Dashboard screen (Phase 1.3)
        self.router.register_screen("dashboard", build_dashboard_screen)
        
        # Register the real Facebook module screen (Phase 1.5)
        self.router.register_screen("facebook", build_facebook_module_screen)

        # Sidebar (fixed width) - created after so it can use the router
        self.sidebar = Sidebar(
            body,
            on_navigate=self._on_navigate,
            width=240,
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Maintain fixed width

        # Show initial screen (Dashboard)
        self.router.show_screen("dashboard")

    def _on_navigate(self, screen_name: str):
        """Handle navigation from sidebar."""
        self.router.show_screen(screen_name)
        # Update sidebar active state
        self.sidebar._set_active_screen(screen_name)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()