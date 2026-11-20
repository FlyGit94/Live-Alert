# check_stripchat.py
import requests
import os

def is_stripchat_live(username: str):
    worker_url = os.environ.get("STRIPCHAT_WORKER_URL", "") # 建议使用环境变量
    if not worker_url:
        print("[Stripchat] 未配置 Worker 地址")
        return False, None

    stripchat_api = f"https://zh.stripchat.com/api/front/v2/models/username/{username}/cam"
    url = f"{worker_url}?target={stripchat_api}"
    
    try:
        # Headers 可以简化，因为 Worker 会全权处理
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Stripchat] 请求失败: {e}")
        return False, None

    # 解析逻辑保持不变，优先从 data["user"]["user"] 获取[reference:4]
    is_live = data.get("user", {}).get("user", {}).get("isLive", False)
    if not is_live:
        is_live = (
            data.get("viewCam", {}).get("model", {}).get("isLive", False)
            or data.get("isLive", False)
        )

    title = (
        data.get("cam", {}).get("topic")
        or data.get("viewCam", {}).get("model", {}).get("displayName")
        or f"{username} 的直播"
    )

    return bool(is_live), title if is_live else None
