# codegen：讓 Playwright 幫你錄下操作

```bash
playwright codegen https://4-learn.github.io/crawler-playground/v1/dynamic/
```

會打開兩個視窗：瀏覽器和程式碼。你在瀏覽器裡點選、選下拉選單，右邊就會產生對應的 Python。

需要桌面環境（Ubuntu Desktop 可以，純 SSH 不行）。

錄下來的程式只是**起點**：

1. 把網址、法規名稱抽成變數。
2. 刪掉多餘的點擊。
3. 加上 `expect(...)` 確認結果真的出現。
4. 把取資料的部分改成迴圈。
