# 13｜用 OpenCode 寫爬蟲

## 安裝（Ubuntu）

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
```

本課同時掛 OpenCode 免費模型（big-pickle）與 NVIDIA build，安裝、接金鑰、換模型的完整步驟見 [`docs/opencode-setup.md`](../docs/opencode-setup.md)。不要把 API key 寫進程式或 commit。

## 使用流程

```bash
cd ~
mkdir lay-off-crawler && cd lay-off-crawler
cp ~/python-web-crawler-demo/13-opencode/SPEC.md .   # 換成你 clone demo repo 的位置
opencode
```

在 OpenCode 裡輸入：

```text
請閱讀 SPEC.md，照規格寫 crawler.py，完成後執行一次並把輸出筆數告訴我。
不要修改 SPEC.md。
```

## 交件

- `SPEC.md`（你寫的規格）
- OpenCode 的對話紀錄（聊天視窗輸入 `/export` 匯出的 `session-….md`）
- 產生的程式與輸出
- 你自己做的驗證（第 14 節）
