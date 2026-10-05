# 爬蟲規格：職業安全衛生法（給 OpenCode 的範例）

## 目標
從爬蟲練習站取得「職業安全衛生法」（pcode `N0060001`）全部條文，存成 JSONL。

## 來源
- 首頁：https://4-learn.github.io/crawler-playground/
- 優先使用 API：`v1/api/laws/N0060001/page-1.json`，依 `next` 欄位走完分頁。
- 若改用 HTML：`v1/laws/N0060001/`，每條是 `article.article`，下一頁是 `a.next`。

## 輸出
檔名 `N0060001.jsonl`，一行一條，UTF-8，欄位：

| 欄位 | 說明 | 範例 |
|---|---|---|
| `pcode` | 法規代碼 | `N0060001` |
| `article_no` | 條號 | `第 1 條` |
| `chapter` | 章名，沒有就空字串 | `第一章 總則` |
| `content` | 條文全文，多段以 `\n` 分隔 | |
| `source_url` | 該條詳細頁網址 | `.../v1/laws/N0060001/articles/1.html` |

## 驗收
- 共 61 條，與 API 的 `total` 相同。
- 沒有重複的 `article_no`。
- `第 1 條` 的內容以「為防止職業災害」開頭。

## 限制（不能做的事）
- 先讀 robots.txt，不可請求 `Disallow` 的路徑。
- 每次請求間隔至少 1 秒；設定 User-Agent `course-crawler/1.0 (你的暱稱)`。
- 只用 `requests`（和需要時的 `beautifulsoup4`），不要用 Selenium。
- 不要硬寫 61 這個數字來通過驗收；從 API 或頁面讀取總數。
