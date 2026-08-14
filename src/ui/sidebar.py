"""Sidebar navigation component with 9 navigation items."""

import tkinter as tk
from src.ui.theme import theme
from src.ui.components.icon_button import IconButton
from src.ui.components.card import Card


class SidebarItem(tk.Frame):
    """A single sidebar navigation item with icon, label, and three visual states."""

    def __init__(self, master, icon_key: str, label: str, on_click=None, **kwargs):
        """
        Initialize a sidebar item.

        Args:
            master: Parent widget.
            icon_key: Key for the icon from theme["icons"].
            label: Text label for the item.
            on_click: Callback function when item is clicked.
            **kwargs: Additional tk.Frame options.
        """
        kwargs.setdefault("bg", theme["colors"]["bg_card"])
        super().__init__(master, **kwargs)

        self.icon_key = icon_key
        self.label = label
        self.on_click = on_click
        self._is_active = False
        self._is_hovered = False

        # Colors for three states
        self._default_bg = theme["colors"]["bg_card"]
        self._default_fg = theme["colors"]["text_secondary"]
        self._hover_bg = "#1E232D"  # Slightly lighter than BG_CARD
        self._hover_fg = theme["colors"]["text_primary"]
        self._active_bg = theme["colors"]["status_scheduled"]  # Primary accent color
        self._active_fg = theme["colors"]["text_primary"]

        self._build_ui()
        self._bind_events()
        self._update_appearance()

    def _build_ui(self):
        """Build the UI for the sidebar item."""
        # Icon
        icon_fallbacks = theme["icons"]
        icon_text = icon_fallbacks.get(self.icon_key, "?")

        self.icon_label = tk.Label(
            self,
            text=icon_text,
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            bg=self._default_bg,
            fg=self._default_fg,
        )
        self.icon_label.pack(side=tk.LEFT, padx=(theme["spacing"]["md"], theme["spacing"]["sm"]), pady=theme["spacing"]["sm"])

        # Label
        self.text_label = tk.Label(
            self,
            text=self.label,
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            bg=self._default_bg,
            fg=self._default_fg,
        )
        self.text_label.pack(side=tk.LEFT, padx=(0, theme["spacing"]["md"]), pady=theme["spacing"]["sm"])

    def _bind_events(self):
        """Bind mouse events for hover and click."""
        for widget in (self, self.icon_label, self.text_label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, event):
        """Handle mouse enter."""
        self._is_hovered = True
        self._update_appearance()

    def _on_leave(self, event):
        """Handle mouse leave."""
        self._is_hovered = False
        self._update_appearance()

    def _on_click(self, event):
        """Handle click."""
        if self.on_click:
            self.on_click(self)

    def _update_appearance(self):
        """Update visual appearance based on state."""
        if self._is_active:
            bg = self._active_bg
            fg = self._active_fg
        elif self._is_hovered:
            bg = self._hover_bg
            fg = self._hover_fg
        else:
            bg = self._default_bg
            fg = self._default_fg

        self.configure(bg=bg)
        self.icon_label.configure(bg=bg, fg=fg)
        self.text_label.configure(bg=bg, fg=fg)

    def set_active(self, active: bool):
        """Set the active state of this item."""
        self._is_active = active
        self._update_appearance()


class Sidebar(tk.Frame):
    """Left sidebar with 9 navigation items."""

    # Navigation items in order: (icon_key, label, screen_name)
    NAV_ITEMS = [
        ("home", "Dashboard", "dashboard"),
        ("calendar", "Schedule", "schedule"),
        ("folder", "Content Library", "content_library"),
        ("user", "Account & Profile", "account_profile"),
        ("list", "Task Manager", "task_manager"),
        ("document", "Logs", "logs"),
        ("gear", "Settings", "settings"),
        ("activity", "System Monitor", "system_monitor"),
        ("help", "Help", "help"),
    ]

    def __init__(self, master, on_navigate=None, **kwargs):
        """
        Initialize the sidebar.

        Args:
            master: Parent widget.
            on_navigate: Callback function(screen_name) when navigation item is clicked.
            **kwargs: Additional tk.Frame options.
        """
        kwargs.setdefault("bg", theme["colors"]["bg_card"])
        kwargs.setdefault("width", 240)
        super().__init__(master, **kwargs)
        self.pack_propagate(False)  # Maintain fixed width

        self.on_navigate = on_navigate
        self.items: list[SidebarItem] = []
        self._active_screen = "dashboard"

        self._build_ui()

    def _build_ui(self):
        """Build the sidebar UI with all navigation items."""
        # Container for nav items
        nav_container = tk.Frame(self, bg=theme["colors"]["bg_card"])
        nav_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=theme["spacing"]["md"])

        for icon_key, label, screen_name in self.NAV_ITEMS:
            item = SidebarItem(
                nav_container,
                icon_key=icon_key,
                label=label,
                on_click=lambda item, sn=screen_name: self._on_item_click(item, sn),
            )
            item.pack(fill=tk.X, padx=theme["spacing"]["sm"], pady=2)
            self.items.append((item, screen_name))

        # Set initial active item (Dashboard)
        self._set_active_screen("dashboard")

    def _on_item_click(self, clicked_item: SidebarItem, screen_name: str):
        """Handle navigation item click."""
        if self.on_navigate:
            self.on_navigate(screen_name)
        self._set_active_screen(screen_name)

    def _set_active_screen(self, screen_name: str):
        """Update active state for all items."""
        self._active_screen = screen_name
        for item, sn in self.items:
            item.set_active(sn == screen_name)

    def get_active_screen(self) -> str:
        """Get the currently active screen name."""
        return self._active_screen


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Sidebar Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])
    root.geometry("300x600")

    def on_nav(screen_name):
        print(f"Navigate to: {screen_name}")

    sidebar = Sidebar(root, on_navigate=on_nav)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    root.mainloop()