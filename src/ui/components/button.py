import tkinter as tk
from src.ui.theme import theme

def _adjust_color(hex_color, factor):
    """Lighten or darken a hex color by a factor.
    factor > 1 lightens, factor < 1 darkens.
    """
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    rgb = tuple(int(hex_color[i:i+lv//3], 16) for i in range(0, lv, lv//3))
    rgb = tuple(min(255, max(0, int(c * factor))) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


class Button(tk.Button):
    """A styled Tkinter button supporting variant and accent_color override.

    Args:
        master: Parent widget.
        variant: One of "primary", "secondary", "outline".
        accent_color: Optional hex color to override the primary variant's background.
        **kwargs: Other tk.Button options (e.g., text, command, width, height).
    """

    def __init__(self, master=None, variant="primary", accent_color=None, **kwargs):
        # Set default font and padding from theme
        kwargs.setdefault(
            "font",
            (theme["typography"]["font_family"], theme["typography"]["font_size_body"])
        )
        kwargs.setdefault("padx", theme["spacing"]["md"])
        kwargs.setdefault("pady", theme["spacing"]["xs"])

        # Determine colors based on variant and accent_color
        if variant == "primary":
            bg = accent_color or theme["colors"]["status_scheduled"]  # fallback to scheduled blue
            fg = theme["colors"]["text_primary"]
        elif variant == "secondary":
            bg = theme["colors"]["bg_card"]
            fg = theme["colors"]["text_primary"]
        elif variant == "outline":
            bg = theme["colors"]["bg_primary"]
            fg = accent_color or theme["colors"]["status_scheduled"]
            kwargs.setdefault("highlightbackground", fg)
            kwargs.setdefault("highlightthickness", 1)
            kwargs.setdefault("relief", "flat")
        else:
            raise ValueError(f"Unsupported variant: {variant}")

        # Store original colors for hover and disabled states
        self._normal_bg = bg
        self._normal_fg = fg
        self._hover_bg = _adjust_color(bg, 1.1) if variant != "outline" else _adjust_color(bg, 1.05)
        self._hover_fg = fg
        self._disabled_bg = theme["colors"]["bg_card"]
        self._disabled_fg = theme["colors"]["text_muted"]

        super().__init__(master, background=bg, foreground=fg, **kwargs)

        # Bind hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        # Track initial state
        self._update_disabled_state()

    def _on_enter(self, event):
        if self["state"] != "disabled":
            self.configure(background=self._hover_bg, foreground=self._hover_fg)

    def _on_leave(self, event):
        if self["state"] != "disabled":
            self.configure(background=self._normal_bg, foreground=self._normal_fg)

    def _update_disabled_state(self):
        if self["state"] == "disabled":
            self.configure(background=self._disabled_bg, foreground=self._disabled_fg)
        else:
            self.configure(background=self._normal_bg, foreground=self._normal_fg)

    # Override configure to handle state changes
    def configure(self, cnf=None, **kw):
        if "state" in kw or (cnf and "state" in cnf):
            super().configure(cnf, **kw)
            self._update_disabled_state()
        else:
            super().configure(cnf, **kw)

    # Alias for config
    config = configure


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Button Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    Button(root, text="Primary", variant="primary").pack(pady=5)
    Button(root, text="Secondary", variant="secondary").pack(pady=5)
    Button(root, text="Outline", variant="outline").pack(pady=5)
    Button(root, text="Facebook Blue", variant="primary", accent_color=theme["colors"]["platform"]["facebook"]["primary"]).pack(pady=5)
    Button(root, text="Disabled", variant="primary", state="disabled").pack(pady=5)

    root.mainloop()