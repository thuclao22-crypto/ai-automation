"""Sample dashboard data for the Dashboard screen.

This module provides static sample data structures used by the Dashboard screen.
All displayed values in the Dashboard come from these structures — no literal
strings/numbers should be typed directly inside widget-construction calls.
"""

# =============================================================================
# STAT CARDS (4 entries)
# =============================================================================
STAT_CARDS = [
    {
        "label": "Tổng công việc",
        "value": 128,
        "subtext": "All Platforms",
        "accent": "default",  # Uses TEXT_PRIMARY/default accent
    },
    {
        "label": "Đã lên lịch",
        "value": 56,
        "subtext": "Scheduled",
        "accent": "default",
    },
    {
        "label": "Đã hoàn thành",
        "value": 62,
        "subtext": "Completed",
        "accent": "default",
    },
    {
        "label": "Lỗi",
        "value": 10,
        "subtext": "Failed",
        "accent": "failed",  # Uses STATUS_FAILED as accent/value color
    },
]


# =============================================================================
# PLATFORM STATUS (6 entries, one per platform)
# =============================================================================
PLATFORM_STATUS = [
    {
        "platform": "facebook",
        "label": "Facebook",
        "status": "Connected",
    },
    {
        "platform": "tiktok",
        "label": "TikTok",
        "status": "Connected",
    },
    {
        "platform": "instagram",
        "label": "Instagram",
        "status": "Connected",
    },
    {
        "platform": "threads",
        "label": "Threads",
        "status": "Connected",
    },
    {
        "platform": "shopee",
        "label": "Shopee",
        "status": "Connected",
    },
    {
        "platform": "youtube",
        "label": "YouTube",
        "status": "Connected",
    },
]


# =============================================================================
# RECENT TASKS (6 entries matching the reference image exactly)
# =============================================================================
RECENT_TASKS = [
    {
        "platform": "facebook",
        "task_type": "Fanpage Post",
        "target": "Page: Tech World",
        "status": "Success",
        "time": "10:30",
    },
    {
        "platform": "tiktok",
        "task_type": "Video Post",
        "target": "Account: @tech.world",
        "status": "Success",
        "time": "10:25",
    },
    {
        "platform": "instagram",
        "task_type": "Reel",
        "target": "Account: @tech.world",
        "status": "Success",
        "time": "10:20",
    },
    {
        "platform": "threads",
        "task_type": "Post",
        "target": "Account: @tech.world",
        "status": "Scheduled",
        "time": "12:00",
    },
    {
        "platform": "shopee",
        "task_type": "Product Video",
        "target": "Shop: Tech Store",
        "status": "Failed",
        "time": "09:45",
    },
    {
        "platform": "youtube",
        "task_type": "Video Upload",
        "target": "Channel: Tech World",
        "status": "Success",
        "time": "08:30",
    },
]


# =============================================================================
# UPCOMING SCHEDULE (5 entries matching the reference image)
# =============================================================================
UPCOMING_SCHEDULE = [
    {
        "time": "12:00",
        "title": "Threads - Post",
        "subtext": "1 task",
    },
    {
        "time": "13:00",
        "title": "Facebook - Group Post",
        "subtext": "2 tasks",
    },
    {
        "time": "15:00",
        "title": "Instagram - Post",
        "subtext": "1 task",
    },
    {
        "time": "18:00",
        "title": "TikTok - Video Post",
        "subtext": "1 task",
    },
    {
        "time": "20:00",
        "title": "YouTube - Video",
        "subtext": "1 task",
    },
]


# =============================================================================
# SYSTEM STATUS (4 entries)
# =============================================================================
SYSTEM_STATUS = [
    {
        "name": "Chrome",
        "value": "Connected",
    },
    {
        "name": "Worker",
        "value": "Running (3)",
    },
    {
        "name": "Database",
        "value": "Connected",
    },
    {
        "name": "Storage",
        "value": "125 GB / 500 GB",
    },
]


# =============================================================================
# PROFILE INFO
# =============================================================================
PROFILE_INFO = {
    "name": "Default Profile",
    "status": "Connected",
}


# =============================================================================
# GENERAL FEATURES (9 strings)
# =============================================================================
GENERAL_FEATURES = [
    "Theo dõi tổng quan tất cả nền tảng",
    "Quản lý lịch đăng chung",
    "Thư viện nội dung dùng chung",
    "Quản lý tài khoản & Profile Chrome",
    "Quản lý công việc & Worker",
    "Nhật ký hệ thống",
    "Cấu hình chung",
    "Giám sát hệ thống",
    "Kết nối Chrome",
]


# =============================================================================
# WORKFLOW STEPS (5 entries in order)
# =============================================================================
WORKFLOW_STEPS = [
    {"label": "Tạo nội dung", "color": "purple"},
    {"label": "Chọn nền tảng", "color": "blue"},
    {"label": "Cấu hình đăng bài", "color": "teal"},
    {"label": "Lên lịch đăng", "color": "orange"},
    {"label": "Theo dõi kết quả", "color": "green"},
]


if __name__ == "__main__":
    # Quick verification
    print("STAT_CARDS:", len(STAT_CARDS))
    print("PLATFORM_STATUS:", len(PLATFORM_STATUS))
    print("RECENT_TASKS:", len(RECENT_TASKS))
    print("UPCOMING_SCHEDULE:", len(UPCOMING_SCHEDULE))
    print("SYSTEM_STATUS:", len(SYSTEM_STATUS))
    print("PROFILE_INFO:", PROFILE_INFO)
    print("GENERAL_FEATURES:", len(GENERAL_FEATURES))
    print("WORKFLOW_STEPS:", len(WORKFLOW_STEPS))
    print("\nSample data loaded successfully!")