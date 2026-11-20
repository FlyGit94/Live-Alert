import os

# 从环境变量读取（在 GitHub Secrets 中配置）
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY", "")
PUSHOVER_APP_TOKEN = os.environ.get("PUSHOVER_APP_TOKEN", "")

# B站：直播间号（URL里 live.bilibili.com/ 后面那串数字）
BILIBILI_ROOM_ID = os.environ.get("BILIBILI_ROOM_ID", "")

# YouTube：频道ID（UC开头，24位）
YOUTUBE_CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID", "")

# YouTube：Data API v3 的密钥（AIzaSy 开头）
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

# 状态文件，记录上次是否在播
STATE_FILE = "state.json"
