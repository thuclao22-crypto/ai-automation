"""Facebook Module Sample Data

Real sample data matching the reference image exactly.
"""

from typing import Dict, Any

# Sample data for Facebook module
facebook_sample_data: Dict[str, Any] = {
    "account": {
        "name": "Tech World",
        "handle": "@tech.world",
        "stats": {
            "Followers": "12.3K",
            "Likes": "110.2K",
            "Fanpages": "5"
        }
    },
    "recent_items": [
        {"title": "Post 1", "date_range": "10:30 - 09/06/2026"},
        {"title": "Post 2", "date_range": "09:20 - 09/06/2026"},
        {"title": "Post 3", "date_range": "08:15 - 09/06/2026"},
        {"title": "Post 4", "date_range": "07:40 - 08/06/2026"}
    ]
}