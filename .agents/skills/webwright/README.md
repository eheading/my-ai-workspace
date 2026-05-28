# Webwright

## 來源

[microsoft/Webwright](https://github.com/microsoft/Webwright) — 將 LLM 轉換為最先進瀏覽器代理的工具。

## 狀態

`active`

## 簡介

Webwright 提供一個「代理 + 終端機 + 瀏覽器」架構，讓 AI 代理以撰寫與執行 Python/Playwright 腳本的方式完成複雜網頁任務，而非傳統的一步一動作方式。每次執行會保存截圖與動作日誌，並自我驗證結果。

## 安裝步驟

### 前置需求

- Python 3.10+
- Git

### 安裝指令（從 Webwright 倉庫根目錄執行）

```bash
git clone https://github.com/microsoft/Webwright /tmp/webwright
cd /tmp/webwright
pip install -e .
playwright install firefox
```

### Claude Code 外掛安裝（可選）

在 Claude Code 內執行：

```
/plugin marketplace add microsoft/Webwright
/plugin install webwright@webwright
```

安裝後重新啟動 Claude Code 讓外掛生效。

## 版本

- 初始安裝版本：`0.1.0`（對應 Webwright main 分支，2026-05）

## 相依套件

- `playwright`（Firefox）
- `httpx`、`pydantic`、`typer`
- 不需要額外 API 金鑰（使用宿主代理的原生視覺能力）

## 使用方式

### 直接以 Python 執行

```bash
python -m webwright.run.cli \
    -c base.yaml -c model_claude.yaml \
    -t "Search for flights from SEA to JFK on 2026-08-15" \
    --start-url https://www.google.com/flights \
    --task-id demo \
    -o outputs/default
```

### 在 Claude Code 中使用

```
/webwright:run search Google Flights for flights from SEA to JFK on 2026-08-15
/webwright:craft search a ticket on Google Flights from LAX to SFO depart June 7 return June 14
```

- `/webwright:run`：一次性腳本，針對指定任務值
- `/webwright:craft`：可重用的參數化 CLI 工具

### 使用場景

- 多步驟網頁自動化（搜尋、篩選、填表、資料擷取）
- 需要截圖證據的可重用 Playwright 腳本
- 長流程瀏覽器任務，需自我驗證結果

## 健康檢查

```bash
python -c "import webwright; print('OK')"
playwright --version
```

## 相關連結

- [GitHub Repo](https://github.com/microsoft/Webwright)
- [部落格文章](https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/)
- [專案頁面](https://microsoft.github.io/Webwright/)
