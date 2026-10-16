import json
import os
import sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from config import (
    BILIBILI_ROOM_ID,
    YOUTUBE_CHANNEL_ID,
    STATE_FILE,
)
from check_bilibili import is_bilibili_live
from check_youtube import is_youtube_live
from notify import send_pushover


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def is_youtube_check_time() -> bool:
    """判断当前北京时间是否在 8:00 ~ 10:00 之间（含8点，不含10点）"""
    beijing = timezone(timedelta(hours=8))
    now = datetime.now(beijing)
    return 8 <= now.hour < 10


def main():
    state = load_state()

    # ---------- Bilibili：每5分钟都查 ----------
    if BILIBILI_ROOM_ID:
        b_live, b_title = is_bilibili_live(BILIBILI_ROOM_ID)
        was_live = state.get("bilibili_live", False)

        if b_live and not was_live:
            send_pushover(
                title="🔴 B站开播了！",
                message=b_title or "主播开播了",
                url=f"https://live.bilibili.com/{BILIBILI_ROOM_ID}",
            )
        elif not b_live and was_live:
            print("[Bilibili] 已下播")

        state["bilibili_live"] = b_live

    # ---------- YouTube：只在北京时间 8~10 点查 ----------
    if YOUTUBE_CHANNEL_ID:
        if not is_youtube_check_time():
            print("[YouTube] 当前不在 8~10 点检查时段，跳过")
        else:
            y_live, y_title = is_youtube_live(YOUTUBE_CHANNEL_ID)
            was_live = state.get("youtube_live", False)

            if y_live and not was_live:
                send_pushover(
                    title="🔴 YouTube开播了！",
                    message=y_title or "频道开播了",
                    url=f"https://www.youtube.com/channel/{YOUTUBE_CHANNEL_ID}/live",
                )
            elif not y_live and was_live:
                print("[YouTube] 已下播")

            state["youtube_live"] = y_live

    save_state(state)
    print("检查完成")


if __name__ == "__main__":
    main()
