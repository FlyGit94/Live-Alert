import requests
from config import PUSHOVER_USER_KEY, PUSHOVER_APP_TOKEN


def send_pushover(title: str, message: str, url: str = ""):
    """通过 Pushover 发送手机通知"""
    if not PUSHOVER_USER_KEY or not PUSHOVER_APP_TOKEN:
        print("[Pushover] 未配置 User Key 或 App Token，跳过")
        return

    data = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
    }
    if url:
        data["url"] = url
        data["url_title"] = "点击进入直播间"

    try:
        r = requests.post(
            "https://api.pushover.net/1/messages.json",
            data=data,
            timeout=15,
        )
        if r.status_code == 200:
            print(f"[Pushover] 发送成功: {title}")
        else:
            print(f"[Pushover] 发送失败: {r.status_code} {r.text}")
    except Exception as e:
        print(f"[Pushover] 异常: {e}")
