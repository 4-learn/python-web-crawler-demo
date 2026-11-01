"""10｜無限捲動：一直往下捲，直到出現「已經到底了」（#feed-end）。

不用 time.sleep 猜秒數：每捲一次，就等「下一條」出現。
執行：python 10-scroll-login/infinite_scroll.py
"""
import os

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
MAX_ROUNDS = 50   # 安全上限：最多捲 50 次，避免無窮迴圈

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "v1/scroll/")
    items = page.locator("article.feed-item")
    items.first.wait_for()

    rounds = 0
    while page.locator("#feed-end").count() == 0 and rounds < MAX_ROUNDS:
        before = items.count()
        page.mouse.wheel(0, 3000)                                  # 往下捲
        expect(items.nth(before)).to_be_attached(timeout=10_000)   # 等第 before+1 條出現
        rounds += 1
        print(f"第 {rounds} 次捲動：{items.count()} 條")

    print("總共", items.count(), "條；最後一條：", items.last.locator(".article-no").inner_text())
    browser.close()
