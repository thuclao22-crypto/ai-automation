import tkinter as tk
from src.ui.theme import theme

class Input(tk.Frame):
    """A text entry or textarea with placeholder, character counter, and focus border.

    Args:
        master: Parent widget.
        placeholder: Placeholder text to show when empty.
        max_length: Maximum number of characters (optional). If set, shows counter.
        multiline: If True, uses a Text widget; otherwise, Entry.
        **kwargs: Other options passed to the underlying Entry or Text widget.
    """

    def __init__(self, master=None, placeholder="", max_length=None, multiline=False, **kwargs):
        super().__init__(master, bg=theme["colors"]["bg_primary"])

        self.placeholder = placeholder
        self.max_length = max_length
        self.multiline = multiline

        # Create the text widget (Entry or Text)
        if self.multiline:
            self.widget = tk.Text(
                self,
                wrap="word",
                width=20,
                height=2,
                relief="flat",
                highlightthickness=0,
                borderwidth=0,
            )
        else:
            self.widget = tk.Entry(
                self,
                relief="flat",
                highlightthickness=0,
                borderwidth=0,
            )

        # Configure the widget's appearance
        widget_cfg = {
            "background": theme["colors"]["bg_card"],
            "foreground": theme["colors"]["text_primary"],
            "font": (theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            # We'll manage the highlight (focus border) via the frame's highlight? 
            # Instead, we'll use the widget's own highlight and then place it in a frame with padding.
            # But we want the focus border to be visible. We'll set the widget's highlightbackground and highlightcolor.
            "highlightbackground": theme["colors"]["border"],
            "highlightcolor": theme["colors"]["status_scheduled"],
            "highlightthickness": 1,
        }
        # Update with any user-provided kwargs (but avoid overriding our essentials)
        widget_cfg.update(kwargs)
        self.widget.configure(**widget_cfg)

        # Place the widget inside the frame with padding
        self.widget.pack(
            fill="both",
            expand=True,
            padx=theme["spacing"]["xs"],
            pady=theme["spacing"]["xs"],
        )

        # Placeholder state
        self._showing_placeholder = False
        if self.placeholder:
            self._show_placeholder()

        # Character counter label
        if self.max_length is not None:
            self.counter_label = tk.Label(
                self,
                text=f"0/{self.max_length}",
                font=(theme["typography"]["font_family"], theme["typography"]["font_size_small"]),
                foreground=theme["colors"]["text_muted"],
                background=theme["colors"]["bg_primary"],
            )
            self.counter_label.pack(
                anchor="e",
                padx=theme["spacing"]["xs"],
                pady=(0, theme["spacing"]["xs"]),
            )
        else:
            self.counter_label = None

        # Bind events
        self.widget.bind("<FocusIn>", self._on_focus_in)
        self.widget.bind("<FocusOut>", self._on_focus_out)
        self.widget.bind("<KeyRelease>", self._on_key_change)
        # Also bind <Button-1> to click? Not needed for placeholder.

        # Initialize counter
        self._update_counter()

    def _show_placeholder(self):
        if not self.placeholder:
            return
        self._showing_placeholder = True
        if self.multiline:
            self.widget.delete("1.0", "end")
            self.widget.insert("1.0", self.placeholder)
        else:
            self.widget.delete(0, "end")
            self.widget.insert(0, self.placeholder)
        self.widget.configure(foreground=theme["colors"]["text_muted"])

    def _hide_placeholder(self):
        if not self._showing_placeholder:
            return
        self._showing_placeholder = False
        if self.multiline:
            self.widget.delete("1.0", "end")
        else:
            self.widget.delete(0, "end")
        self.widget.configure(foreground=theme["colors"]["text_primary"])

    def _on_focus_in(self, event):
        if self._showing_placeholder:
            self._hide_placeholder()

    def _on_focus_out(self, event):
        current = self.get()
        if not current:
            self._show_placeholder()

    def _on_key_change(self, event):
        self._update_counter()

    def _update_counter(self):
        if self.counter_label is None:
            return
        current = len(self.get())
        if self.max_length is not None:
            self.counter_label.configure(text=f"{current}/{self.max_length}")
        else:
            self.counter_label.configure(text=str(current))

    def get(self):
        """Get the current value, excluding placeholder text."""
        if self._showing_placeholder:
            return ""
        if self.multiline:
            return self.widget.get("1.0", "end-1c")
        else:
            return self.widget.get()

    def set(self, value):
        """Set the value, clearing placeholder if any."""
        self._hide_placeholder()
        if self.multiline:
            self.widget.delete("1.0", "end")
            self.widget.insert("1.0", value)
        else:
            self.widget.delete(0, "end")
            self.widget.insert(0, value)
        self._update_counter()

    # For compatibility with Entry/Text, we can also expose focus_set, etc.
    def focus_set(self):
        self.widget.focus_set()


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Input Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    # Single-line input
    tk.Label(root, text="Single-line:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    inp1 = Input(root, placeholder="Enter text...", max_length=50)
    inp1.pack(fill="x", padx=10, pady=5)

    # Multi-line input
    tk.Label(root, text="Multi-line:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    inp2 = Input(root, placeholder="Enter longer text...", max_length=200, multiline=True)
    inp2.pack(fill="x", padx=10, pady=5)

    # Button to show values
    def show_values():
        print("Single-line:", repr(inp1.get()))
        print("Multi-line:", repr(inp2.get()))

    tk.Button(root, text="Show Values", command=show_values).pack(pady=10)

    root.mainloop()