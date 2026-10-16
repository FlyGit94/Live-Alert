import requests


def is_bilibili_live(room_id: str) -> tuple[bool, str]:
    """
    检查B站是否开播
    返回: (是否在播, 直播间标题)
    """
    if not room_id:
        return False, ""

    url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}"
    headers = {
        # 简单伪装，避免被B站直接拒绝
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Referer": "https://live.bilibili.com/",
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()

        if data.get("code") != 0:
            print(f"[Bilibili] API 返回错误: {data}")
            return False, ""

        # live_status: 0=未开播, 1=直播中, 2=轮播
        live_status = data["data"].get("live_status", 0)
        title = data["data"].get("title", "")
        is_live = (live_status == 1)

        print(f"[Bilibili] live_status={live_status}, title={title}")
        return is_live, title

    except Exception as e:
        print(f"[Bilibili] 异常: {e}")
        return False, ""
