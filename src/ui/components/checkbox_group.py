import tkinter as tk
from src.ui.theme import theme

class CheckboxGroup(tk.Frame):
    """A horizontal row of labeled checkboxes.

    Args:
        master: Parent widget.
        options: List of option strings.
        variable: Optional dictionary to store the state of each checkbox.
                  If not provided, a dictionary will be created.
        **kwargs: Other tk.Frame options.
    """

    def __init__(self, master=None, options=None, variable=None, **kwargs):
        super().__init__(master, bg=theme["colors"]["bg_primary"])

        self.options = options or []
        self._variable = variable if variable is not None else {}

        # Create a checkbox for each option
        for option in self.options:
            # Initialize the variable for this option if not present
            if option not in self._variable:
                self._variable[option] = tk.BooleanVar(value=False)

            cb = tk.Checkbutton(
                self,
                text=option,
                variable=self._variable[option],
                bg=theme["colors"]["bg_primary"],
                fg=theme["colors"]["text_primary"],
                selectcolor=theme["colors"]["bg_card"],
                font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
                activebackground=theme["colors"]["bg_primary"],
                activeforeground=theme["colors"]["text_primary"],
            )
            cb.pack(side="left", padx=(0, theme["spacing"]["sm"]))

    def get_checked(self):
        """Return a set of currently checked option strings."""
        return {option for option, var in self._variable.items() if var.get()}

    def set_checked(self, checked_options):
        """Set the checked state of each option.
        checked_options: iterable of option strings to check.
        """
        for option in self.options:
            self._variable[option].set(option in checked_options)


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("CheckboxGroup Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    tk.Label(root, text="CheckboxGroup:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    options = ["Post", "Reels", "Fanpage", "Group"]
    cbg = CheckboxGroup(root, options=options)
    cbg.pack(anchor="w", padx=10, pady=5)

    def show_checked():
        print("Checked:", cbg.get_checked())

    tk.Button(root, text="Show Checked", command=show_checked).pack(pady=10)

    root.mainloop()