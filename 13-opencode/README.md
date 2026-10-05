# 13｜用 OpenCode 寫爬蟲

## 安裝（Ubuntu）

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
```

模型與金鑰依老師上課公布的設定；不要把 API key 寫進程式或 commit。

## 使用流程

```bash
mkdir osh-crawler && cd osh-crawler
cp ../SPEC.md .
opencode
```

在 OpenCode 裡輸入：

```text
請閱讀 SPEC.md，照規格寫 crawler.py，完成後執行一次並把輸出筆數告訴我。
不要修改 SPEC.md。
```

## 交件

- `SPEC.md`（你寫的規格）
- OpenCode 的對話紀錄（`/share` 或複製貼上）
- 產生的程式與輸出
- 你自己做的驗證（第 14 節）
