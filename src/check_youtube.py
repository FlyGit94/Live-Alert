import requests
from config import YOUTUBE_API_KEY


def is_youtube_live(channel_id: str) -> tuple[bool, str]:
    """用 YouTube Data API v3 检查频道是否正在直播"""
    if not channel_id:
        return False, ""

    if not YOUTUBE_API_KEY:
        print("[YouTube] 未配置 YOUTUBE_API_KEY，跳过")
        return False, ""

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "eventType": "live",
        "type": "video",
        "key": YOUTUBE_API_KEY,
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        data = r.json()

        if "error" in data:
            print(f"[YouTube] API 错误: {data['error'].get('message')}")
            return False, ""

        items = data.get("items", [])
        if items:
            title = items[0]["snippet"]["title"]
            print(f"[YouTube] 正在直播: {title}")
            return True, title
        else:
            print("[YouTube] 未开播")
            return False, ""

    except Exception as e:
        print(f"[YouTube] 异常: {e}")
        return False, ""
