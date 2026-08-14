"""Sample data generator for platform modules.

Provides a generic function to build sample data shaped for all platform screens.
"""

from typing import Dict, Any


def build_sample_data_for(platform_key: str) -> Dict[str, Any]:
    """Build sample data for a platform module screen.

    Args:
        platform_key: Identifier for the platform (e.g., 'facebook', 'instagram').

    Returns:
        A dict shaped as:
        {
            "account": {
                "name": str,
                "handle": str,
                "stats": {label: value, ...}
            },
            "recent_items": [
                {"title": str, "date_range": str},
                ...
            ]
        }
    """
    # Generic placeholder values that can be overridden per platform later
    account_name = f"Tên tài khoản {platform_key}"
    account_handle = f"@{platform_key}_handle"
    account_stats = {
        "Followers": "10K",
        "Following": "1K",
        "Posts": "100",
    }
    recent_items = [
        {"title": f"Bài viết mẫu 1 cho {platform_key}", "date_range": "2 giờ trước"},
        {"title": f"Bài viết mẫu 2 cho {platform_key}", "date_range": "1 ngày trước"},
        {"title": f"Bài viết mẫu 3 cho {platform_key}", "date_range": "3 ngày trước"},
    ]

    return {
        "account": {
            "name": account_name,
            "handle": account_handle,
            "stats": account_stats,
        },
        "recent_items": recent_items,
    }