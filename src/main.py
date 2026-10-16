import json
import os
import sys
from datetime import datetime, timezone, timedelta

# 让 src 目录内的模块可以互相 import
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
    """
    判断当前北京时间是否在 7:45 ~ 10:15 之间
    （含 7:45，含 10:15）
    """
    beijing = timezone(timedelta(hours=8))
    now = datetime.now(beijing)

    # 当天 7:45 和 10:15 的时间点
    start = now.replace(hour=7, minute=45, second=0, microsecond=0)
    end = now.replace(hour=10, minute=15, second=0, microsecond=0)

    return start <= now <= end


def main():
    state = load_state()

    # ---------- Bilibili（每 5 分钟都查）----------
    if BILIBILI_ROOM_ID:
        b_live, b_title = is_bilibili_live(BILIBILI_ROOM_ID)
        was_live = state.get("bilibili_live", False)

        if b_live and not was_live:
            # 刚刚开播 → 推送
            send_pushover(
                title="🔴 B站开播了！",
                message=b_title or "火羽大小姐开播了",
                url=f"https://live.bilibili.com/{BILIBILI_ROOM_ID}",
            )
        elif not b_live and was_live:
            print("[Bilibili] 已下播")

        state["bilibili_live"] = b_live

    # ---------- YouTube（只在 7:45 ~ 10:15 查）----------
    if YOUTUBE_CHANNEL_ID:
        force = os.environ.get("FORCE_YOUTUBE", "false").lower() == "true"
        if not is_youtube_check_time():
            print("[YouTube] 当前不在 7:45~10:15 检查时段，跳过")
        else:
            print(f"[YouTube] 开始检查 (force={force})")
            y_live, y_title = is_youtube_live(YOUTUBE_CHANNEL_ID)
            was_live = state.get("youtube_live", False)

            if y_live and not was_live:
                send_pushover(
                    title="🔴 YouTube开播了！",
                    message=y_title or "火羽大小姐开播了",
                    url=f"https://www.youtube.com/channel/{YOUTUBE_CHANNEL_ID}/live",
                )
            elif not y_live and was_live:
                print("[YouTube] 已下播")

            state["youtube_live"] = y_live

    save_state(state)
    print("检查完成")


if __name__ == "__main__":
    main()
