"""Platform Module Screen Template

A reusable, parameterized builder for all 6 platform module screens.
All platform-specific values come from ModuleConfig — no hardcoded platform names.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable

from src.ui.theme import theme, get_platform_color
from src.ui.components import (
    Card,
    Button,
    Input,
    UploadDropzone,
    DateTimePicker,
    Toggle,
    CheckboxGroup,
    Avatar,
    IconButton,
    Badge,
)
from src.ui.data.module_config import ModuleConfig
from src.ui.router import show_screen


def build_module_screen(parent: tk.Widget, config: ModuleConfig, sample_data: Dict[str, Any],
                        on_save: Optional[Callable[[Dict[str, Any]], None]] = None,
                        on_schedule: Optional[Callable[[Dict[str, Any]], None]] = None) -> tk.Frame:
    """Build a complete platform module screen from a config.

    Args:
        parent: Parent widget (typically a Frame or Toplevel).
        config: ModuleConfig instance with all platform-specific values.
        sample_data: Dict with runtime data (account name, stats, recent items, etc.).
        on_save: Callback function called when "Lưu" button is clicked, receives content_state dict.
        on_schedule: Callback function called when schedule button is clicked, receives content_state dict.

    Returns:
        A Frame containing the full module screen layout.
    """
    # Set default callbacks (no-op that prints to console)
    if on_save is None:
        on_save = lambda state: print("Save clicked:", state)
    if on_schedule is None:
        on_schedule = lambda state: print("Schedule clicked:", state)
    # Main container frame
    main_frame = tk.Frame(parent, bg=theme["colors"]["bg_primary"])
    main_frame.pack(fill="both", expand=True)

    # Configure grid: 2 columns (left content, right sidebar), 1 row
    main_frame.grid_columnconfigure(0, weight=3)  # Left column - content
    main_frame.grid_columnconfigure(1, weight=1)  # Right column - account info
    main_frame.grid_rowconfigure(0, weight=1)

    # Form state
    form_state = {
        "content": "",
        "checked_post_types": [],
        "extra_text": "",
        "selected_datetime": None,
        "post_now": False,
    }

    # =========================================================================
    # LEFT COLUMN - Content Area
    # =========================================================================
    left_column = tk.Frame(main_frame, bg=theme["colors"]["bg_primary"])
    left_column.grid(row=0, column=0, sticky="nsew", padx=(theme["spacing"]["md"], theme["spacing"]["sm"]), pady=theme["spacing"]["md"])
    left_column.grid_rowconfigure(5, weight=1)  # Make recent items area expandable if needed

    # ---- (a) Header Row ----
    header_frame = tk.Frame(left_column, bg=theme["colors"]["bg_primary"])
    header_frame.pack(fill="x", pady=(0, theme["spacing"]["md"]))

    # Platform icon + display name (left side)
    header_left = tk.Frame(header_frame, bg=theme["colors"]["bg_primary"])
    header_left.pack(side="left")

    # Platform icon from theme fallbacks
    icon_fallback = theme["icons"].get(config.platform_key.lower(), "����")
    icon_label = tk.Label(
        header_left,
        text=icon_fallback,
        bg=theme["colors"]["bg_primary"],
        fg=config.accent_color,
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_h1"]),
    )
    icon_label.pack(side="left", padx=(0, theme["spacing"]["sm"]))

    # Display name
    name_label = tk.Label(
        header_left,
        text=config.display_name,
        bg=theme["colors"]["bg_primary"],
        fg=theme["colors"]["text_primary"],
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_h2"], theme["typography"]["font_weight_bold"]),
    )
    name_label.pack(side="left", anchor="center")

    # Home + Settings IconButtons (right side)
    header_right = tk.Frame(header_frame, bg=theme["colors"]["bg_primary"])
    header_right.pack(side="right")

    IconButton(
        header_right,
        icon="home",
        command=lambda: show_screen("Dashboard"),
        size=28,
    ).pack(side="left", padx=(theme["spacing"]["xs"], 0))

    IconButton(
        header_right,
        icon="gear",
        command=lambda: None,  # No-op for settings
        size=28,
    ).pack(side="left", padx=(theme["spacing"]["xs"], 0))

    # ---- (b) Content Card ----
    content_card = Card(left_column)
    content_card.pack(fill="x", pady=(0, theme["spacing"]["md"]))

    # Content label
    content_label = tk.Label(
        content_card.inner_frame,
        text=config.content_label,
        bg=theme["colors"]["bg_card"],
        fg=theme["colors"]["text_primary"],
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"], theme["typography"]["font_weight_bold"]),
    )
    content_label.pack(anchor="w", pady=(0, theme["spacing"]["xs"]))

    # Textarea with character counter
    content_textarea = Input(
        content_card.inner_frame,
        placeholder="Nhập nội dung bài viết...",
        max_length=config.content_char_limit,
        multiline=True,
    )
    content_textarea.pack(fill="x")
    
    # Error label for empty content
    content_error_label = tk.Label(
        content_card.inner_frame,
        text="Vui lòng nhập nội dung",
        bg=theme["colors"]["bg_primary"],
        fg=theme["colors"]["status_failed"],
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_small"]),
    )
    content_error_label.pack(anchor="w", pady=(theme["spacing"]["xs"], 0))
    content_error_label.pack_forget()  # initially hidden
    
    # Update form state on content change and handle counter color
    def _on_content_change(event=None):
        form_state["content"] = content_textarea.get()
        # Update counter color if over limit
        current_length = len(form_state["content"])
        if current_length > config.content_char_limit:
            content_textarea.counter_label.configure(foreground=theme["colors"]["status_failed"])
        else:
            content_textarea.counter_label.configure(foreground=theme["colors"]["text_muted"])
        # Show/hide error label based on content emptiness
        if not form_state["content"]:
            content_error_label.pack(anchor="w", pady=(theme["spacing"]["xs"], 0))
        else:
            content_error_label.pack_forget()
    
    content_textarea.widget.bind("<KeyRelease>", _on_content_change)

    # ---- (c) Media Section ----
    if config.media_types:
        media_frame = tk.Frame(left_column, bg=theme["colors"]["bg_primary"])
        media_frame.pack(fill="x", pady=(0, theme["spacing"]["md"]))

        media_label = tk.Label(
            media_frame,
            text="2. Media",
            bg=theme["colors"]["bg_primary"],
            fg=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"], theme["typography"]["font_weight_bold"]),
        )
        media_label.pack(anchor="w", pady=(0, theme["spacing"]["xs"]))

        # Container for dropzones - side by side if 2, stacked if 1
        dropzone_container = tk.Frame(media_frame, bg=theme["colors"]["bg_primary"])
        dropzone_container.pack(fill="x")

        for i, media_type in enumerate(config.media_types):
            if len(config.media_types) == 2:
                # Side by side with equal width
                dropzone = UploadDropzone(
                    dropzone_container,
                    kind=media_type,
                    callback=lambda mt=media_type: print(f"Upload {mt} clicked"),
                )
                dropzone.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else theme["spacing"]["sm"], 0))
            else:
                # Single - full width
                dropzone = UploadDropzone(
                    dropzone_container,
                    kind=media_type,
                    callback=lambda mt=media_type: print(f"Upload {mt} clicked"),
                )
                dropzone.pack(fill="x")

    # ---- (d) Schedule Section ----
    schedule_frame = tk.Frame(left_column, bg=theme["colors"]["bg_primary"])
    schedule_frame.pack(fill="x", pady=(0, theme["spacing"]["md"]))

    schedule_label = tk.Label(
        schedule_frame,
        text="3. Lên lịch đăng",
        bg=theme["colors"]["bg_primary"],
        fg=theme["colors"]["text_primary"],
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"], theme["typography"]["font_weight_bold"]),
    )
    schedule_label.pack(anchor="w", pady=(0, theme["spacing"]["xs"]))

    schedule_controls = tk.Frame(schedule_frame, bg=theme["colors"]["bg_primary"])
    schedule_controls.pack(fill="x")

    # DateTimePicker
    datetime_picker = DateTimePicker(schedule_controls)
    datetime_picker.pack(side="left", padx=(0, theme["spacing"]["md"]))

    # "Đăng ngay" Toggle
    post_now_toggle = Toggle(schedule_controls, label="Đăng ngay")
    post_now_toggle.pack(side="left", anchor="center")

    # Update form state on datetime change
    def _on_datetime_change(*args):
        if not post_now_toggle.get():
            date_str = datetime_picker.get_date()
            time_str = datetime_picker.get_time()
            form_state["selected_datetime"] = f"{date_str} {time_str}"

    # Toggle command to disable/enable datetime picker fields and update form state
    def _on_toggle():
        if post_now_toggle.get():
            # Disable the datetime picker fields
            datetime_picker.date_entry.configure(state="disabled", foreground=theme["colors"]["text_muted"])
            datetime_picker.time_entry.configure(state="disabled", foreground=theme["colors"]["text_muted"])
            form_state["post_now"] = True
            form_state["selected_datetime"] = None
        else:
            datetime_picker.date_entry.configure(state="normal", foreground=theme["colors"]["text_primary"])
            datetime_picker.time_entry.configure(state="normal", foreground=theme["colors"]["text_primary"])
            form_state["post_now"] = False
            # Update the selected datetime from the picker
            date_str = datetime_picker.get_date()
            time_str = datetime_picker.get_time()
            form_state["selected_datetime"] = f"{date_str} {time_str}"

    # Set the toggle command
    post_now_toggle._command = _on_toggle

    # Trace changes to the date and time fields
    datetime_picker._date_str.trace("w", _on_datetime_change)
    datetime_picker._time_str.trace("w", _on_datetime_change)

    # Initialize the selected_datetime from the picker (since toggle is off by default)
    _on_datetime_change()

    # ---- (e) Post Type Selector (conditional) ----
    if config.has_post_type_selector:
        post_type_frame = tk.Frame(left_column, bg=theme["colors"]["bg_primary"])
        post_type_frame.pack(fill="x", pady=(0, theme["spacing"]["md"]))

        post_type_label = tk.Label(
            post_type_frame,
            text="4. Chọn loại đăng",
            bg=theme["colors"]["bg_primary"],
            fg=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"], theme["typography"]["font_weight_bold"]),
        )
        post_type_label.pack(anchor="w", pady=(0, theme["spacing"]["xs"]))

        # CheckboxGroup
        checkbox_group = CheckboxGroup(post_type_frame, options=config.post_type_options)
        checkbox_group.pack(anchor="w", pady=(0, theme["spacing"]["sm"]))
        
        # Update form state on checkbox change
        def _on_checkbox_change():
            form_state["checked_post_types"] = list(checkbox_group.get_checked())
        
        # Bind to each checkbox variable for change events
        for option, var in checkbox_group._variable.items():
            var.trace("w", lambda *args: _on_checkbox_change())

        # Extra text field (if configured)
        if config.extra_text_field_label:
            extra_input = Input(
                post_type_frame,
                placeholder=config.extra_text_field_label,
                max_length=500,
                multiline=True,
            )
            extra_input.pack(fill="x")

    # ---- (h) Bottom Button Row ----
    button_frame = tk.Frame(left_column, bg=theme["colors"]["bg_primary"])
    button_frame.pack(fill="x", pady=(theme["spacing"]["md"], 0))

    # "Lưu" button (secondary)
    def _on_save():
        # Validate content is not empty
        if not form_state["content"]:
            content_error_label.pack(anchor="w", pady=(theme["spacing"]["xs"], 0))
            return
        content_error_label.pack_forget()
        # Update form state with latest values before calling callback
        form_state["checked_post_types"] = list(checkbox_group.get_checked()) if config.has_post_type_selector else []
        form_state["extra_text"] = extra_input.get() if config.extra_text_field_label else ""
        if not post_now_toggle.get():
            form_state["selected_datetime"] = f"{datetime_picker.get_date()} {datetime_picker.get_time()}"
        else:
            form_state["selected_datetime"] = None
        form_state["post_now"] = post_now_toggle.get()
        on_save(form_state)
    
    save_button = Button(
        button_frame,
        text="Lưu",
        variant="secondary",
        command=_on_save,
    )
    save_button.pack(side="left", padx=(0, theme["spacing"]["sm"]))

    # Schedule button (primary, with accent color)
    def _on_schedule():
        # Validate content is not empty
        if not form_state["content"]:
            content_error_label.pack(anchor="w", pady=(theme["spacing"]["xs"], 0))
            return
        content_error_label.pack_forget()
        # Update form state with latest values before calling callback
        form_state["checked_post_types"] = list(checkbox_group.get_checked()) if config.has_post_type_selector else []
        form_state["extra_text"] = extra_input.get() if config.extra_text_field_label else ""
        if not post_now_toggle.get():
            form_state["selected_datetime"] = f"{datetime_picker.get_date()} {datetime_picker.get_time()}"
        else:
            form_state["selected_datetime"] = None
        form_state["post_now"] = post_now_toggle.get()
        on_schedule(form_state)
    
    schedule_button = Button(
        button_frame,
        text=config.schedule_button_label,
        variant="primary",
        accent_color=config.accent_color,
        command=_on_schedule,
    )
    schedule_button.pack(side="left")

    # =========================================================================
    # RIGHT COLUMN - Account Info & Recent Items
    # =========================================================================
    right_column = tk.Frame(main_frame, bg=theme["colors"]["bg_primary"])
    right_column.grid(row=0, column=1, sticky="nsew", padx=(theme["spacing"]["sm"], theme["spacing"]["md"]), pady=theme["spacing"]["md"])
    right_column.grid_rowconfigure(1, weight=1)  # Recent items area expands

    # ---- (f) Account Info Card ----
    account_card = Card(
        right_column,
        show_header=True,
        header_icon="user",
        header_title="Thông tin tài khoản",
    )
    account_card.pack(fill="x", pady=(0, theme["spacing"]["md"]))

    # Avatar + account name/handle
    account_info_frame = tk.Frame(account_card.inner_frame, bg=theme["colors"]["bg_card"])
    account_info_frame.pack(fill="x", pady=(0, theme["spacing"]["md"]))

    # Avatar
    avatar_fallback = sample_data.get("account_initials", "??")
    avatar = Avatar(account_info_frame, size=48, fallback_text=avatar_fallback)
    avatar.pack(side="left", padx=(0, theme["spacing"]["md"]))

    # Name and handle
    name_handle_frame = tk.Frame(account_info_frame, bg=theme["colors"]["bg_card"])
    name_handle_frame.pack(side="left", fill="x", expand=True)

    account_name = tk.Label(
        name_handle_frame,
        text=sample_data.get("account_name", "Tên tài khoản"),
        bg=theme["colors"]["bg_card"],
        fg=theme["colors"]["text_primary"],
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"], theme["typography"]["font_weight_bold"]),
    )
    account_name.pack(anchor="w")

    account_handle = tk.Label(
        name_handle_frame,
        text=sample_data.get("account_handle", "@handle"),
        bg=theme["colors"]["bg_card"],
        fg=theme["colors"]["text_secondary"],
        font=(theme["typography"]["font_family"], theme["typography"]["font_size_small"]),
    )
    account_handle.pack(anchor="w")

    # Stat row
    stat_labels = config.account_stat_labels
    stat_values = sample_data.get("account_stats", {})

    if stat_labels:
        stat_frame = tk.Frame(account_card.inner_frame, bg=theme["colors"]["bg_card"])
        stat_frame.pack(fill="x")

        for i, label in enumerate(stat_labels):
            stat_item = tk.Frame(stat_frame, bg=theme["colors"]["bg_card"])
            stat_item.pack(side="left", expand=True, fill="x", padx=(0, theme["spacing"]["sm"]) if i < len(stat_labels) - 1 else (0, 0))

            # Value
            value = stat_values.get(label, "0")
            value_label = tk.Label(
                stat_item,
                text=str(value),
                bg=theme["colors"]["bg_card"],
                fg=theme["colors"]["text_primary"],
                font=(theme["typography"]["font_family"], theme["typography"]["font_size_h2"], theme["typography"]["font_weight_bold"]),
            )
            value_label.pack(anchor="center")

            # Label
            label_label = tk.Label(
                stat_item,
                text=label,
                bg=theme["colors"]["bg_card"],
                fg=theme["colors"]["text_secondary"],
                font=(theme["typography"]["font_family"], theme["typography"]["font_size_small"]),
            )
            label_label.pack(anchor="center")

    # ---- (g) Recent Items Card ----
    recent_card = Card(
        right_column,
        show_header=True,
        header_icon="list",
        header_title=config.recent_items_title,
    )
    recent_card.pack(fill="both", expand=True)

    # Scrollable list of recent items
    recent_items = sample_data.get("recent_items", [])

    # Create a canvas with scrollbar for the list
    canvas_frame = tk.Frame(recent_card.inner_frame, bg=theme["colors"]["bg_card"])
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        canvas_frame,
        bg=theme["colors"]["bg_card"],
        highlightthickness=0,
    )
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=theme["colors"]["bg_card"])

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind mousewheel to canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Add recent item rows
    for item in recent_items:
        item_frame = tk.Frame(scrollable_frame, bg=theme["colors"]["bg_card"])
        item_frame.pack(fill="x", pady=theme["spacing"]["xs"])

        # Thumbnail/icon
        thumb_frame = tk.Frame(item_frame, bg=theme["colors"]["bg_card"], width=48, height=48)
        thumb_frame.pack(side="left", padx=(0, theme["spacing"]["sm"]))
        thumb_frame.pack_propagate(False)

        thumb_type = item.get("type", "post")
        if thumb_type == "image":
            thumb_icon = theme["icons"].get("image", "�������")
        elif thumb_type == "video":
            thumb_icon = theme["icons"].get("video", "����")
        else:
            thumb_icon = theme["icons"].get("document", "����")

        thumb_label = tk.Label(
            thumb_frame,
            text=thumb_icon,
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_h1"]),
        )
        thumb_label.pack(expand=True)

        # Title + date range
        text_frame = tk.Frame(item_frame, bg=theme["colors"]["bg_card"])
        text_frame.pack(side="left", fill="x", expand=True)

        title_label = tk.Label(
            text_frame,
            text=item.get("title", "Untitled"),
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            anchor="w",
        )
        title_label.pack(fill="x")

        date_label = tk.Label(
            text_frame,
            text=item.get("date_range", ""),
            bg=theme["colors"]["bg_card"],
            fg=theme["colors"]["text_muted"],
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_small"]),
            anchor="w",
        )
        date_label.pack(fill="x")

    return main_frame


# =============================================================================
# SMOKE TEST
# =============================================================================
if __name__ == "__main__":
    import tkinter as tk

    # Create two Toplevel windows with different configs
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # ---- Config 1: With post type selector and extra field (e.g., Facebook) ----
    config1 = ModuleConfig(
        platform_key="facebook",
        display_name="FACEBOOK MODULE",
        accent_color=theme["colors"]["platform"]["facebook"]["primary"],
        content_label="1. Nội dung bài viết",
        content_char_limit=5000,
        media_types=["image", "video"],
        has_post_type_selector=True,
        post_type_options=["Post", "Reels", "Fanpage", "Group"],
        extra_text_field_label="Nhập tên Fanpage (mỗi tên một dòng)",
        account_stat_labels=["Followers", "Likes", "Fanpages"],
        recent_items_title="Bài viết gần đây",
        schedule_button_label="Lên lịch",
    )

    sample_data1 = {
        "account_name": "Nguyễn Văn A",
        "account_handle": "@nguyenvana",
        "account_initials": "NV",
        "account_stats": {
            "Followers": "12.5K",
            "Likes": "8.2K",
            "Fanpages": "3",
        },
        "recent_items": [
            {"type": "image", "title": "Bài viết về du lịch", "date_range": "2 ngày trước"},
            {"type": "video", "title": "Video review sản phẩm", "date_range": "1 tuần trước"},
            {"type": "post", "title": "Chia sẻ tâm trạng", "date_range": "2 tuần trước"},
            {"type": "image", "title": "Album ảnh hội nghị", "date_range": "1 tháng trước"},
        ],
    }

    # ---- Config 2: Without post type selector (e.g., Instagram) ----
    config2 = ModuleConfig(
        platform_key="instagram",
        display_name="INSTAGRAM MODULE",
        accent_color=theme["colors"]["platform"]["instagram"]["primary"],
        content_label="1. Caption bài viết",
        content_char_limit=2200,
        media_types=["image", "video"],
        has_post_type_selector=False,
        post_type_options=[],
        extra_text_field_label=None,
        account_stat_labels=["Followers", "Following", "Posts"],
        recent_items_title="Bài đăng gần đây",
        schedule_button_label="Đăng ngay",
    )

    sample_data2 = {
        "account_name": "Trần Thị B",
        "account_handle": "@tranthib",
        "account_initials": "TB",
        "account_stats": {
            "Followers": "25.3K",
            "Following": "1.2K",
            "Posts": "156",
        },
        "recent_items": [
            {"type": "image", "title": "��nh phong cảnh đẹp", "date_range": "3 giờ trước"},
            {"type": "video", "title": "Reels vui nhộn", "date_range": "1 ngày trước"},
            {"type": "image", "title": "��nh ẩm thực", "date_range": "5 ngày trước"},
        ],
    }

    # Window 1
    win1 = tk.Toplevel(root)
    win1.title("Module Template - Config 1 (with post type selector)")
    win1.geometry("1200x800")
    win1.configure(bg=theme["colors"]["bg_primary"])
    build_module_screen(win1, config1, sample_data1)

    # Window 2
    win2 = tk.Toplevel(root)
    win2.title("Module Template - Config 2 (without post type selector)")
    win2.geometry("1200x800")
    win2.configure(bg=theme["colors"]["bg_primary"])
    build_module_screen(win2, config2, sample_data2)

    # Destroy the root window after 5 seconds to exit the mainloop automatically
    root.after(5000, root.destroy)
    root.mainloop()