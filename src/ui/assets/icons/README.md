# UI Icons Assets

This folder contains all icon assets used by the AI-AUTOMATION-POST desktop application.

## Required Icon Files

Each icon should be provided in both PNG (for raster fallback) and SVG (for scalable vector) formats.
Recommended size: 24x24px for PNG, viewBox="0 0 24 24" for SVG.

### Navigation & UI Icons

| Icon Name | Filename                        | Description                        |
| --------- | ------------------------------- | ---------------------------------- |
| Home      | `home.png` / `home.svg`         | Main dashboard / home screen       |
| Calendar  | `calendar.png` / `calendar.svg` | Scheduling, date picker            |
| Folder    | `folder.png` / `folder.svg`     | Content library, media library     |
| User      | `user.png` / `user.svg`         | Profile, account settings          |
| List      | `list.png` / `list.svg`         | List view, task queue              |
| Document  | `document.png` / `document.svg` | Content editor, post composer      |
| Gear      | `gear.png` / `gear.svg`         | Settings, configuration            |
| Activity  | `activity.png` / `activity.svg` | Activity log, history              |
| Help      | `help.png` / `help.svg`         | Help, documentation, about         |
| Bell      | `bell.png` / `bell.svg`         | Notifications, alerts              |
| Moon      | `moon.png` / `moon.svg`         | Dark mode toggle (active)          |
| Sun       | `sun.png` / `sun.svg`           | Light mode toggle (active)         |
| Chrome    | `chrome.png` / `chrome.svg`     | Browser automation, Chrome profile |

### Platform Logo Icons

| Platform  | Filename                          | Brand Color Reference             |
| --------- | --------------------------------- | --------------------------------- |
| Facebook  | `facebook.png` / `facebook.svg`   | #1877F2                           |
| TikTok    | `tiktok.png` / `tiktok.svg`       | #000000 / #FE2C55                 |
| Instagram | `instagram.png` / `instagram.svg` | #C13584 (gradient representative) |
| Threads   | `threads.png` / `threads.svg`     | #000000                           |
| Shopee    | `shopee.png` / `shopee.svg`       | #EE4D2D                           |
| YouTube   | `youtube.png` / `youtube.svg`     | #FF0000                           |

## Usage in Code

Icons are loaded via the theme module's helper functions. The application first
attempts to load the PNG/SVG asset from this folder. If the asset is not found,
it falls back to the Unicode symbol defined in `src.ui.theme.ICON_FALLBACKS`.

Example usage:

```python
from src.ui.theme import get_icon_fallback

# Get unicode fallback (used when asset not available)
icon = get_icon_fallback("facebook")  # Returns "📘"

# In UI components, prefer asset loading with fallback:
# icon_path = Path(__file__).parent.parent / "assets" / "icons" / "facebook.png"
# if icon_path.exists():
#     # Load PNG/SVG
# else:
#     # Use get_icon_fallback("facebook")
```

## Asset Guidelines

- **Format**: PNG (24x24px, transparent background) + SVG (viewBox="0 0 24 24")
- **Style**: Outlined/line style preferred, consistent stroke width (2px)
- **Color**: Single-color (monochrome) — color is applied at runtime via CSS/tint
- **Naming**: Lowercase, singular, no spaces (e.g., `calendar.png`, not `Calendar.png`)
- **License**: All icons must be MIT/Apache-2.0 licensed or created in-house

## Source Recommendations

- [Heroicons](https://heroicons.com/) — MIT licensed, outline style
- [Lucide](https://lucide.dev/) — ISC licensed, consistent stroke
- [Tabler Icons](https://tabler-icons.io/) — MIT licensed
- [Phosphor Icons](https://phosphoricons.com/) — MIT licensed

## Adding New Icons

1. Add both PNG and SVG files to this folder
2. Update this README with the new icon entry
3. Add the unicode fallback to `src/ui/theme.py` in `ICON_FALLBACKS`
4. Run any asset optimization/build steps if configured
