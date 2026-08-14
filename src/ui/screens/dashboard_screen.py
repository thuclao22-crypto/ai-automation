"""Dashboard screen implementation.

This module builds the Dashboard screen with four sections:
1. Stats row (4 stat cards)
2. Platforms row (6 platform status cards)
3. Recent Tasks panel
4. Upcoming Schedule panel

All data comes from src.ui.data.sample_dashboard_data.
"""

import tkinter as tk
from src.ui.theme import theme, get_platform_color, get_icon_fallback
from src.ui.components.card import Card
from src.ui.components.badge import Badge
from src.ui.components.avatar import Avatar
from src.ui.components.button import Button
from src.ui.router import show_screen
from src.ui.data.sample_dashboard_data import (
    STAT_CARDS,
    PLATFORM_STATUS,
    RECENT_TASKS,
    UPCOMING_SCHEDULE,
    SYSTEM_STATUS,
    PROFILE_INFO,
    GENERAL_FEATURES,
    WORKFLOW_STEPS,
)


def build_dashboard_screen(parent: tk.Widget) -> tk.Frame:
    """
    Build the Dashboard screen.

    Args:
        parent: Parent widget to contain the screen.

    Returns:
        A Frame containing the Dashboard UI.
    """
    # Main container frame with scrollable canvas
    container = tk.Frame(parent, bg=theme["colors"]["bg_primary"])
    container.pack(fill=tk.BOTH, expand=True)

    # Create a canvas with scrollbar for vertical scrolling
    canvas = tk.Canvas(
        container,
        bg=theme["colors"]["bg_primary"],
        highlightthickness=0,
    )
    scrollbar = tk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview,
        bg=theme["colors"]["bg_card"],
        troughcolor=theme["colors"]["bg_primary"],
        activebackground=theme["colors"]["status_scheduled"],
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Content frame inside canvas
    content_frame = tk.Frame(canvas, bg=theme["colors"]["bg_primary"])
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Update scroll region when content frame changes size
    def _on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    content_frame.bind("<Configure>", _on_frame_configure)
    canvas.bind("<Configure>", _on_canvas_configure)

    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # =========================================================================
    # SECTION 1: STATS ROW (4 stat cards, horizontal)
    # =========================================================================
    stats_frame = tk.Frame(content_frame, bg=theme["colors"]["bg_primary"])
    stats_frame.pack(fill=tk.X, padx=theme["spacing"]["lg"], pady=(theme["spacing"]["lg"], theme["spacing"]["md"]))

    # Configure grid columns for equal width
    for i in range(4):
        stats_frame.grid_columnconfigure(i, weight=1, uniform="stats")

    for idx, stat in enumerate(STAT_CARDS):
        card = Card(
            stats_frame,
            show_header=False,
            padx=theme["spacing"]["md"],
            pady=theme["spacing"]["md"],
        )
        card.grid(row=0, column=idx, padx=theme["spacing"]["sm"], pady=0, sticky="nsew")

        # Label (above value)
        label = tk.Label(
            card.inner_frame,
            text=stat["label"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
        )
        label.pack(anchor="w")

        # Value (big number)
        # Determine value color based on accent
        if stat["accent"] == "failed":
            value_color = theme["colors"]["status_failed"]
        else:
            value_color = theme["colors"]["text_primary"]

        value_label = tk.Label(
            card.inner_frame,
            text=str(stat["value"]),
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_h1"],
                theme["typography"]["font_weight_bold"],
            ),
            fg=value_color,
            bg=theme["colors"]["bg_card"],
        )
        value_label.pack(anchor="w", pady=(theme["spacing"]["xs"], 0))

        # Subtext (below value)
        subtext = tk.Label(
            card.inner_frame,
            text=stat["subtext"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
        )
        subtext.pack(anchor="w")

    # =========================================================================
    # SECTION 2: PLATFORMS ROW (6 platform cards, horizontal)
    # =========================================================================
    platforms_frame = tk.Frame(content_frame, bg=theme["colors"]["bg_primary"])
    platforms_frame.pack(fill=tk.X, padx=theme["spacing"]["lg"], pady=(0, theme["spacing"]["lg"]))

    # Configure grid columns for equal width
    for i in range(6):
        platforms_frame.grid_columnconfigure(i, weight=1, uniform="platforms")

    for idx, platform in enumerate(PLATFORM_STATUS):
        card = Card(
            platforms_frame,
            show_header=False,
            padx=theme["spacing"]["md"],
            pady=theme["spacing"]["md"],
        )
        card.grid(row=0, column=idx, padx=theme["spacing"]["sm"], pady=0, sticky="nsew")

        # Platform icon (using Avatar with platform color background)
        platform_color = get_platform_color(platform["platform"], "primary")
        icon_fallback = get_icon_fallback(platform["platform"])

        # Create a small avatar-like circle for the platform icon
        icon_canvas = tk.Canvas(
            card.inner_frame,
            width=48,
            height=48,
            bg=theme["colors"]["bg_card"],
            highlightthickness=0,
        )
        icon_canvas.pack(pady=(0, theme["spacing"]["sm"]))

        # Draw circle with platform color
        icon_canvas.create_oval(
            4, 4, 44, 44,
            fill=platform_color,
            outline="",
        )
        # Draw fallback icon text
        icon_canvas.create_text(
            24, 24,
            text=icon_fallback,
            fill=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], 20),
            anchor="center",
        )

        # Platform name
        name_label = tk.Label(
            card.inner_frame,
            text=platform["label"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_body"],
                theme["typography"]["font_weight_bold"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
        )
        name_label.pack()

        # Connected status with green dot
        status_frame = tk.Frame(card.inner_frame, bg=theme["colors"]["bg_card"])
        status_frame.pack(pady=(theme["spacing"]["xs"], 0))

        # Green dot
        dot_canvas = tk.Canvas(
            status_frame,
            width=8,
            height=8,
            bg=theme["colors"]["bg_card"],
            highlightthickness=0,
        )
        dot_canvas.pack(side=tk.LEFT)
        dot_canvas.create_oval(0, 0, 8, 8, fill=theme["colors"]["status_success"], outline="")

        # "Connected" text
        status_label = tk.Label(
            status_frame,
            text=platform["status"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["status_success"],
            bg=theme["colors"]["bg_card"],
        )
        status_label.pack(side=tk.LEFT, padx=(theme["spacing"]["xs"], 0))

        # Make Facebook platform card clickable (index 0)
        if idx == 0:  # Facebook is the first platform in PLATFORM_STATUS
            def _on_facebook_click(event):
                show_screen("facebook")
            
            # Bind click to the card and all its children
            card.bind("<Button-1>", _on_facebook_click)
            card.inner_frame.bind("<Button-1>", _on_facebook_click)
            icon_canvas.bind("<Button-1>", _on_facebook_click)
            name_label.bind("<Button-1>", _on_facebook_click)
            status_frame.bind("<Button-1>", _on_facebook_click)
            dot_canvas.bind("<Button-1>", _on_facebook_click)
            status_label.bind("<Button-1>", _on_facebook_click)
            # Change cursor to indicate clickability
            card.configure(cursor="hand2")
            card.inner_frame.configure(cursor="hand2")
            icon_canvas.configure(cursor="hand2")
            name_label.configure(cursor="hand2")
            status_frame.configure(cursor="hand2")
            dot_canvas.configure(cursor="hand2")
            status_label.configure(cursor="hand2")

    # =========================================================================
    # SECTION 3 & 4: SIDE-BY-SIDE PANELS
    # =========================================================================
    bottom_frame = tk.Frame(content_frame, bg=theme["colors"]["bg_primary"])
    bottom_frame.pack(fill=tk.BOTH, expand=True, padx=theme["spacing"]["lg"], pady=(0, theme["spacing"]["lg"]))

    # Configure grid for two equal columns
    bottom_frame.grid_columnconfigure(0, weight=1, uniform="panels")
    bottom_frame.grid_columnconfigure(1, weight=1, uniform="panels")
    bottom_frame.grid_rowconfigure(0, weight=1)

    # -------------------------------------------------------------------------
    # PANEL 3: "Công việc gần đây" (Recent Tasks)
    # -------------------------------------------------------------------------
    recent_tasks_card = Card(
        bottom_frame,
        show_header=True,
        header_title="Công việc gần đây",
        padx=theme["spacing"]["md"],
        pady=theme["spacing"]["md"],
    )
    recent_tasks_card.grid(row=0, column=0, padx=(0, theme["spacing"]["sm"]), sticky="nsew")

    # Create a frame for the task rows (use pack since inner_frame uses pack)
    tasks_list_frame = tk.Frame(recent_tasks_card.inner_frame, bg=theme["colors"]["bg_card"])
    tasks_list_frame.pack(fill=tk.BOTH, expand=True)

    for idx, task in enumerate(RECENT_TASKS):
        row_frame = tk.Frame(tasks_list_frame, bg=theme["colors"]["bg_card"])
        row_frame.pack(fill=tk.X, pady=theme["spacing"]["xs"])
        row_frame.grid_columnconfigure(1, weight=1)

        # Platform icon (small)
        platform_color = get_platform_color(task["platform"], "primary")
        icon_fallback = get_icon_fallback(task["platform"])

        icon_canvas = tk.Canvas(
            row_frame,
            width=32,
            height=32,
            bg=theme["colors"]["bg_card"],
            highlightthickness=0,
        )
        icon_canvas.grid(row=0, column=0, rowspan=2, padx=(0, theme["spacing"]["sm"]), sticky="n")
        icon_canvas.create_oval(2, 2, 30, 30, fill=platform_color, outline="")
        icon_canvas.create_text(
            16, 16,
            text=icon_fallback,
            fill=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], 14),
            anchor="center",
        )

        # Task title (bold)
        title_label = tk.Label(
            row_frame,
            text=task["task_type"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_body"],
                theme["typography"]["font_weight_bold"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
            anchor="w",
        )
        title_label.grid(row=0, column=1, sticky="ew")

        # Subtitle (target, secondary text)
        subtitle_label = tk.Label(
            row_frame,
            text=task["target"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
            anchor="w",
        )
        subtitle_label.grid(row=1, column=1, sticky="ew")

        # Status badge (right side)
        status_map = {
            "Success": "success",
            "Failed": "failed",
            "Scheduled": "scheduled",
        }
        badge_status = status_map.get(task["status"], "success")
        badge = Badge(
            row_frame,
            status=badge_status,
            text=task["status"],
        )
        badge.grid(row=0, column=2, rowspan=2, padx=(theme["spacing"]["sm"], 0), sticky="e")

        # Time (below badge, small text)
        time_label = tk.Label(
            row_frame,
            text=task["time"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
        )
        time_label.grid(row=2, column=2, padx=(theme["spacing"]["sm"], 0), sticky="e")

    # -------------------------------------------------------------------------
    # PANEL 4: "Lịch sắp tới" (Upcoming Schedule)
    # -------------------------------------------------------------------------
    upcoming_card = Card(
        bottom_frame,
        show_header=True,
        header_title="Lịch sắp tới",
        padx=theme["spacing"]["md"],
        pady=theme["spacing"]["md"],
    )
    upcoming_card.grid(row=0, column=1, padx=(theme["spacing"]["sm"], 0), sticky="nsew")

    # Create a frame for the schedule rows (use pack since inner_frame uses pack)
    schedule_list_frame = tk.Frame(upcoming_card.inner_frame, bg=theme["colors"]["bg_card"])
    schedule_list_frame.pack(fill=tk.BOTH, expand=True)

    for idx, schedule in enumerate(UPCOMING_SCHEDULE):
        row_frame = tk.Frame(schedule_list_frame, bg=theme["colors"]["bg_card"])
        row_frame.pack(fill=tk.X, pady=theme["spacing"]["xs"])
        row_frame.grid_columnconfigure(1, weight=1)

        # Time (bold, left-aligned)
        time_label = tk.Label(
            row_frame,
            text=schedule["time"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_body"],
                theme["typography"]["font_weight_bold"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
            anchor="w",
            width=6,
        )
        time_label.grid(row=0, column=0, sticky="w")

        # Title
        title_label = tk.Label(
            row_frame,
            text=schedule["title"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_body"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
            anchor="w",
        )
        title_label.grid(row=0, column=1, sticky="ew")

        # Subtext count
        subtext_label = tk.Label(
            row_frame,
            text=schedule["subtext"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
            anchor="w",
        )
        subtext_label.grid(row=1, column=1, sticky="ew")

    # "Xem tất cả →" button at the bottom of the panel
    view_all_button = Button(
        upcoming_card.inner_frame,
        text="Xem tất cả →",
        variant="outline",
        accent_color=theme["colors"]["status_scheduled"],
        command=lambda: print("View all schedule clicked"),
    )
    view_all_button.pack(pady=(theme["spacing"]["md"], 0), anchor="w")

    # =========================================================================
    # SECTION 5: SYSTEM STATUS PANEL ("Hệ thống")
    # =========================================================================
    system_status_card = Card(
        content_frame,
        show_header=True,
        header_title="Hệ thống",
        padx=theme["spacing"]["md"],
        pady=theme["spacing"]["md"],
    )
    system_status_card.pack(fill=tk.X, padx=theme["spacing"]["lg"], pady=(0, theme["spacing"]["lg"]))

    # Create a frame for the status chips (horizontal row)
    status_chips_frame = tk.Frame(system_status_card.inner_frame, bg=theme["colors"]["bg_card"])
    status_chips_frame.pack(fill=tk.X)

    # Configure 4 equal columns for the 4 status chips
    for i in range(4):
        status_chips_frame.grid_columnconfigure(i, weight=1, uniform="status_chips")

    for idx, status_item in enumerate(SYSTEM_STATUS):
        chip_frame = tk.Frame(status_chips_frame, bg=theme["colors"]["bg_card"])
        chip_frame.grid(row=0, column=idx, padx=theme["spacing"]["sm"], sticky="nsew")

        # Icon (using chrome icon as generic system icon)
        icon_canvas = tk.Canvas(
            chip_frame,
            width=32,
            height=32,
            bg=theme["colors"]["bg_card"],
            highlightthickness=0,
        )
        icon_canvas.pack(pady=(0, theme["spacing"]["xs"]))
        icon_canvas.create_oval(2, 2, 30, 30, fill=theme["colors"]["status_scheduled"], outline="")
        icon_canvas.create_text(
            16, 16,
            text=get_icon_fallback("chrome"),
            fill=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], 14),
            anchor="center",
        )

        # Name (bold)
        name_label = tk.Label(
            chip_frame,
            text=status_item["name"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
                theme["typography"]["font_weight_bold"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
        )
        name_label.pack()

        # Value (secondary text)
        value_label = tk.Label(
            chip_frame,
            text=status_item["value"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
            wraplength=120,
            justify="center",
        )
        value_label.pack()

    # =========================================================================
    # SECTION 6: PROFILE PANEL + FEATURES + WORKFLOW (Bottom row)
    # =========================================================================
    # Create a frame for the bottom section with 3 columns:
    # Left: Profile panel, Middle: Features panel, Right: Workflow panel
    bottom_section_frame = tk.Frame(content_frame, bg=theme["colors"]["bg_primary"])
    bottom_section_frame.pack(fill=tk.BOTH, expand=True, padx=theme["spacing"]["lg"], pady=(0, theme["spacing"]["lg"]))

    # Configure grid: Profile (1 part), Features (1 part), Workflow (1 part)
    bottom_section_frame.grid_columnconfigure(0, weight=1, uniform="bottom_panels")
    bottom_section_frame.grid_columnconfigure(1, weight=1, uniform="bottom_panels")
    bottom_section_frame.grid_columnconfigure(2, weight=1, uniform="bottom_panels")
    bottom_section_frame.grid_rowconfigure(0, weight=1)

    # -------------------------------------------------------------------------
    # PROFILE PANEL (left column)
    # -------------------------------------------------------------------------
    profile_card = Card(
        bottom_section_frame,
        show_header=False,
        padx=theme["spacing"]["md"],
        pady=theme["spacing"]["md"],
    )
    profile_card.grid(row=0, column=0, padx=(0, theme["spacing"]["sm"]), sticky="nsew")

    # "Profile:" label
    profile_label = tk.Label(
        profile_card.inner_frame,
        text="Profile:",
        font=(
            theme["typography"]["font_family"],
            theme["typography"]["font_size_small"],
        ),
        fg=theme["colors"]["text_secondary"],
        bg=theme["colors"]["bg_card"],
        anchor="w",
    )
    profile_label.pack(fill=tk.X, pady=(0, theme["spacing"]["xs"]))

    # Dropdown-styled selector (using a frame with label + chevron)
    dropdown_frame = tk.Frame(profile_card.inner_frame, bg=theme["colors"]["bg_primary"], highlightthickness=1, highlightbackground=theme["colors"]["border"])
    dropdown_frame.pack(fill=tk.X, pady=(0, theme["spacing"]["sm"]))

    dropdown_inner = tk.Frame(dropdown_frame, bg=theme["colors"]["bg_primary"])
    dropdown_inner.pack(fill=tk.X, padx=theme["spacing"]["sm"], pady=theme["spacing"]["xs"])

    profile_name_label = tk.Label(
        dropdown_inner,
        text=PROFILE_INFO["name"],
        font=(
            theme["typography"]["font_family"],
            theme["typography"]["font_size_body"],
        ),
        fg=theme["colors"]["text_primary"],
        bg=theme["colors"]["bg_primary"],
        anchor="w",
    )
    profile_name_label.pack(side=tk.LEFT)

    # Chevron down icon
    chevron_label = tk.Label(
        dropdown_inner,
        text="��",
        font=(theme["typography"]["font_family"], 10),
        fg=theme["colors"]["text_secondary"],
        bg=theme["colors"]["bg_primary"],
    )
    chevron_label.pack(side=tk.RIGHT)

    # Green dot + "Connected" text beneath
    status_frame = tk.Frame(profile_card.inner_frame, bg=theme["colors"]["bg_card"])
    status_frame.pack(fill=tk.X, pady=(0, theme["spacing"]["md"]))

    dot_canvas = tk.Canvas(
        status_frame,
        width=8,
        height=8,
        bg=theme["colors"]["bg_card"],
        highlightthickness=0,
    )
    dot_canvas.pack(side=tk.LEFT)
    dot_canvas.create_oval(0, 0, 8, 8, fill=theme["colors"]["status_success"], outline="")

    connected_label = tk.Label(
        status_frame,
        text=PROFILE_INFO["status"],
        font=(
            theme["typography"]["font_family"],
            theme["typography"]["font_size_small"],
        ),
        fg=theme["colors"]["status_success"],
        bg=theme["colors"]["bg_card"],
    )
    connected_label.pack(side=tk.LEFT, padx=(theme["spacing"]["xs"], 0))

    # "OPEN CHROME" button (full width, Facebook accent blue)
    open_chrome_button = Button(
        profile_card.inner_frame,
        text="OPEN CHROME",
        variant="primary",
        accent_color=theme["colors"]["platform"]["facebook"]["primary"],
        command=lambda: print("Open Chrome clicked"),
    )
    open_chrome_button.pack(fill=tk.X)

    # -------------------------------------------------------------------------
    # FEATURES PANEL (middle column) - "Tính năng chung (màn hình chính)"
    # -------------------------------------------------------------------------
    features_card = Card(
        bottom_section_frame,
        show_header=True,
        header_title="Tính năng chung (màn hình chính)",
        padx=theme["spacing"]["md"],
        pady=theme["spacing"]["md"],
    )
    features_card.grid(row=0, column=1, padx=theme["spacing"]["sm"], sticky="nsew")

    # Bulleted list of features
    features_list_frame = tk.Frame(features_card.inner_frame, bg=theme["colors"]["bg_card"])
    features_list_frame.pack(fill=tk.BOTH, expand=True)

    for feature in GENERAL_FEATURES:
        feature_row = tk.Frame(features_list_frame, bg=theme["colors"]["bg_card"])
        feature_row.pack(fill=tk.X, pady=theme["spacing"]["xs"])

        # Bullet marker
        bullet_label = tk.Label(
            feature_row,
            text="•",
            font=(theme["typography"]["font_family"], theme["typography"]["font_size_body"]),
            fg=theme["colors"]["text_secondary"],
            bg=theme["colors"]["bg_card"],
        )
        bullet_label.pack(side=tk.LEFT, padx=(0, theme["spacing"]["sm"]))

        # Feature text
        feature_label = tk.Label(
            feature_row,
            text=feature,
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
            anchor="w",
            wraplength=250,
            justify="left",
        )
        feature_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # -------------------------------------------------------------------------
    # WORKFLOW PANEL (right column) - "Luồng hoạt động chung"
    # -------------------------------------------------------------------------
    workflow_card = Card(
        bottom_section_frame,
        show_header=True,
        header_title="Luồng hoạt động chung",
        padx=theme["spacing"]["md"],
        pady=theme["spacing"]["md"],
    )
    workflow_card.grid(row=0, column=2, padx=(theme["spacing"]["sm"], 0), sticky="nsew")

    # Horizontal workflow steps
    workflow_steps_frame = tk.Frame(workflow_card.inner_frame, bg=theme["colors"]["bg_card"])
    workflow_steps_frame.pack(fill=tk.X)

    # Color mapping for workflow steps
    workflow_color_map = {
        "purple": "#A855F7",   # Purple
        "blue": "#3B82F6",     # Blue
        "teal": "#14B8A6",     # Teal
        "orange": "#F97316",   # Orange
        "green": "#22C55E",    # Green (same as status_success)
    }

    for idx, step in enumerate(WORKFLOW_STEPS):
        step_frame = tk.Frame(workflow_steps_frame, bg=theme["colors"]["bg_card"])
        step_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Colored circular icon badge
        step_color = workflow_color_map.get(step["color"], theme["colors"]["status_scheduled"])
        badge_canvas = tk.Canvas(
            step_frame,
            width=40,
            height=40,
            bg=theme["colors"]["bg_card"],
            highlightthickness=0,
        )
        badge_canvas.pack(pady=(0, theme["spacing"]["xs"]))
        badge_canvas.create_oval(4, 4, 36, 36, fill=step_color, outline="")
        # Step number in the circle
        badge_canvas.create_text(
            20, 20,
            text=str(idx + 1),
            fill=theme["colors"]["text_primary"],
            font=(theme["typography"]["font_family"], 14, theme["typography"]["font_weight_bold"]),
            anchor="center",
        )

        # Step label
        step_label = tk.Label(
            step_frame,
            text=step["label"],
            font=(
                theme["typography"]["font_family"],
                theme["typography"]["font_size_small"],
            ),
            fg=theme["colors"]["text_primary"],
            bg=theme["colors"]["bg_card"],
            wraplength=100,
            justify="center",
        )
        step_label.pack()

        # Arrow separator (except after last step)
        if idx < len(WORKFLOW_STEPS) - 1:
            arrow_frame = tk.Frame(workflow_steps_frame, bg=theme["colors"]["bg_card"])
            arrow_frame.pack(side=tk.LEFT, padx=theme["spacing"]["sm"])
            arrow_label = tk.Label(
                arrow_frame,
                text="→",
                font=(theme["typography"]["font_family"], 18),
                fg=theme["colors"]["text_secondary"],
                bg=theme["colors"]["bg_card"],
            )
            arrow_label.pack()

    return container


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Dashboard Screen Smoke Test")
    root.configure(bg=theme["colors"]["bg_primary"])
    root.geometry("1200x800")

    build_dashboard_screen(root)

    root.mainloop()