# 在 check_stripchat.py 中
import requests

def is_stripchat_live(username: str):
    # 你的 Worker 地址
    worker_url = "https://stripchat-proxy.daitw199411.workers.dev/"
    # 原始的 Stripchat API 地址
    stripchat_api = f"https://zh.stripchat.com/api/front/v2/models/username/{username}/cam"
    
    # 构造代理请求的完整 URL
    url = f"{worker_url}?target={stripchat_api}"
    
    # 可以简化 headers，因为 Worker 会处理转发
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    
    try:
        # 向你的 Worker 发起请求
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Stripchat] 请求失败: {e}")
        return False, None

    # 解析逻辑保持不变
    # 优先从 data["user"]["user"]["isLive"] 获取
    is_live = data.get("user", {}).get("user", {}).get("isLive", False)
    
    # 回退解析路径
    if not is_live:
        is_live = (
            data.get("viewCam", {})
                .get("model", {})
                .get("isLive", False)
            or data.get("isLive", False)
        )

    title = (
        data.get("cam", {}).get("topic")
        or data.get("viewCam", {})
            .get("model", {})
            .get("displayName")
        or data.get("displayName")
        or f"{username} 的直播"
    )

    return bool(is_live), title if is_live else None
