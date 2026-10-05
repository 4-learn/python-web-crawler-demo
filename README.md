# python-web-crawler-demo

勞動部 AI 大數據人才養成班「Python 網路爬蟲（2026 改版）」的上課示範程式。

- 講義（HackMD Book）：<https://hackmd.io/c/rJLTWogjfx>
- 練習站：<https://4-learn.github.io/crawler-playground/>（原始碼：[crawler-playground](https://github.com/4-learn/crawler-playground)）

這裡只有**講解用的示範**；Workshop 請自己完成。

## 環境

Ubuntu LTS（22.04／24.04）、Python 3.10 以上。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium   # 第 07 節起需要
```

所有程式預設連線 GitHub Pages 練習站。上課時老師若開教室版伺服器，改用：

```bash
export PLAYGROUND=http://老師的IP:8000/
```

## 目錄

| 資料夾 | 節次 | 內容 |
|---|---|---|
| `01-legal/` | 01 | 用 `urllib.robotparser` 判斷能不能爬 |
| `02-http/` | 02 | status code、header、ETag／304 |
| `03-api/` | 03 | 用 requests 走完 JSON 分頁；全國法規資料庫官方開放資料 |
| `04-bs4/` | 04 | CSS selector、DOM 走訪 |
| `05-pagination/` | 05 | 跟著「下一頁」爬完一部法規、JSON-LD、輸出 JSONL |
| `06-polite/` | 06 | `PoliteSession`：robots.txt、固定間隔、429 重試 |
| `07-playwright/` | 07 | requests 看不到動態內容；第一支 Playwright |
| `08-locator/` | 08 | locator、`expect`、codegen |
| `09-intercept/` | 09 | 攔截網路回應取得 JSON |
| `10-scroll-login/` | 10 | 無限捲動；登入與 `storage_state` |
| `11-trace-selenium/` | 11 | Trace Viewer；Selenium 4 與 Playwright 對照 |
| `13-opencode/` | 13 | 寫給 OpenCode 的規格範例 |
| `14-verify/` | 14 | 用 pytest 驗證爬蟲輸出 |
| `15-change/` | 15 | v1／v2 變動偵測、ETag 條件式請求、筆數歸零報警 |
| `16-mariadb/` | 16 | JSONL 寫入 MariaDB（參數化查詢＋upsert）；匯出 CSV／Markdown |

第 12 節與 17–18 節是 Workshop，沒有示範程式。

## 規則

- 練習站以外的網站，先讀 robots.txt 和服務條款，能用官方 API 就用 API。
- 每次請求間隔至少 1 秒；User-Agent 寫上你是誰。
- `state.json`（登入狀態）、密碼、API key 不要 commit。
