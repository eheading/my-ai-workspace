# MEMORY.md

## 工作空間定位
- 這個倉庫是個人 AI 工作空間。
- 目標是讓 AI 助手在不同對話中持續沿用同一個角色、記憶與工作方式。
- 重要資訊應優先沉澱到文件中，而不是只存在於對話上下文。

## 使用者協作偏好
- 偏好輕量、可長期維護的結構。
- 規則應簡潔、實用、可擴充，不過度設計。
- `AGENTS.md` 為核心文件。

## 穩定約定
- 長期記憶與每日／臨時記錄分開維護。
- 長期記憶存放在 `MEMORY.md`。
- 每日或臨時記錄存放在 `memory/daily/`.

## 已建立的系統

### x-tracker（X.com 投資追蹤系統）
- **位置**：`x-tracker/`
- **功能**：追蹤指定 X.com 帳號的投資相關貼文，每日 AI 整理摘要並透過 Telegram 推送
- **技術**：twscrape、OpenAI API、python-telegram-bot、APScheduler、SQLite、Click、Docker
- **部署**：`docker compose up -d`（需先設定 `x-tracker/.env`）
- **文件**：`x-tracker/README.md`