"""
Design Tokens & Theme Module

Centralized theme module holding every color, font, spacing, and radius value
used anywhere in the UI. No screen ever hardcodes a raw color/size literal.

Icon Strategy Decision:
-----------------------
Tkinter has no built-in icon font. We use a bundled folder of PNG/SVG icon
assets under src/ui/assets/icons/ with a text/unicode-symbol fallback for
development and environments where assets are not available.

Required icon files (to be added to src/ui/assets/icons/):
- home.png / home.svg
- calendar.png / calendar.svg
- folder.png / folder.svg
- user.png / user.svg
- list.png / list.svg
- document.png / document.svg
- gear.png / gear.svg
- activity.png / activity.svg
- help.png / help.svg
- bell.png / bell.svg
- moon.png / moon.svg (dark mode)
- sun.png / sun.svg (light mode)
- chrome.png / chrome.svg
- facebook.png / facebook.svg
- tiktok.png / tiktok.svg
- instagram.png / instagram.svg
- threads.png / threads.svg
- shopee.png / shopee.svg
- youtube.png / youtube.svg

Unicode fallbacks are defined in ICON_FALLBACKS dict below.
"""

from __future__ import annotations

from typing import Dict, Tuple


# =============================================================================
# BASE SURFACE COLORS
# =============================================================================

# Near-black app background — main window background
BG_PRIMARY: str = "#0E1116"

# Slightly lighter panel background — cards, sidebars, dialogs
BG_CARD: str = "#171B23"

# Subtle gray for borders, dividers, input outlines
BORDER_COLOR: str = "#262B36"


# =============================================================================
# TEXT COLORS
# =============================================================================

# Primary text — headings, body text on dark surfaces
TEXT_PRIMARY: str = "#F5F6F7"

# Secondary text — labels, descriptions, less prominent content
TEXT_SECONDARY: str = "#9AA1AC"

# Muted text — placeholder text, disabled states, hints
TEXT_MUTED: str = "#6B7280"


# =============================================================================
# STATUS COLORS
# =============================================================================

# Success state — published, completed, connected
STATUS_SUCCESS: str = "#22C55E"

# Failed state — error, disconnected, failed publish
STATUS_FAILED: str = "#EF4444"

# Scheduled state — pending, queued, waiting
STATUS_SCHEDULED: str = "#3B82F6"

# Warning state — caution, rate limit, needs attention
STATUS_WARNING: str = "#F59E0B"


# =============================================================================
# PLATFORM ACCENT COLORS
# =============================================================================

# Facebook brand blue
FACEBOOK_ACCENT: str = "#1877F2"

# TikTok primary black + secondary pink/red
TIKTOK_ACCENT: str = "#000000"
TIKTOK_ACCENT_SECONDARY: str = "#FE2C55"

# Instagram representative gradient color (purple-pink)
INSTAGRAM_ACCENT: str = "#C13584"

# Threads black
THREADS_ACCENT: str = "#000000"

# Shopee orange-red
SHOPEE_ACCENT: str = "#EE4D2D"

# YouTube red
YOUTUBE_ACCENT: str = "#FF0000"


# Platform colors dict for easy lookup by platform name string
PLATFORM_COLORS: Dict[str, Dict[str, str]] = {
    "facebook": {
        "primary": FACEBOOK_ACCENT,
        "secondary": FACEBOOK_ACCENT,
    },
    "tiktok": {
        "primary": TIKTOK_ACCENT,
        "secondary": TIKTOK_ACCENT_SECONDARY,
    },
    "instagram": {
        "primary": INSTAGRAM_ACCENT,
        "secondary": INSTAGRAM_ACCENT,
    },
    "threads": {
        "primary": THREADS_ACCENT,
        "secondary": THREADS_ACCENT,
    },
    "shopee": {
        "primary": SHOPEE_ACCENT,
        "secondary": SHOPEE_ACCENT,
    },
    "youtube": {
        "primary": YOUTUBE_ACCENT,
        "secondary": YOUTUBE_ACCENT,
    },
}


# =============================================================================
# TYPOGRAPHY
# =============================================================================

# Cross-platform safe default font family with fallbacks
# Segoe UI on Windows, system UI on macOS/Linux
FONT_FAMILY: str = "Segoe UI"

# Font sizes in points (Tkinter uses points)
FONT_SIZE_H1: int = 24      # Page titles, major headings
FONT_SIZE_H2: int = 18      # Section headings, card titles
FONT_SIZE_BODY: int = 14    # Default body text, labels, inputs
FONT_SIZE_SMALL: int = 12   # Secondary labels, captions, timestamps

# Font weights (Tkinter: "normal", "bold")
FONT_WEIGHT_REGULAR: str = "normal"
FONT_WEIGHT_BOLD: str = "bold"


