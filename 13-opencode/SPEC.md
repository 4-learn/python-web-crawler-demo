# 爬蟲規格範例：大量解僱勞工保護法（給 OpenCode）

> 這是上課示範用的規格。Workshop 請換成另一部法規，自己寫一份。

## 目標
從爬蟲練習站取得「大量解僱勞工保護法」（pcode `N0020012`）全部條文，存成 JSONL。

## 來源
- 首頁：https://4-learn.github.io/crawler-playground/
- 使用 API：`v1/api/laws/N0020012/page-1.json`，依 `next` 欄位走完分頁；`next` 是 `null` 就停。

## 輸出
檔名 `N0020012.jsonl`，一行一條，UTF-8，欄位：

| 欄位 | 說明 | 範例 |
|---|---|---|
| `pcode` | 法規代碼 | `N0020012` |
| `article_no` | 條號 | `第 1 條` |
| `chapter` | 章名，沒有就空字串 | |
| `content` | 條文全文，多段以 `\n` 分隔 | |
| `source_url` | 該條詳細頁網址 | `.../v1/laws/N0020012/articles/1.html` |

## 驗收
- 條數等於 API 的 `total`。
- 沒有重複的 `article_no`。
- 執行結束時印出條數，以及第一條和最後一條的條號。

## 限制（不能做的事）
- 先讀 robots.txt，不可請求 `Disallow` 的路徑。
- 每次請求間隔至少 1 秒；設定 User-Agent `course-crawler/1.0 (你的暱稱)`。
- 只用 `requests`，不要用 Selenium 或 Playwright。
- 不要把條數寫死在程式裡；從 API 讀取總數。
- 不要修改這份 SPEC.md。
