"""Facebook Module Screen

Instantiates the shared module template with Facebook-specific config and sample data.
"""

import tkinter as tk
from src.ui.theme import theme
from src.ui.data.module_config import ModuleConfig
from src.ui.data import facebook_sample_data
from src.ui.screens.module_template import build_module_screen


def build_facebook_module_screen(parent) -> tk.Frame:
    """Build the Facebook module screen using the shared template.

    Args:
        parent: Parent widget to contain the screen.

    Returns:
        A Frame containing the Facebook module screen.
    """
    config = ModuleConfig(
        platform_key="facebook",
        display_name="1. FACEBOOK MODULE",
        accent_color=theme.PLATFORM_COLORS["facebook"]["primary"],
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
    # Use the sample data we defined
    sample_data = facebook_sample_data.facebook_sample_data
    # The template provides default no-op callbacks if we pass None
    return build_module_screen(parent, config, sample_data, on_save=None, on_schedule=None)