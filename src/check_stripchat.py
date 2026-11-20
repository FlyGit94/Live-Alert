import requests

def is_stripchat_live(username: str):
    """
    检查 Stripchat 主播是否在播。
    返回 (is_live: bool, title: str | None)
    """
    url = f"https://stripchat.com/api/front/v2/models/username/{username}/cam"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Live-Alert/1.0)",
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Stripchat] 请求失败: {e}")
        return False, None

    # 常见结构：data["viewCam"]["model"]["isLive"]
    is_live = (
        data.get("viewCam", {})
            .get("model", {})
            .get("isLive", False)
        or data.get("isLive", False)
    )

    title = (
        data.get("viewCam", {})
            .get("model", {})
            .get("displayName")
        or data.get("displayName")
        or f"{username} 的直播"
    )

    return bool(is_live), title if is_live else None
