import tkinter as tk
from src.ui.theme import theme
from datetime import datetime

class DateTimePicker(tk.Frame):
    """A compound widget with a date field and a time field.

    Args:
        master: Parent widget.
        **kwargs: Other tk.Frame options.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg=theme["colors"]["bg_primary"])

        # Store the selected date and time as strings
        self._date_str = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self._time_str = tk.StringVar(value=datetime.now().strftime("%H:%M"))

        # Create date field
        date_frame = tk.Frame(self, bg=theme["colors"]["bg_primary"])
        date_frame.pack(side="left", padx=(0, theme["spacing"]["md"]))

        self.date_button = tk.Button(
            date_frame,
            text="",  # We'll set the icon via the theme's fallback
            command=self._pick_date,
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            relief="flat",
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
        )
        self.date_button.pack(side="left")
        self._update_date_button_icon()

        self.date_entry = tk.Entry(
            date_frame,
            textvariable=self._date_str,
            width=12,
            justify="center",
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            relief="flat",
        )
        self.date_entry.pack(side="left", padx=(theme["spacing"]["xs"], 0))

        # Create time field
        time_frame = tk.Frame(self, bg=theme["colors"]["bg_primary"])
        time_frame.pack(side="left")

        self.time_button = tk.Button(
            time_frame,
            text="",  # We'll set the icon via the theme's fallback
            command=self._pick_time,
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            relief="flat",
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
        )
        self.time_button.pack(side="left")
        self._update_time_button_icon()

        self.time_entry = tk.Entry(
            time_frame,
            textvariable=self._time_str,
            width=8,
            justify="center",
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            relief="flat",
        )
        self.time_entry.pack(side="left", padx=(theme["spacing"]["xs"], 0))

    def _update_date_button_icon(self):
        icon_fallbacks = theme["icons"]
        icon_text = icon_fallbacks.get("calendar", "���📅")
        self.date_button.config(text=icon_text)

    def _update_time_button_icon(self):
        icon_fallbacks = theme["icons"]
        icon_text = icon_fallbacks.get("clock", "���🕐")  # Note: we don't have clock in the fallback, but we can use a placeholder
        # Since we don't have clock in the provided ICON_FALLBACKS, we'll use a default or note that we need to add it.
        # For now, we'll use the fallback for "clock" if exists, else use a generic.
        # We'll check the theme's icon fallbacks for "clock", but it's not in the list from theme.py.
        # We'll use the string "���🕐" as a hardcoded fallback? But we cannot use raw unicode? 
        # Actually, we can use the unicode string because it's not a raw pixel or color. 
        # The requirement is about raw hex codes and pixel literals. Using a unicode string is acceptable.
        # However, we are supposed to use the theme's icon fallbacks. Since "clock" is not there, we'll use the unicode directly.
        # We'll change: we'll use the theme's get_icon_fallback function? But we don't have that exposed.
        # We'll use the ICON_FALLBACKS dict from theme.
        icon_text = theme["icons"].get("clock", "���🕐")
        self.time_button.config(text=icon_text)

    def _pick_date(self):
        # In a real implementation, this would open a date picker popup.
        # For smoke test, we'll just set the date to today.
        self._date_str.set(datetime.now().strftime("%Y-%m-%d"))

    def _pick_time(self):
        # In a real implementation, this would open a time picker popup.
        # For smoke test, we'll just set the time to now.
        self._time_str.set(datetime.now().strftime("%H:%M"))

    def get_date(self):
        return self._date_str.get()

    def get_time(self):
        return self._time_str.get()

    def set_date(self, date_str):
        self._date_str.set(date_str)

    def set_time(self, time_str):
        self._time_str.set(time_str)


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("DateTimePicker Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    dtp = DateTimePicker(root)
    dtp.pack(padx=20, pady=20)

    def show_values():
        print(f"Date: {dtp.get_date()}, Time: {dtp.get_time()}")

    tk.Button(root, text="Show Values", command=show_values).pack(pady=10)

    root.mainloop()