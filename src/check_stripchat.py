import requests
import time
import random
import string

def is_stripchat_live(username: str):
    """
    检查 Stripchat 主播是否在播。
    返回 (is_live: bool, title: str | None)
    """
    # 1. 生成一个随机的 uniq 参数，模仿前端行为
    uniq = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    
    # 2. 使用更完整的 API URL，并带上前端常用的查询参数
    url = f"https://zh.stripchat.com/api/front/v2/models/username/{username}/cam"
    params = {
        "timezoneOffset": "-480",
        "triggerRequest": "loadCam",
        "primaryTag": "girls",
        "uniq": uniq,
    }
    
    # 3. 核心：伪装成真实浏览器的完整请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",  # 关键：声明这是一个AJAX请求
        "Referer": f"https://zh.stripchat.com/{username}", # 关键：告诉服务器请求来源页
        "Origin": "https://zh.stripchat.com",
        "Connection": "keep-alive",
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Stripchat] 请求失败: {e}")
        return False, None

    # 4. 解析逻辑可能需要调整，优先从 user.user 层级获取
    # 根据社区代码，isLive 状态可能在 data["user"]["user"]["isLive"] 中
    is_live = data.get("user", {}).get("user", {}).get("isLive", False)
    
    # 如果上面没找到，再回退到之前的解析路径
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
