import requests
import re


def is_youtube_live(channel_id: str) -> tuple[bool, str]:
    """
    用 RSS 方式检查 YouTube 频道是否有直播
    免费、无配额限制，但只能查到"最新视频"，通过标题关键词判断
    返回: (是否在播, 视频标题/链接)
    """
    if not channel_id:
        return False, ""

    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            print(f"[YouTube] RSS 请求失败: {r.status_code}")
            return False, ""

        xml = r.text

        # 取最新的一个 entry
        entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
        if not entries:
            print("[YouTube] RSS 无内容")
            return False, ""

        latest = entries[0]
        title_match = re.search(r"<title>(.*?)</title>", latest, re.DOTALL)
        link_match = re.search(r'<link rel="alternate" href="(.*?)"', latest)
        title = title_match.group(1) if title_match else ""

        # RSS 无法直接判断是否直播中，只能靠标题/URL 判断
        # YouTube 直播的 URL 一般是 /watch?v=xxx，标题可能含"直播"或"LIVE"
        # 更准确的方式：请求视频页，看是否含 "isLive":true
        # 这里用简单方案：访问视频页判断
        if link_match:
            video_url = link_match.group(1)
            if "/watch" in video_url:
                if _check_video_is_live(video_url):
                    return True, title

        print(f"[YouTube] 最新视频: {title}")
        return False, ""

    except Exception as e:
        print(f"[YouTube] 异常: {e}")
        return False, ""


def _check_video_is_live(video_url: str) -> bool:
    """请求视频页，判断是否正在直播"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        r = requests.get(video_url, headers=headers, timeout=15)
        html = r.text
        # 正在直播的页面会包含这几个标志
        if '"isLive":true' in html or '"isLiveNow":true' in html:
            return True
        if 'isLiveContent":true' in html and '"isLive":true' in html:
            return True
        return False
    except Exception as e:
        print(f"[YouTube] 视频页检查异常: {e}")
        return False
