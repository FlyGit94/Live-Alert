# B站 / YouTube 开播监控

每5分钟检查一次，开播时通过 Pushover 推送到手机。

## 配置

在 GitHub 仓库 Settings → Secrets and variables → Actions 添加：

- PUSHOVER_USER_KEY
- PUSHOVER_APP_TOKEN
- BILIBILI_ROOM_ID
- YOUTUBE_CHANNEL_ID

## 手动测试

Actions → Check Live Status → Run workflow
