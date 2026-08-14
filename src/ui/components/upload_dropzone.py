import tkinter as tk
from src.ui.theme import theme

class UploadDropzone(tk.Frame):
    """A bordered rectangular drop zone for uploading files.

    Args:
        master: Parent widget.
        kind: Either "image" or "video". Determines default icon and label.
        label: Primary label text. If not provided, defaults based on kind.
        subtext: Subtext line (e.g., accepted formats). If not provided, defaults based on kind.
        callback: Function to call when the drop zone is clicked (to open file dialog).
        **kwargs: Other tk.Frame options.
    """

    def __init__(self, master=None, kind="image", label=None, subtext=None, callback=None, **kwargs):
        super().__init__(master, bg=theme["colors"]["bg_primary"])

        self.kind = kind
        self.callback = callback

        # Set default label and subtext based on kind
        if label is None:
            if kind == "image":
                label = "Tải lên hình ảnh"
            else:  # video
                label = "Tải lên video"
        if subtext is None:
            if kind == "image":
                subtext = "JPG, PNG, WEBP"
            else:  # video
                subtext = "MP4, MOV, AVI"

        # Configure the frame to have a border-like appearance
        # We'll use a Frame with a background and then an inner Frame with padding and a different background?
        # Actually, we want a bordered area. We'll set the frame's background to the border color and then
        # put an inner frame with the card background and padding.
        # This way, the outer frame's background shows as a border.

        # Set the outer frame's background to border color
        self.configure(bg=theme["colors"]["border"])

        # Inner frame with card background and padding
        inner_frame = tk.Frame(self, bg=theme["colors"]["bg_card"])
        inner_frame.pack(padx=theme["spacing"]["xs"], pady=theme["spacing"]["xs"], fill="both", expand=True)

        # Upload icon
        icon_fallbacks = theme["icons"]
        icon_key = "image" if kind == "image" else "video"
        icon_text = icon_fallbacks.get(icon_key, "���������📎")  # fallback to a generic attachment icon
        self.icon_label = tk.Label(
            inner_frame,
            text=icon_text,
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_h1"]),  # large icon
        )
        self.icon_label.pack(pady=(theme["spacing"]["md"], theme["spacing"]["xs"]))

        # Primary label
        self.label_label = tk.Label(
            inner_frame,
            text=label,
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"],
                  theme["typography"]["font_weight_bold"]),
        )
        self.label_label.pack(pady=(0, theme["spacing"]["xs"]))

        # Subtext
        self.subtext_label = tk.Label(
            inner_frame,
            text=subtext,
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_muted"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_small"]),
        )
        self.subtext_label.pack()

        # Make the entire drop zone clickable
        self.bind("<Button-1>", self._on_click)
        inner_frame.bind("<Button-1>", self._on_click)
        self.icon_label.bind("<Button-1>", self._on_click)
        self.label_label.bind("<Button-1>", self._on_click)
        self.subtext_label.bind("<Button-1>", self._on_click)

        # Change cursor to indicate clickability
        self.configure(cursor="hand2")
        inner_frame.configure(cursor="hand2")
        self.icon_label.configure(cursor="hand2")
        self.label_label.configure(cursor="hand2")
        self.subtext_label.configure(cursor="hand2")

    def _on_click(self, event):
        if self.callback:
            self.callback()


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("UploadDropzone Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])

    def on_image_click():
        print("Image dropzone clicked")

    def on_video_click():
        print("Video dropzone clicked")

    # Image dropzone
    tk.Label(root, text="Image:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    udz_image = UploadDropzone(root, kind="image", callback=on_image_click)
    udz_image.pack(fill="x", padx=10, pady=5)

    # Video dropzone
    tk.Label(root, text="Video:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    udz_video = UploadDropzone(root, kind="video", callback=on_video_click)
    udz_video.pack(fill="x", padx=10, pady=5)

    # Custom label and subtext
    tk.Label(root, text="Custom:", bg=theme["colors"]["bg_primary"], fg=theme["colors"]["text_primary"]).pack(anchor="w", padx=10, pady=(10,0))
    udz_custom = UploadDropzone(
        root,
        kind="image",
        label="Custom Label",
        subtext="Custom Subtext",
        callback=lambda: print("Custom clicked")
    )
    udz_custom.pack(fill="x", padx=10, pady=5)

    root.mainloop()