import tkinter as tk
from src.ui.theme import theme

class IconButton(tk.Button):
    """A small square/circular button for a single icon.

    Args:
        master: Parent widget.
        icon: Either a unicode string or a key from theme["icons"]["fallbacks"].
        command: Callback function when button is clicked.
        size: Size of the button in pixels (width and height). Defaults to 24.
        **kwargs: Other tk.Button options (e.g., tooltip).
    """

    def __init__(self, master=None, icon="", command=None, size=24, **kwargs):
        # Resolve icon: if it's a key in theme's icon fallbacks, use the fallback; otherwise use as-is
        icon_fallbacks = theme["icons"]
        if isinstance(icon, str) and icon in icon_fallbacks:
            display_icon = icon_fallbacks[icon]
        else:
            display_icon = icon

        # Set default appearance
        kwargs.setdefault("font", (theme["typography"]["font_family"], theme["typography"]["font_size_body"]))
        kwargs.setdefault("text", display_icon)
        kwargs.setdefault("command", command)
        kwargs.setdefault("width", size // 8)  # Rough conversion: 8 pixels per character unit
        kwargs.setdefault("height", size // 16)  # Rough conversion: 16 pixels per line unit
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("borderwidth", 0)
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("bg", theme["colors"]["bg_card"])
        kwargs.setdefault("fg", theme["colors"]["text_primary"])
        kwargs.setdefault("activebackground", theme["colors"]["border"])
        kwargs.setdefault("activeforeground", theme["colors"]["text_primary"])

        super().__init__(master, **kwargs)

        # Store original colors for hover effect
        self._normal_bg = kwargs["bg"]
        self._normal_fg = kwargs["fg"]
        self._hover_bg = theme["colors"]["border"]
        self._hover_fg = theme["colors"]["text_primary"]

        # Bind hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.configure(background=self._hover_bg, foreground=self._hover_fg)

    def _on_leave(self, event):
        self.configure(background=self._normal_bg, foreground=self._normal_fg)


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("IconButton Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    # Test with unicode fallback
    IconButton(root, icon="home", command=lambda: print("Home clicked")).pack(side="left", padx=5, pady=5)
    IconButton(root, icon="gear", command=lambda: print("Settings clicked")).pack(side="left", padx=5, pady=5)
    IconButton(root, icon="bell", command=lambda: print("Bell clicked")).pack(side="left", padx=5, pady=5)

    root.mainloop()