"""Module Configuration Data Classes

Defines the configuration schema for platform module screens.
All platform-specific values are parameterized through ModuleConfig.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModuleConfig:
    """Configuration for a platform module screen.

    All platform-specific text, colors, and layout options are defined here
    so that a single template can render any of the 6 platform screens.
    """

    # Platform identifier (e.g., "facebook", "tiktok", "instagram", "threads", "shopee", "youtube")
    platform_key: str

    # Display name shown in header (e.g., "FACEBOOK MODULE")
    display_name: str

    # Accent color hex string, sourced from theme.PLATFORM_COLORS
    accent_color: str

    # Label for the content textarea (e.g., "1. Nội dung bài viết")
    content_label: str

    # Character limit for the content textarea (e.g., 5000)
    content_char_limit: int

    # List of media types to show upload dropzones for ("image" and/or "video")
    media_types: List[str] = field(default_factory=lambda: ["image", "video"])

    # Whether to show the post type selector section
    has_post_type_selector: bool = False

    # Options for the post type checkbox group (e.g., ["Post", "Reels", "Fanpage", "Group"])
    post_type_options: List[str] = field(default_factory=list)

    # Optional extra text field label beneath checkboxes (e.g., "Nhập tên Fanpage (mỗi tên một dòng)")
    # None if not needed
    extra_text_field_label: Optional[str] = None

    # Labels for account stat row (e.g., ["Followers", "Likes", "Fanpages"])
    account_stat_labels: List[str] = field(default_factory=list)

    # Title for recent items section (e.g., "Bài viết gần đây")
    recent_items_title: str = "Bài viết gần đây"

    # Label for the schedule button (default "Lên lịch")
    schedule_button_label: str = "Lên lịch"