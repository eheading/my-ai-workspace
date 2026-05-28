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

## 定時任務
- `.github/workflows/daily-investment-briefing.yml`：每天北京時間 21:00（UTC 13:00）自動收集美股開市前投資熱點，以 GitHub Issue（標籤 `daily-briefing`）形式推送日報。
- 資料來源：Yahoo Finance（指數、熱門股票、板塊 ETF、新聞 RSS）、Reddit r/wallstreetbets、Reddit r/investing。
- 依賴 `GITHUB_TOKEN`（自動注入），無需額外 secrets。