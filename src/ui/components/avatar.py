import tkinter as tk
from src.ui.theme import theme
from PIL import Image, ImageTk
import os

class Avatar(tk.Frame):
    """Circular image container with fallback to initials-in-circle.

    Args:
        master: Parent widget.
        image_path: Path to an image file (optional).
        size: Size of the avatar in pixels (width and height). Defaults to 40.
        fallback_text: Text to show when no image is set (usually initials).
        **kwargs: Other tk.Frame options.
    """

    def __init__(self, master=None, image_path=None, size=40, fallback_text="", **kwargs):
        super().__init__(master, bg=theme["colors"]["bg_primary"])

        self.size = size
        self.fallback_text = fallback_text
        self.image_path = image_path

        # Create a canvas for drawing the circular avatar
        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg=theme["colors"]["bg_primary"],
            highlightthickness=0,
        )
        self.canvas.pack()

        # Load and display the image or fallback
        self._image_ref = None  # Keep a reference to prevent garbage collection
        self._draw_avatar()

    def _draw_avatar(self):
        self.canvas.delete("all")  # Clear previous drawing

        if self.image_path and os.path.exists(self.image_path):
            try:
                # Open and resize the image
                image = Image.open(self.image_path)
                image = image.resize((self.size, self.size), Image.Resampling.LANCZOS)
                
                # Create a circular mask
                mask = Image.new("L", (self.size, self.size), 0)
                from PIL import ImageDraw
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, self.size, self.size), fill=255)
                
                # Apply the mask
                image.putalpha(mask)
                
                # Convert to Tkinter-compatible photo image
                self._image_ref = ImageTk.PhotoImage(image)
                
                # Draw the image on the canvas
                self.canvas.create_image(0, 0, anchor="nw", image=self._image_ref)
            except Exception as e:
                print(f"Error loading avatar image: {e}")
                self._draw_fallback()
        else:
            self._draw_fallback()

    def _draw_fallback(self):
        # Draw a circle with the fallback text
        # Background circle
        self.canvas.create_oval(
            0, 0, self.size, self.size,
            fill=theme["colors"]["bg_card"],
            outline=""
        )
        
        # Text (initials)
        if self.fallback_text:
            self.canvas.create_text(
                self.size // 2,
                self.size // 2,
                text=self.fallback_text,
                fill=theme["colors"]["text_primary"],
                font=(theme["typography"]["font_family"], 
                      max(10, self.size // 3),  # Scale font size with avatar size
                      theme["typography"]["font_weight_bold"]),
                anchor="center"
            )

    def set_image(self, image_path):
        """Set a new image path and redraw."""
        self.image_path = image_path
        self._draw_avatar()

    def set_fallback_text(self, text):
        """Set new fallback text and redraw."""
        self.fallback_text = text
        self._draw_avatar()


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Avatar Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    # Avatar with fallback text
    tk.Label(root, text="With fallback:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    avatar1 = Avatar(root, size=50, fallback_text="HT")
    avatar1.pack(anchor="w", padx=10, pady=5)

    # Avatar with image (if exists, otherwise fallback)
    tk.Label(root, text="With image (or fallback):", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    avatar2 = Avatar(root, size=50, image_path="nonexistent.png", fallback_text="ABC")
    avatar2.pack(anchor="w", padx=10, pady=5)

    root.mainloop()