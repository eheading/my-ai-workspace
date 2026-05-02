# X Tracker

追蹤 X.com 投資相關帳號，每日由 AI 整理為股票重點摘要，並透過 Telegram 傳送。

---

## 功能

| 功能 | 說明 |
|---|---|
| 追蹤用戶 | 新增 / 移除 X.com 帳號，可附加備注描述 |
| 自動抓取 | 每日定時使用 twscrape 抓取最新貼文 |
| AI 過濾 | OpenAI 自動篩選投資相關貼文 |
| AI 摘要 | 生成每日股票重點摘要（繁體中文） |
| Telegram 推送 | 每日自動傳送總結到指定 Telegram 聊天 |
| Docker 支援 | 一行指令部署為長期運行的服務 |

---

## 快速開始

### 1. 前置條件

- Python 3.12+（或 Docker）
- X.com 帳號（至少一個，供 twscrape 使用）
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Telegram Bot Token](https://t.me/BotFather)（向 @BotFather 建立 bot）
- Telegram Chat ID（對 bot 發送任意訊息後執行以下指令取得）

```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

---

### 2. 安裝依賴

```bash
cd x-tracker
pip install -r requirements.txt
```

---

### 3. 設定環境變數

```bash
cp .env.example .env
# 用文字編輯器填入各項設定
nano .env
```

主要設定項目：

| 變數 | 說明 |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | Telegram 聊天 ID（可為個人或群組）|
| `OPENAI_API_KEY` | OpenAI API Key |
| `OPENAI_MODEL` | AI 模型（預設 `gpt-4o-mini`）|
| `TWITTER_ACCOUNTS` | X.com 帳號 JSON 陣列（見下方說明）|
| `DAILY_SUMMARY_TIME` | 每日傳送時間（UTC，預設 `09:00`）|
| `TWEETS_PER_USER` | 每個用戶每次最多抓取幾條貼文（預設 `20`）|
| `LOOKBACK_DAYS` | 分析最近幾天的貼文（預設 `1`）|

**TWITTER_ACCOUNTS 格式**（JSON 陣列，可加多個帳號）：

```json
[
  {
    "username": "your_x_username",
    "password": "your_x_password",
    "email": "your_email@example.com",
    "email_password": "your_email_password"
  }
]
```

---

### 4. 新增追蹤用戶

```bash
python cli.py add elonmusk --desc "Tesla & SpaceX owner, market mover"
python cli.py add jimcramer --desc "CNBC Mad Money host"
python cli.py list
```

---

### 5. 手動執行（測試）

```bash
# 完整流程：抓取 → 分析 → 傳送 Telegram
python cli.py run

# 分步執行
python cli.py scrape    # 只抓取貼文
python cli.py analyse   # 只分析並儲存摘要
python cli.py send      # 只傳送今日摘要
```

---

### 6. 啟動每日排程器

```bash
python cli.py daemon
```

程式將在背景持續運行，每天於 `DAILY_SUMMARY_TIME`（UTC）執行完整流程。

---

## Docker 部署（推薦）

```bash
cd x-tracker

# 建立 .env 並填入設定
cp .env.example .env
nano .env

# 啟動
docker compose up -d

# 查看日誌
docker compose logs -f

# 停止
docker compose down
```

容器重啟後資料庫自動保留在 `./data/` 目錄。

---

## CLI 指令總覽

```
python cli.py add <username> [--desc <description>]   新增追蹤用戶
python cli.py remove <username>                        移除追蹤用戶
python cli.py list                                     列出所有追蹤用戶
python cli.py scrape                                   抓取最新貼文
python cli.py analyse                                  AI 分析並生成摘要
python cli.py send                                     傳送今日摘要到 Telegram
python cli.py run                                      完整流程（抓取+分析+傳送）
python cli.py daemon                                   啟動每日排程服務
```

---

## 架構說明

```
x-tracker/
├── main.py          入口點
├── cli.py           CLI 介面（click）
├── config.py        環境變數設定管理
├── db.py            SQLite 資料庫操作
├── scraper.py       X.com 貼文抓取（twscrape）
├── analyzer.py      AI 分析與摘要生成（OpenAI）
├── telegram_bot.py  Telegram 推送（python-telegram-bot）
├── requirements.txt 依賴清單
├── .env.example     環境變數模板
├── Dockerfile       Docker 映像設定
└── docker-compose.yml Docker Compose 部署設定
```

---

## 注意事項

- **X.com 使用條款**：twscrape 使用模擬登入方式抓取資料，請自行評估使用風險及合規性。建議使用專用帳號，避免使用主要帳號。
- **OpenAI 費用**：使用 `gpt-4o-mini` 成本較低，每日摘要約消耗 0.01–0.05 USD。
- **資料安全**：`.env` 文件包含敏感資訊，請勿提交到版本控制。`.gitignore` 已排除此文件。