# =============================================================================
# SPACING SCALE
# =============================================================================
# Pixel-equivalent units for padding/margins in Tkinter.
# Base unit = 4px. All values are multiples of 4 for visual rhythm.

SPACE_XS: int = 4   # Tight spacing — icon gaps, inline element spacing
SPACE_SM: int = 8   # Small spacing — internal padding, form field gaps
SPACE_MD: int = 16  # Medium spacing — card padding, section gaps
SPACE_LG: int = 24  # Large spacing — major section separation
SPACE_XL: int = 32  # Extra large spacing — page margins, modal padding

# Spacing scale as a dict for programmatic access
SPACING: Dict[str, int] = {
    "xs": SPACE_XS,
    "sm": SPACE_SM,
    "md": SPACE_MD,
    "lg": SPACE_LG,
    "xl": SPACE_XL,
}


# =============================================================================
# RADIUS SCALE
# =============================================================================
# Corner radius values for card/button styling approximations in Tkinter.
# Native Tkinter has no border-radius; these values are used by a
# canvas-drawn rounded rectangle helper (to be implemented in ui/components).
# The helper draws a rounded rectangle on a Canvas widget using these radii.

RADIUS_SM: int = 4   # Small radius — buttons, badges, chips
RADIUS_MD: int = 8   # Medium radius — cards, input fields, dropdowns
RADIUS_LG: int = 12  # Large radius — modals, dialogs, major containers

# Radius scale as a dict for programmatic access
RADIUS: Dict[str, int] = {
    "sm": RADIUS_SM,
    "md": RADIUS_MD,
    "lg": RADIUS_LG,
}


# =============================================================================
# ICON FALLBACKS (Unicode symbols)
# =============================================================================
# Text/unicode-symbol fallback for environments where PNG/SVG assets
# are not available. Used when asset loading fails or during development.

ICON_FALLBACKS: Dict[str, str] = {
    "home": "🏠",
    "calendar": "📅",
    "folder": "📁",
    "user": "👤",
    "list": "📋",
    "document": "📄",
    "gear": "⚙️",
    "activity": "📊",
    "help": "❓",
    "bell": "🔔",
    "moon": "🌙",
    "sun": "☀️",
    "chrome": "🌐",
    "facebook": "📘",
    "tiktok": "🎵",
    "instagram": "📷",
    "threads": "🧵",
    "shopee": "🛍️",
    "youtube": "▶️",
}


# =============================================================================
# COMPOSITE THEME OBJECT
# =============================================================================
# Single export for convenient importing: from src.ui.theme import theme

theme = {
    "colors": {
        "bg_primary": BG_PRIMARY,
        "bg_card": BG_CARD,
        "border": BORDER_COLOR,
        "text_primary": TEXT_PRIMARY,
        "text_secondary": TEXT_SECONDARY,
        "text_muted": TEXT_MUTED,
        "status_success": STATUS_SUCCESS,
        "status_failed": STATUS_FAILED,
        "status_scheduled": STATUS_SCHEDULED,
        "status_warning": STATUS_WARNING,
        "platform": PLATFORM_COLORS,
    },
    "typography": {
        "font_family": FONT_FAMILY,
        "font_size_h1": FONT_SIZE_H1,
        "font_size_h2": FONT_SIZE_H2,
        "font_size_body": FONT_SIZE_BODY,
        "font_size_small": FONT_SIZE_SMALL,
        "font_weight_regular": FONT_WEIGHT_REGULAR,
        "font_weight_bold": FONT_WEIGHT_BOLD,
    },
    "spacing": SPACING,
    "radius": RADIUS,
    "icons": ICON_FALLBACKS,
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_platform_color(platform: str, variant: str = "primary") -> str:
    """
    Get a platform's accent color by name.

    Args:
        platform: Platform name ("facebook", "tiktok", "instagram",
                  "threads", "shopee", "youtube").
        variant: Color variant ("primary" or "secondary").

    Returns:
        Hex color string.

    Raises:
        KeyError: If platform or variant is not found.
    """
    return PLATFORM_COLORS[platform.lower()][variant]


def get_spacing(size: str) -> int:
    """
    Get spacing value by size name.

    Args:
        size: One of "xs", "sm", "md", "lg", "xl".

    Returns:
        Spacing value in pixels.

    Raises:
        KeyError: If size is not found.
    """
    return SPACING[size]


def get_radius(size: str) -> int:
    """
    Get radius value by size name.

    Args:
        size: One of "sm", "md", "lg".

    Returns:
        Radius value in pixels.

    Raises:
        KeyError: If size is not found.
    """
    return RADIUS[size]


def get_icon_fallback(name: str) -> str:
    """
    Get unicode fallback symbol for an icon.

    Args:
        name: Icon name (e.g., "home", "calendar", "facebook").

    Returns:
        Unicode symbol string, or "?" if not found.
    """
    return ICON_FALLBACKS.get(name.lower(), "?")