"""Placeholder screen builder for unbuilt screens."""

import tkinter as tk
from src.ui.theme import theme
from src.ui.components.card import Card


def build_placeholder(parent: tk.Widget, screen_name: str) -> tk.Frame:
    """
    Build a placeholder screen with a centered card showing "{screen_name} — Coming soon".

    Args:
        parent: Parent widget to contain the screen.
        screen_name: Name of the screen to display.

    Returns:
        A Frame containing the placeholder UI.
    """
    # Main container frame
    container = tk.Frame(parent, bg=theme["colors"]["bg_primary"])
    container.pack(fill=tk.BOTH, expand=True)

    # Center the card using a grid with weight
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # Create a centered card
    card = Card(
        container,
        show_header=False,
        padx=theme["spacing"]["xl"],
        pady=theme["spacing"]["xl"],
    )
    card.grid(row=0, column=0)

    # Format screen name for display (replace underscores with spaces, title case)
    display_name = screen_name.replace("_", " ").title()

    # Placeholder text
    placeholder_text = f"{display_name} — Coming soon"

    label = tk.Label(
        card.inner_frame,
        text=placeholder_text,
        font=(
            theme["typography"]["font_family"],
            theme["typography"]["font_size_h2"],
            theme["typography"]["font_weight_regular"]
        ),
        fg=theme["colors"]["text_secondary"],
        bg=theme["colors"]["bg_card"],
    )
    label.pack(expand=True)

    return container


# Screen names for the 8 non-Dashboard screens
PLACEHOLDER_SCREENS = [
    "schedule",
    "content_library",
    "account_profile",
    "task_manager",
    "logs",
    "settings",
    "system_monitor",
    "help",
]


def register_all_placeholders(router) -> None:
    """
    Register all placeholder screens with the router.

    Args:
        router: Router instance to register screens with.
    """
    for screen_name in PLACEHOLDER_SCREENS:
        # Use lambda with default argument to capture screen_name
        router.register_screen(
            screen_name,
            lambda parent, sn=screen_name: build_placeholder(parent, sn)
        )


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Placeholder Screen Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])
    root.geometry("600x400")

    content = tk.Frame(root, bg=theme["colors"]["bg_primary"])
    content.pack(fill=tk.BOTH, expand=True)

    # Test with a few screens
    for screen_name in ["schedule", "settings", "help"]:
        frame = build_placeholder(content, screen_name)
        frame.pack(fill=tk.BOTH, expand=True)
        break  # Only show one for test

    root.mainloop()